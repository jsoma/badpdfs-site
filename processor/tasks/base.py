"""
Base classes for the task system.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass
import json

from domain.models import PDFExample, Approach


@dataclass
class TaskContext:
    """Shared context passed between tasks."""
    artifacts_dir: Path
    config: Dict[str, Any]
    cache: 'BuildCache'  # Forward reference
    results: Dict[str, Any]
    verbose: bool = False
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            print(f"[{level}] {message}")
    
    def get_artifact_path(self, pdf: PDFExample, *parts) -> Path:
        """Get path to an artifact for a specific PDF."""
        return self.artifacts_dir / "pdfs" / pdf.id / Path(*parts)
    
    def read_artifact(self, path: Path) -> Any:
        """Read a JSON artifact."""
        if path.exists():
            with open(path, 'r') as f:
                return json.load(f)
        return None
    
    def write_artifact(self, path: Path, data: Any):
        """Write a JSON artifact."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)


class Task(ABC):
    """Base class for all processing tasks."""
    
    def __init__(self, name: str, dependencies: List[str] = None):
        self.name = name
        self.dependencies = dependencies or []
    
    @abstractmethod
    def process(self, pdf: PDFExample, context: TaskContext) -> Dict[str, Any]:
        """
        Process a single PDF example.
        
        Args:
            pdf: The PDF example to process
            context: Shared task context
            
        Returns:
            Dict containing task results
        """
        pass
    
    @abstractmethod
    def get_inputs(self, pdf: PDFExample) -> List[Path]:
        """
        Get input files for this task.
        
        Used for cache invalidation - if any input changes,
        the task needs to run again.
        """
        pass
    
    @abstractmethod
    def get_outputs(self, pdf: PDFExample, context: TaskContext) -> List[Path]:
        """
        Get output files for this task.
        
        Used to check if outputs exist and for cleanup.
        """
        pass
    
    def needs_processing(self, pdf: PDFExample, context: TaskContext) -> bool:
        """
        Check if this task needs to run for the given PDF.
        
        Default implementation checks:
        1. If any outputs are missing
        2. If any inputs have changed (via cache)
        3. If any dependencies have run in this session
        
        Can be overridden for custom logic.
        """
        # Check if outputs exist
        outputs = self.get_outputs(pdf, context)
        for output in outputs:
            if not output.exists():
                context.log(f"{self.name}: Output missing: {output}", "DEBUG")
                return True
        
        # Check if inputs have changed
        inputs = self.get_inputs(pdf)
        for input_path in inputs:
            if context.cache.has_file_changed(input_path):
                context.log(f"{self.name}: Input changed: {input_path}", "DEBUG")
                return True
        
        # Check if any dependencies have run in this session
        for dep in self.dependencies:
            if dep in context.results:
                context.log(f"{self.name}: Dependency '{dep}' has run, triggering reprocessing", "DEBUG")
                return True
        
        # Log why we're skipping
        context.log(f"{self.name}: All outputs exist, no inputs changed, no dependencies ran", "DEBUG")
        return False
    
    def validate_inputs(self, pdf: PDFExample) -> bool:
        """Validate that all required inputs exist."""
        for input_path in self.get_inputs(pdf):
            if not input_path.exists():
                return False
        return True
    
    def cleanup_outputs(self, pdf: PDFExample, context: TaskContext):
        """Remove all outputs for this task."""
        for output in self.get_outputs(pdf, context):
            if output.exists():
                if output.is_file():
                    output.unlink()
                else:
                    import shutil
                    shutil.rmtree(output)
    
    def __repr__(self):
        deps = f", deps={self.dependencies}" if self.dependencies else ""
        return f"{self.__class__.__name__}(name='{self.name}'{deps})"


class BatchTask(Task):
    """
    Base class for tasks that process all PDFs at once.
    
    Some tasks (like search index) need to process all PDFs
    together rather than one at a time.
    """
    
    @abstractmethod
    def process_batch(self, pdfs: List[PDFExample], context: TaskContext) -> Dict[str, Any]:
        """Process all PDFs at once."""
        pass
    
    def process(self, pdf: PDFExample, context: TaskContext) -> Dict[str, Any]:
        """Not used for batch tasks."""
        raise NotImplementedError("BatchTask uses process_batch instead")
    
    @abstractmethod
    def get_batch_outputs(self, context: TaskContext) -> List[Path]:
        """Get output files for the batch task."""
        pass
    
    def needs_batch_processing(self, pdfs: List[PDFExample], context: TaskContext) -> bool:
        """Check if batch processing is needed."""
        # Check if outputs exist
        outputs = self.get_batch_outputs(context)
        for output in outputs:
            if not output.exists():
                return True
        
        # Check if any PDF has changed
        for pdf in pdfs:
            for input_path in self.get_inputs(pdf):
                if context.cache.has_file_changed(input_path):
                    return True
        
        return False


class TaskResult:
    """Result from running a task."""
    
    def __init__(self, task_name: str, success: bool, 
                 data: Dict[str, Any] = None, error: str = None):
        self.task_name = task_name
        self.success = success
        self.data = data or {}
        self.error = error
        self.outputs_created = []
    
    def add_output(self, path: Path):
        """Record an output file created by this task."""
        self.outputs_created.append(path)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "task_name": self.task_name,
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "outputs_created": [str(p) for p in self.outputs_created]
        }