"""
Main processor that orchestrates the PDF Gallery build pipeline.
"""

import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
import shutil

from domain import Gallery, PDFExample
from tasks import Task, BatchTask, TaskContext, TaskResult
from .cache import BuildCache
from .config import Config


class TaskGraph:
    """Manages task dependencies and execution order."""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.edges: Dict[str, Set[str]] = {}  # task -> dependencies
    
    def add_task(self, task: Task):
        """Add a task to the graph."""
        self.tasks[task.name] = task
        self.edges[task.name] = set(task.dependencies)
    
    def get_execution_order(self) -> List[str]:
        """
        Get tasks in execution order using topological sort.
        
        Returns:
            List of task names in order they should be executed
            
        Raises:
            ValueError: If there's a circular dependency
        """
        # Kahn's algorithm for topological sort
        in_degree = {task: len(deps) for task, deps in self.edges.items()}
        queue = [task for task, degree in in_degree.items() if degree == 0]
        result = []
        
        while queue:
            current = queue.pop(0)
            result.append(current)
            
            # Find tasks that depend on current
            for task, deps in self.edges.items():
                if current in deps:
                    in_degree[task] -= 1
                    if in_degree[task] == 0:
                        queue.append(task)
        
        if len(result) != len(self.tasks):
            raise ValueError("Circular dependency detected in task graph")
        
        return result


