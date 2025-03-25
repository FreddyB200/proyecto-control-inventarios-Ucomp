"""Input validation utilities."""
from typing import Optional
from datetime import datetime

def validate_required(value: str, field_name: str) -> Optional[str]:
    """Validate that a required field is not empty.
    
    Args:
        value: The value to validate
        field_name: Name of the field for error message
        
    Returns:
        Error message if validation fails, None otherwise
    """
    if not value or not value.strip():
        return f"{field_name} es requerido"
    return None

def validate_numeric(value: str, field_name: str) -> Optional[str]:
    """Validate that a field contains a valid number.
    
    Args:
        value: The value to validate
        field_name: Name of the field for error message
        
    Returns:
        Error message if validation fails, None otherwise
    """
    try:
        float(value)
        return None
    except ValueError:
        return f"{field_name} debe ser un número válido"

def validate_positive(value: float, field_name: str) -> Optional[str]:
    """Validate that a number is positive.
    
    Args:
        value: The number to validate
        field_name: Name of the field for error message
        
    Returns:
        Error message if validation fails, None otherwise
    """
    if value <= 0:
        return f"{field_name} debe ser mayor que 0"
    return None

def validate_date(date_str: str, field_name: str) -> Optional[str]:
    """Validate that a string is a valid date.
    
    Args:
        date_str: The date string to validate
        field_name: Name of the field for error message
        
    Returns:
        Error message if validation fails, None otherwise
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return None
    except ValueError:
        return f"{field_name} debe ser una fecha válida (YYYY-MM-DD)"

def validate_email(email: str) -> Optional[str]:
    """Validate that a string is a valid email address.
    
    Args:
        email: The email string to validate
        
    Returns:
        Error message if validation fails, None otherwise
    """
    if not email or not "@" in email or not "." in email:
        return "El email debe ser una dirección válida"
    return None

def validate_password(password: str) -> Optional[str]:
    """Validate password strength.
    
    Args:
        password: The password to validate
        
    Returns:
        Error message if validation fails, None otherwise
    """
    if len(password) < 8:
        return "La contraseña debe tener al menos 8 caracteres"
    if not any(c.isupper() for c in password):
        return "La contraseña debe contener al menos una mayúscula"
    if not any(c.islower() for c in password):
        return "La contraseña debe contener al menos una minúscula"
    if not any(c.isdigit() for c in password):
        return "La contraseña debe contener al menos un número"
    return None 