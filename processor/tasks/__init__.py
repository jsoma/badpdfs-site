"""
Task system for PDF Gallery processor.
"""

from .base import Task, BatchTask, TaskContext, TaskResult
from .metadata import MetadataTask
from .execution import ExecutionTask
from .screenshots import ScreenshotTask
from .search import SearchIndexTask
from .validation import ValidationTask
from .notebooks import NotebookTask
__all__ = [
    # Base classes
    'Task',
    'BatchTask',
    'TaskContext',
    'TaskResult',
    
    # Task implementations
    'MetadataTask',
    'ExecutionTask',
    'ScreenshotTask',
    'SearchIndexTask',
    'ValidationTask',
    'NotebookTask',
]