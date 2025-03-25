import hashlib
import os
import bcrypt

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: The password to hash
        
    Returns:
        str: The hashed password
    """
    # Convert password to bytes
    password_bytes = password.encode('utf-8')
    
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return the hash as a string
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password: The password to verify
        hashed_password: The hashed password to check against
        
    Returns:
        bool: True if password matches, False otherwise
    """
    try:
        # Convert strings to bytes
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        
        # Check if password matches
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False

def generate_token(length: int = 32) -> str:
    """
    Generate a random token.
    
    Args:
        length: The length of the token to generate
        
    Returns:
        str: The generated token
    """
    return os.urandom(length).hex() 