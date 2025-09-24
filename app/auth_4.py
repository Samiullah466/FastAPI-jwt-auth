import bcrypt
import jwt
import time
from fastapi import HTTPException
from jwt import ExpiredSignatureError, InvalidTokenError

# ------------------------------------------------------------------------------
# JWT & Password Utilities
# ------------------------------------------------------------------------------

SECRET_KEY = "mysecret"   
ALGORITHM = "HS256"


# ------------------------------------------------------------------------------
# Password Hashing & Verification
# ------------------------------------------------------------------------------

def hash_password(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.

    Args:
        password (str): Plain-text password.

    Returns:
        str: Secure hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a plain-text password against its hashed value.

    Args:
        password (str): Plain-text password.
        hashed (str): Hashed password (from DB).

    Returns:
        bool: True if valid, False otherwise.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


# ------------------------------------------------------------------------------
# JWT Token Management
# ------------------------------------------------------------------------------

def create_jwt(username: str, role: str) -> str:
    """
    Create a JWT access token for authentication.

    Args:
        username (str): User's unique username.
        role (str): User's role ( Teacher, Student).

    Returns:
        str: Encoded JWT token (valid for 1 hour).
    """
    payload = {
        "sub": username,       # Subject (username)
        "role": role,          # User role
        "exp": time.time() + 3600  # Expiry: 1 hour (3600s)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt(token: str) -> dict:
    """
    Decode and validate a JWT token.

    Args:
        token (str): JWT token string.

    Returns:
        dict: Decoded payload if valid.

    Raises:
        HTTPException: 401 if token expired or invalid.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
