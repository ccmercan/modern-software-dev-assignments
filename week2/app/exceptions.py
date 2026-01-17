"""
Custom exception classes for the application.
Provides structured error handling with appropriate HTTP status codes.
"""

from __future__ import annotations


class AppException(Exception):
    """Base exception for all application exceptions."""
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(AppException):
    """Exception raised when a requested resource is not found."""
    
    def __init__(self, resource_type: str, resource_id: int | str):
        message = f"{resource_type} with id {resource_id} not found"
        super().__init__(message, status_code=404)
        self.resource_type = resource_type
        self.resource_id = resource_id


class NoteNotFoundError(NotFoundError):
    """Exception raised when a note is not found."""
    
    def __init__(self, note_id: int):
        super().__init__("Note", note_id)
        self.note_id = note_id


class ActionItemNotFoundError(NotFoundError):
    """Exception raised when an action item is not found."""
    
    def __init__(self, action_item_id: int):
        super().__init__("Action item", action_item_id)
        self.action_item_id = action_item_id


class DatabaseError(AppException):
    """Exception raised for database-related errors."""
    
    def __init__(self, message: str, original_error: Exception | None = None):
        super().__init__(f"Database error: {message}", status_code=500)
        self.original_error = original_error


class ValidationError(AppException):
    """Exception raised for validation errors."""
    
    def __init__(self, message: str):
        super().__init__(message, status_code=400)
