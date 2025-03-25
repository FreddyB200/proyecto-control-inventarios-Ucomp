"""Error handling utilities."""
from typing import Optional, Any, Dict
from PyQt6.QtWidgets import QMessageBox

class AppError(Exception):
    """Base exception for application errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Initialize the error.
        
        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}

class DatabaseError(AppError):
    """Exception for database-related errors."""
    pass

class ValidationError(AppError):
    """Exception for validation errors."""
    pass

class AuthenticationError(AppError):
    """Exception for authentication errors."""
    pass

def show_error(parent: Any, message: str, details: Optional[str] = None) -> None:
    """Show an error message dialog.
    
    Args:
        parent: Parent widget for the dialog
        message: Error message to display
        details: Optional detailed error information
    """
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle("Error")
    msg.setText(message)
    
    if details:
        msg.setDetailedText(details)
        
    msg.exec()

def show_warning(parent: Any, message: str, details: Optional[str] = None) -> None:
    """Show a warning message dialog.
    
    Args:
        parent: Parent widget for the dialog
        message: Warning message to display
        details: Optional detailed warning information
    """
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle("Advertencia")
    msg.setText(message)
    
    if details:
        msg.setDetailedText(details)
        
    msg.exec()

def show_info(parent: Any, message: str, details: Optional[str] = None) -> None:
    """Show an information message dialog.
    
    Args:
        parent: Parent widget for the dialog
        message: Information message to display
        details: Optional detailed information
    """
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setWindowTitle("Información")
    msg.setText(message)
    
    if details:
        msg.setDetailedText(details)
        
    msg.exec()

def handle_exception(parent: Any, error: Exception) -> None:
    """Handle an exception by showing an appropriate error dialog.
    
    Args:
        parent: Parent widget for the dialog
        error: The exception to handle
    """
    if isinstance(error, AppError):
        show_error(parent, error.message, str(error.details))
    else:
        show_error(parent, "Error inesperado", str(error)) 