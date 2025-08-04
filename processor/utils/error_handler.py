"""
Error handling utilities for better user feedback.
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional


class BuildError:
    """Represents a build error with helpful context."""
    
    def __init__(self, pdf_id: str, task: str, error: str, suggestion: Optional[str] = None):
        self.pdf_id = pdf_id
        self.task = task
        self.error = error
        self.suggestion = suggestion
    
    def __str__(self):
        result = f"[{self.task}] {self.pdf_id}: {self.error}"
        if self.suggestion:
            result += f"\n    💡 {self.suggestion}"
        return result


class ErrorCollector:
    """Collects and reports errors with helpful suggestions."""
    
    def __init__(self):
        self.errors: List[BuildError] = []
        self.warnings: List[str] = []
    
    def add_error(self, pdf_id: str, task: str, error: Exception):
        """Add an error with automatic suggestion generation."""
        error_str = str(error)
        suggestion = self._get_suggestion(error, error_str)
        
        self.errors.append(BuildError(
            pdf_id=pdf_id,
            task=task,
            error=error_str,
            suggestion=suggestion
        ))
    
    def add_warning(self, message: str):
        """Add a warning message."""
        self.warnings.append(message)
    
    def _get_suggestion(self, error: Exception, error_str: str) -> Optional[str]:
        """Generate helpful suggestions based on error type."""
        
        # Import errors
        if isinstance(error, ImportError):
            if "natural_pdf" in error_str:
                return "Install natural-pdf: pip install -e ~/Development/natural-pdf"
            elif "pikepdf" in error_str:
                return "Install pikepdf: pip install pikepdf"
            elif "rich" in error_str:
                return "Install rich: pip install rich"
            return f"Install missing package: pip install {error.name}"
        
        # File errors
        if isinstance(error, FileNotFoundError):
            if ".pdf" in error_str:
                return "Check if PDF file exists in content directory"
            elif ".md" in error_str:
                return "Check if markdown file exists"
            return f"Check if file exists: {error.filename}"
        
        # JSON errors
        if "json" in error_str.lower() or "yaml" in error_str.lower():
            return "Check markdown front matter for valid YAML format"
        
        # Permission errors
        if isinstance(error, PermissionError):
            return "Check file permissions or run with appropriate privileges"
        
        # Execution errors
        if "execution" in error_str.lower():
            return "Check Python code in markdown for syntax errors"
        
        # Memory errors
        if isinstance(error, MemoryError):
            return "Try processing fewer PDFs at once or increase available memory"
        
        # Network errors
        if "urlopen" in error_str or "connection" in error_str.lower():
            return "Check internet connection for downloading resources"
        
        return None
    
    def has_errors(self) -> bool:
        """Check if any errors were collected."""
        return len(self.errors) > 0
    
    def print_summary(self):
        """Print a formatted error summary."""
        if not self.errors and not self.warnings:
            print("\n✅ No errors or warnings!")
            return
        
        if self.warnings:
            print("\n⚠️  Warnings:")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if self.errors:
            print(f"\n❌ {len(self.errors)} Errors Found:")
            print("=" * 60)
            
            # Group errors by task
            errors_by_task: Dict[str, List[BuildError]] = {}
            for error in self.errors:
                if error.task not in errors_by_task:
                    errors_by_task[error.task] = []
                errors_by_task[error.task].append(error)
            
            for task, task_errors in errors_by_task.items():
                print(f"\n{task} ({len(task_errors)} errors):")
                for error in task_errors[:5]:  # Show max 5 errors per task
                    print(f"  {error}")
                
                if len(task_errors) > 5:
                    print(f"  ... and {len(task_errors) - 5} more")
            
            print("\n" + "=" * 60)
            print("💡 Quick fixes:")
            print("  1. Run diagnostics: python build.py diagnose")
            print("  2. Force rebuild: python build.py build --force")
            print("  3. Check CLAUDE.md for common issues")
    
    def get_exit_code(self) -> int:
        """Get appropriate exit code based on errors."""
        if self.has_errors():
            return 1
        elif self.warnings:
            return 0  # Warnings don't fail the build
        return 0


def handle_build_error(error: Exception, context: str = "") -> None:
    """Handle a build error with helpful output."""
    print(f"\n❌ Build failed{' during ' + context if context else ''}")
    print(f"Error: {type(error).__name__}: {error}")
    
    # Provide specific guidance
    if isinstance(error, ImportError):
        print("\n💡 Missing dependency detected.")
        print("   Make sure you're in the virtual environment:")
        print("   source .venv/bin/activate")
    elif isinstance(error, FileNotFoundError):
        print("\n💡 File not found.")
        print("   Check if all required files exist.")
    elif isinstance(error, PermissionError):
        print("\n💡 Permission denied.")
        print("   Check file permissions.")
    
    print("\nFor more help, run: python build.py diagnose")
    sys.exit(1)