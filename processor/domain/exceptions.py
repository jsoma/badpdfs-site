"""
Custom exceptions for the PDF Gallery processor.
"""


class PDFGalleryException(Exception):
    """Base exception for all PDF Gallery errors."""
    pass


class PDFNotFoundException(PDFGalleryException):
    """Raised when a PDF file cannot be found."""
    pass


class MetadataException(PDFGalleryException):
    """Raised when there's an error processing metadata."""
    pass


class ExecutionException(PDFGalleryException):
    """Raised when code execution fails."""
    pass


class ValidationException(PDFGalleryException):
    """Raised when validation fails."""
    pass


class TaskException(PDFGalleryException):
    """Base exception for task-related errors."""
    pass


class TaskDependencyException(TaskException):
    """Raised when task dependencies cannot be resolved."""
    pass


class CacheException(PDFGalleryException):
    """Raised when there's an error with the cache system."""
    pass