class GalleryProcessor:
    """
    Main processing orchestrator for the PDF Gallery.
    
    This class manages:
    - Task registration and dependencies
    - Build caching and incremental updates
    - Parallel processing where possible
    - Error handling and recovery
    """
    
    def __init__(self, config: Optional[Config] = None, 
                 cache_file: Optional[Path] = None,
                 verbose: bool = True):
        self.config = config or Config()
        self.cache_file = cache_file or (self.config.project_root / ".build_cache.json")
        self.cache = BuildCache(self.cache_file)
        self.verbose = verbose if verbose is not None else self.config.verbose
        
        # Initialize gallery
        self.gallery = Gallery(
            content_dir=self.config.content_dir,
            artifacts_dir=self.config.artifacts_dir
        )
        
        # Task registry
        self.tasks: Dict[str, Task] = {}
        self.batch_tasks: Dict[str, BatchTask] = {}
        
        # Processing state
        self.processed_pdfs: Set[str] = set()
        self.failed_pdfs: Dict[str, str] = {}  # pdf_id -> error
        self.task_results: Dict[str, TaskResult] = {}
    
    def register_task(self, task: Task):
        """Register a task for processing."""
        if isinstance(task, BatchTask):
            self.batch_tasks[task.name] = task
        else:
            self.tasks[task.name] = task
    
    def get_task_graph(self) -> TaskGraph:
        """Build the task dependency graph."""
        graph = TaskGraph()
        
        # Add all tasks
        for task in self.tasks.values():
            graph.add_task(task)
        for task in self.batch_tasks.values():
            graph.add_task(task)
        
        return graph
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            prefix = {
                "INFO": "ℹ️ ",
                "SUCCESS": "✅",
                "ERROR": "❌",
                "SKIP": "⏭️ ",
                "RUN": "🔄"
            }.get(level, "")
            print(f"[{timestamp}] {prefix} {message}")
    
    def process_all(self, force: bool = False) -> bool:
        """
        Process all PDFs through all registered tasks.
        
        Args:
            force: Force processing even if cache says it's up to date
            
        Returns:
            True if all processing succeeded
        """
        self.log(f"Starting full build (force={force})")
        
        # Get all PDFs to process
        pdfs = self.gallery.get_published()
        if not pdfs:
            self.log("No published PDFs found", "SKIP")
            return True
        
        self.log(f"Found {len(pdfs)} published PDFs")
        
        # Create task context
        context = TaskContext(
            artifacts_dir=self.config.artifacts_dir,
            config=self.config.to_dict(),
            cache=self.cache,
            results={},
            verbose=self.verbose
        )
        
        # Get task execution order
        try:
            graph = self.get_task_graph()
            task_order = graph.get_execution_order()
        except ValueError as e:
            self.log(f"Task dependency error: {e}", "ERROR")
            return False
        
        # Process regular tasks
        success = self._process_regular_tasks(pdfs, task_order, context, force)
        
        # Process batch tasks
        if success:
            success = self._process_batch_tasks(pdfs, task_order, context, force)
        
        # Save cache
        self.cache.save()
        
        # Report results
        self._report_results()
        
        return success and len(self.failed_pdfs) == 0
    
    def process_pdf(self, pdf_id: str, tasks: Optional[List[str]] = None,
                   force: bool = False) -> bool:
        """
        Process a single PDF through specified tasks.
        
        Args:
            pdf_id: ID of the PDF to process
            tasks: List of task names to run (None = all tasks)
            force: Force processing even if cache says it's up to date
            
        Returns:
            True if processing succeeded
        """
        pdf = self.gallery.get_example(pdf_id)
        if not pdf:
            self.log(f"PDF not found: {pdf_id}", "ERROR")
            return False
        
        if not pdf.is_published():
            self.log(f"PDF not published: {pdf_id}", "SKIP")
            return True
        
        self.log(f"Processing PDF: {pdf_id}")
        
        # Create task context
        context = TaskContext(
            artifacts_dir=self.config.artifacts_dir,
            config=self.config.to_dict(),
            cache=self.cache,
            results={},
            verbose=self.verbose
        )
        
        # Filter tasks if specified
        tasks_to_run = self.tasks
        if tasks:
            tasks_to_run = {name: task for name, task in self.tasks.items() 
                           if name in tasks}
        
        # Process the PDF
        success = True
        tasks_run = []
        tasks_skipped = []
        
        for task_name, task in tasks_to_run.items():
            if force or task.needs_processing(pdf, context):
                result = self._run_task(task, pdf, context)
                tasks_run.append(task_name)
                # Record that this task ran in the context
                context.results[task_name] = result
                if not result.success:
                    success = False
                    break
            else:
                self.log(f"Task {task_name} is up to date for {pdf_id}", "SKIP")
                tasks_skipped.append(task_name)
                # Don't update cache when skipping - the task didn't actually process the changes!
        
        # Summary
        if tasks_run:
            self.log(f"Ran tasks: {', '.join(tasks_run)}")
        if tasks_skipped:
            self.log(f"Skipped tasks: {', '.join(tasks_skipped)}")
        
        # Save cache
        self.cache.save()
        
        return success
    
    def process_changed(self) -> bool:
        """Process only PDFs that have changed."""
        self.log("Processing changed PDFs")
        
        # Find changed markdown files
        changed_files = set()
        for pdf in self.gallery.get_published():
            for approach in pdf.approaches:
                if self.cache.has_file_changed(approach.file):
                    changed_files.add(pdf.id)
                    break
        
        if not changed_files:
            self.log("No changes detected", "SKIP")
            return True
        
        self.log(f"Found {len(changed_files)} changed PDFs: {', '.join(sorted(changed_files))}")
        
        # Process each changed PDF
        success = True
        for pdf_id in changed_files:
            if not self.process_pdf(pdf_id):
                success = False
        
        return success
    
    def _process_regular_tasks(self, pdfs: List[PDFExample], 
                             task_order: List[str],
                             context: TaskContext,
                             force: bool) -> bool:
        """Process regular (per-PDF) tasks."""
        regular_task_names = [name for name in task_order if name in self.tasks]
        
        for task_name in regular_task_names:
            task = self.tasks[task_name]
            self.log(f"Running task: {task_name}")
            
            processed = 0
            skipped = 0
            failed = 0
            
            for pdf in pdfs:
                if force or task.needs_processing(pdf, context):
                    result = self._run_task(task, pdf, context)
                    if result.success:
                        processed += 1
                    else:
                        failed += 1
                        self.failed_pdfs[pdf.id] = result.error or "Unknown error"
                else:
                    skipped += 1
                    # Don't update cache when skipping - the task didn't actually process the changes!
            
            self.log(
                f"Task {task_name} complete: "
                f"{processed} processed, {skipped} skipped, {failed} failed",
                "SUCCESS" if failed == 0 else "ERROR"
            )
            
            if failed > 0 and task_name in ["metadata", "validation"]:
                # Critical tasks - stop if they fail
                return False
        
        return True
    
    def _process_batch_tasks(self, pdfs: List[PDFExample],
                           task_order: List[str],
                           context: TaskContext,
                           force: bool) -> bool:
        """Process batch tasks that handle all PDFs at once."""
        batch_task_names = [name for name in task_order if name in self.batch_tasks]
        
        for task_name in batch_task_names:
            task = self.batch_tasks[task_name]
            
            if force or task.needs_batch_processing(pdfs, context):
                self.log(f"Running batch task: {task_name}")
                
                try:
                    start_time = time.time()
                    result_data = task.process_batch(pdfs, context)
                    duration = time.time() - start_time
                    
                    result = TaskResult(
                        task_name=task_name,
                        success=True,
                        data=result_data
                    )
                    
                    # Update cache for all inputs
                    for pdf in pdfs:
                        context.cache.update_files(task.get_inputs(pdf))
                    
                    self.log(
                        f"Batch task {task_name} complete in {duration:.2f}s",
                        "SUCCESS"
                    )
                    
                except Exception as e:
                    self.log(f"Batch task {task_name} failed: {e}", "ERROR")
                    return False
            else:
                self.log(f"Batch task {task_name} is up to date", "SKIP")
        
        return True
    
    def _run_task(self, task: Task, pdf: PDFExample, 
                 context: TaskContext) -> TaskResult:
        """Run a single task on a single PDF."""
        try:
            # Validate inputs exist
            if not task.validate_inputs(pdf):
                return TaskResult(
                    task_name=task.name,
                    success=False,
                    error=f"Missing required inputs for {pdf.id}"
                )
            
            # Run the task
            start_time = time.time()
            result_data = task.process(pdf, context)
            duration = time.time() - start_time
            
            # Create result
            result = TaskResult(
                task_name=task.name,
                success=True,
                data=result_data
            )
            
            # Record outputs
            for output in task.get_outputs(pdf, context):
                if output.exists():
                    result.add_output(output)
            
            # Update cache
            context.cache.update_files(task.get_inputs(pdf))
            context.cache.record_task_result(pdf.id, task.name, result.to_dict())
            
            # Record success
            self.processed_pdfs.add(pdf.id)
            
            context.log(
                f"Task {task.name} processed {pdf.id} in {duration:.2f}s",
                "SUCCESS"
            )
            
            return result
            
        except Exception as e:
            import traceback
            error_msg = f"{type(e).__name__}: {str(e)}"
            
            context.log(
                f"Task {task.name} failed for {pdf.id}: {error_msg}",
                "ERROR"
            )
            
            # Provide more specific error information
            if isinstance(e, ImportError) and "natural_pdf" in str(e):
                context.log(
                    "💡 natural-pdf not found. Install with: pip install -e ~/Development/natural-pdf",
                    "INFO"
                )
            elif isinstance(e, FileNotFoundError):
                context.log(
                    f"💡 File not found. Check if the file exists: {e.filename}",
                    "INFO"
                )
            elif isinstance(e, json.JSONDecodeError):
                context.log(
                    "💡 Invalid JSON. Check the markdown front matter format.",
                    "INFO"
                )
            
            if self.verbose:
                traceback.print_exc()
            
            return TaskResult(
                task_name=task.name,
                success=False,
                error=error_msg
            )
    
    def sync_to_frontend(self) -> bool:
        """Sync artifacts to frontend public directory."""
        self.log("Syncing artifacts to frontend")
        
        frontend_artifacts = self.config.frontend_artifacts_dir
        frontend_artifacts.mkdir(parents=True, exist_ok=True)
        
        # Files to sync
        files_to_sync = [
            "all_metadata.json",
            "search_index.compact.json",
            "valid_pdfs.json"
        ]
        
        # Sync individual files
        for filename in files_to_sync:
            src = self.config.artifacts_dir / filename
            if src.exists():
                dst = frontend_artifacts / filename
                shutil.copy2(src, dst)
                self.log(f"Synced {filename}", "SUCCESS")
        
        # Sync directories
        dirs_to_sync = ["screenshots", "executions", "notebooks"]
        for dirname in dirs_to_sync:
            src_dir = self.config.artifacts_dir / dirname
            dst_dir = frontend_artifacts / dirname
            
            if src_dir.exists():
                # Use copytree with dirs_exist_ok for merging
                shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
                self.log(f"Synced {dirname} directory", "SUCCESS")
        
        return True
    
    def clean(self):
        """Clean all generated artifacts."""
        self.log("Cleaning all artifacts")
        
        # Remove artifacts directory
        if self.config.artifacts_dir.exists():
            shutil.rmtree(self.config.artifacts_dir)
            self.log("Removed artifacts directory", "SUCCESS")
        
        # Remove frontend artifacts
        if self.config.frontend_artifacts_dir.exists():
            shutil.rmtree(self.config.frontend_artifacts_dir)
            self.log("Removed frontend artifacts", "SUCCESS")
        
        # Clear cache
        self.cache.clear()
        self.cache.save()
        self.log("Cleared build cache", "SUCCESS")
    
    def _report_results(self):
        """Report build results."""
        self.log("=" * 60)
        self.log("BUILD SUMMARY")
        self.log("=" * 60)
        
        total_pdfs = len(self.gallery.get_published())
        processed = len(self.processed_pdfs)
        failed = len(self.failed_pdfs)
        
        self.log(f"Total PDFs: {total_pdfs}")
        self.log(f"Processed: {processed}")
        self.log(f"Failed: {failed}")
        
        if self.failed_pdfs:
            self.log("\nFailed PDFs:")
            for pdf_id, error in self.failed_pdfs.items():
                self.log(f"  - {pdf_id}: {error}", "ERROR")
                
                # Provide helpful suggestions based on error type
                if "natural_pdf" in error.lower():
                    self.log("    💡 Fix: pip install -e ~/Development/natural-pdf")
                elif "no such file" in error.lower():
                    self.log("    💡 Check if the PDF file exists in the content directory")
                elif "json" in error.lower():
                    self.log("    💡 Check markdown front matter for valid YAML/JSON")
                elif "execution" in error.lower():
                    self.log("    💡 Check Python code in markdown for syntax errors")
        
        if failed == 0:
            self.log("\nBuild completed successfully!", "SUCCESS")
            self.log("\n🎉 Your PDFs are ready at http://localhost:4321")
        else:
            self.log("\nBuild completed with errors", "ERROR")
            self.log("\n⚠️  Some PDFs failed to process. Check the errors above.")
            self.log("💡 To diagnose issues, run: python build.py diagnose")