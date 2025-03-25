"""Security utilities for password hashing and verification."""
import bcrypt

def hash_password(password: str) -> str:
    """Hash a password using bcrypt.
    
    Args:
        password: The plain text password to hash
        
    Returns:
        The hashed password as a string
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash.
    
    Args:
        password: The plain text password to verify
        hashed: The hashed password to check against
        
    Returns:
        True if the password matches, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def generate_token(length: int = 32) -> str:
    """
    Generate a random token.
    
    Args:
        length: The length of the token to generate
        
    Returns:
        str: The generated token
    """
    return os.urandom(length).hex() 