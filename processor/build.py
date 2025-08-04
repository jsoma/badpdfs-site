#!/usr/bin/env python3
"""
New unified build system using the refactored architecture.

This is a drop-in replacement for build.py that uses the new
object-oriented task system.
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from core import Config, GalleryProcessor
from tasks import (
    MetadataTask, ExecutionTask, ScreenshotTask,
    SearchIndexTask, ValidationTask, NotebookTask
)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Build management system for Bad PDFs Gallery"
    )
    parser.add_argument(
        "command",
        choices=["build", "clean", "status", "rebuild", "diagnose"],
        help="Command to run"
    )
    parser.add_argument(
        "--steps",
        nargs="+",
        choices=["metadata", "execution", "screenshots", "search_index", "validation", "notebooks"],
        help="Specific steps to run (default: all)"
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Force rebuild even if files haven't changed"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Quiet output (disable verbose mode)"
    )
    parser.add_argument(
        "--pdf",
        help="Process only a specific PDF by ID"
    )
    
    args = parser.parse_args()
    
    # Initialize configuration
    config = Config()
    
    # Create processor (verbose is True by default, use --quiet to disable)
    processor = GalleryProcessor(config, verbose=not args.quiet)
    
    # Register all tasks
    all_tasks = {
        'metadata': MetadataTask(),
        'execution': ExecutionTask(),
        'screenshots': ScreenshotTask(),
        'search_index': SearchIndexTask(),
        'validation': ValidationTask(),
        'notebooks': NotebookTask()
    }
    
    # Register tasks based on steps requested
    if args.steps:
        for step in args.steps:
            if step in all_tasks:
                processor.register_task(all_tasks[step])
    else:
        # Register all tasks
        for task in all_tasks.values():
            processor.register_task(task)
    
    # Execute command
    if args.command == "build":
        if args.pdf:
            # Process single PDF
            success = processor.process_pdf(args.pdf, tasks=args.steps, force=args.force)
        else:
            # Process all PDFs
            success = processor.process_all(force=args.force)
        
        # Sync to frontend if successful
        if success:
            processor.sync_to_frontend()
        
        sys.exit(0 if success else 1)
        
    elif args.command == "rebuild":
        # Force rebuild everything
        success = processor.process_all(force=True)
        if success:
            processor.sync_to_frontend()
        sys.exit(0 if success else 1)
        
    elif args.command == "clean":
        processor.clean()
        
    elif args.command == "status":
        # Show status
        print("PDF Gallery Build Status")
        print("=" * 60)
        
        # Check artifacts
        artifacts_exist = {
            "Metadata": (config.artifacts_dir / "all_metadata.json").exists(),
            "Search Index": (config.artifacts_dir / "search_index.compact.json").exists(),
            "Valid PDFs": (config.artifacts_dir / "valid_pdfs.json").exists(),
            "Screenshots": (config.artifacts_dir / "screenshots").exists(),
            "Executions": (config.artifacts_dir / "executions").exists(),
            "Notebooks": (config.artifacts_dir / "notebooks").exists(),
        }
        
        for name, exists in artifacts_exist.items():
            status = "✅" if exists else "❌"
            print(f"{status} {name}")
        
        # Show cache stats
        print(f"\nCache Statistics:")
        cache_stats = processor.cache.get_stats()
        print(f"  Total files tracked: {cache_stats['total_files']}")
        print(f"  Build steps recorded: {cache_stats['total_builds']}")
        print(f"  Task results cached: {cache_stats['total_task_results']}")
        
        # Show last build times
        print(f"\nLast Build Times:")
        for step in ['metadata', 'execution', 'screenshots', 'search_index', 'validation', 'notebooks']:
            last_time = processor.cache.get_last_build_time(step)
            if last_time:
                time_str = last_time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"  {step}: {time_str}")
            else:
                print(f"  {step}: Never")
    
    elif args.command == "diagnose":
        # Run comprehensive diagnostics
        print("🔍 Running Build System Diagnostics")
        print("=" * 60)
        
        # Check environment
        print("\n📋 Environment Check:")
        print(f"  Python: {sys.version.split()[0]}")
        print(f"  Working Directory: {os.getcwd()}")
        print(f"  Config Root: {config.root_dir}")
        print(f"  Content Directory: {config.content_dir}")
        print(f"  Artifacts Directory: {config.artifacts_dir}")
        print(f"  Frontend Directory: {config.frontend_dir}")
        
        # Check virtual environment
        venv_active = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        print(f"  Virtual Environment: {'✅ Active' if venv_active else '❌ Not Active'}")
        
        # Check natural-pdf installation
        try:
            import natural_pdf
            pdf_path = Path(natural_pdf.__file__).parent
            is_editable = 'site-packages' not in str(pdf_path)
            print(f"  natural-pdf: ✅ Installed ({'editable' if is_editable else 'regular'})")
            print(f"    Location: {pdf_path}")
        except ImportError:
            print(f"  natural-pdf: ❌ Not Installed")
            print(f"    Fix: pip install -e ~/Development/natural-pdf")
        
        # Check R2 configuration
        r2_key = os.environ.get("R2_ACCESS_KEY_ID")
        r2_secret = os.environ.get("R2_SECRET_ACCESS_KEY")
        if r2_key and r2_secret:
            print(f"  R2 Credentials: ✅ Configured")
        else:
            print(f"  R2 Credentials: ⚠️  Not configured (optional)")
            print(f"    To enable R2 uploads, set R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY")
        
        # Check directory structure
        print("\n📁 Directory Structure:")
        required_dirs = [
            (config.content_dir, "Content directory"),
            (config.content_dir / "pdfs", "PDFs content directory"),
            (config.artifacts_dir, "Artifacts directory"),
            (config.frontend_dir, "Frontend directory"),
            (config.frontend_dir / "public" / "artifacts", "Frontend artifacts directory"),
        ]
        
        for dir_path, name in required_dirs:
            if dir_path.exists():
                print(f"  ✅ {name}: {dir_path}")
            else:
                print(f"  ❌ {name}: Missing at {dir_path}")
        
        # Check markdown files
        print("\n📄 Content Files:")
        md_files = list(config.content_dir.glob("pdfs/**/*.md"))
        print(f"  Found {len(md_files)} markdown files")
        
        if args.pdf:
            # Check specific PDF
            pdf_dirs = list(config.content_dir.glob(f"pdfs/{args.pdf}"))
            if pdf_dirs:
                pdf_dir = pdf_dirs[0]
                print(f"\n  Checking PDF: {args.pdf}")
                md_files_in_dir = list(pdf_dir.glob("*.md"))
                print(f"    Markdown files: {len(md_files_in_dir)}")
                for md in md_files_in_dir:
                    print(f"      - {md.name}")
            else:
                print(f"\n  ❌ PDF directory not found: {args.pdf}")
        
        # Check artifacts
        print("\n🔧 Artifacts Status:")
        artifacts_status = []
        
        # Metadata
        metadata_file = config.artifacts_dir / "all_metadata.json"
        if metadata_file.exists():
            try:
                import json
                with open(metadata_file) as f:
                    metadata = json.load(f)
                artifacts_status.append(f"  ✅ Metadata: {len(metadata)} entries")
            except:
                artifacts_status.append(f"  ⚠️  Metadata: Exists but invalid JSON")
        else:
            artifacts_status.append(f"  ❌ Metadata: Missing")
        
        # Valid PDFs
        valid_pdfs_file = config.artifacts_dir / "valid_pdfs.json"
        if valid_pdfs_file.exists():
            try:
                with open(valid_pdfs_file) as f:
                    valid_pdfs = json.load(f)
                artifacts_status.append(f"  ✅ Valid PDFs: {len(valid_pdfs)} validated")
            except:
                artifacts_status.append(f"  ⚠️  Valid PDFs: Exists but invalid JSON")
        else:
            artifacts_status.append(f"  ❌ Valid PDFs: Missing")
        
        # Execution results
        exec_dir = config.artifacts_dir / "executions" / "pdfs"
        if exec_dir.exists():
            exec_count = len(list(exec_dir.glob("*/*.json")))
            artifacts_status.append(f"  ✅ Executions: {exec_count} files")
        else:
            artifacts_status.append(f"  ❌ Executions: Directory missing")
        
        for status in artifacts_status:
            print(status)
        
        # Check sync status
        print("\n🔄 Frontend Sync Status:")
        frontend_artifacts = config.frontend_dir / "public" / "artifacts"
        if frontend_artifacts.exists():
            # Check if files are in sync
            sync_issues = []
            
            for file_name in ["all_metadata.json", "valid_pdfs.json", "search_index.json"]:
                src = config.artifacts_dir / file_name
                dst = frontend_artifacts / file_name
                
                if src.exists() and not dst.exists():
                    sync_issues.append(f"  ⚠️  {file_name}: Not synced to frontend")
                elif src.exists() and dst.exists():
                    src_mtime = src.stat().st_mtime
                    dst_mtime = dst.stat().st_mtime
                    if src_mtime > dst_mtime:
                        sync_issues.append(f"  ⚠️  {file_name}: Out of sync (processor is newer)")
            
            if sync_issues:
                for issue in sync_issues:
                    print(issue)
                print(f"\n  Fix: python fix_execution_paths.py")
            else:
                print(f"  ✅ All artifacts are synced")
        else:
            print(f"  ❌ Frontend artifacts directory missing")
        
        # Suggest fixes
        print("\n💡 Suggested Actions:")
        
        action_count = 0
        
        if not venv_active:
            action_count += 1
            print(f"  {action_count}. Activate virtual environment:")
            print("     source .venv/bin/activate")
        
        try:
            import natural_pdf
        except ImportError:
            action_count += 1
            print(f"  {action_count}. Install natural-pdf:")
            print("     pip install -e ~/Development/natural-pdf")
        
        if not metadata_file.exists():
            action_count += 1
            print(f"  {action_count}. Generate metadata:")
            print("     python generate_artifacts.py")
        
        if not valid_pdfs_file.exists():
            action_count += 1
            print(f"  {action_count}. Validate artifacts:")
            print("     python validate_artifacts.py")
        
        if frontend_artifacts.exists() and 'sync_issues' in locals() and sync_issues:
            action_count += 1
            print(f"  {action_count}. Sync to frontend:")
            print("     python fix_execution_paths.py")
        
        print("\n📌 Quick fix for all issues:")
        print("   python build.py build --force")


if __name__ == "__main__":
    main()