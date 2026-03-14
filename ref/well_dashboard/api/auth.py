"""
Authentication Utilities — Well Dashboard API

Provides:
    - Password hashing via bcrypt
    - JWT creation and verification
    - FastAPI dependency for protected routes (get_current_user)

Usage:
    from api.auth import get_current_user, create_access_token, get_password_hash

    # Protect an endpoint:
    @app.get("/protected")
    async def protected(user = Depends(get_current_user)):
        return {"user": user["username"]}
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from api.config import settings

# ── Password Hashing ──────────────────────────────────────────────────────────

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hashed: str) -> bool:
    """Return True if *plain* matches the stored *hashed* password."""
    return pwd_context.verify(plain, hashed)


def get_password_hash(password: str) -> str:
    """Hash a plain-text password with bcrypt and return the hash string."""
    return pwd_context.hash(password)


# ── JWT Tokens ────────────────────────────────────────────────────────────────

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a signed JWT token from *data*.

    Args:
        data:           Payload dict (must include at minimum ``user_id``).
        expires_delta:  Custom TTL; defaults to ``ACCESS_TOKEN_EXPIRE_MINUTES``.

    Returns:
        Encoded JWT string.
    """
    payload = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload.update({"exp": expire})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT token.

    Returns:
        The decoded payload dict, or ``None`` if the token is invalid/expired.
    """
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None


# ── FastAPI Dependency ────────────────────────────────────────────────────────

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    FastAPI dependency that validates the Bearer token and returns the user row.

    Raises:
        HTTPException 401: Token missing or invalid.
        HTTPException 404: Token valid but user no longer exists in DB.

    Usage::

        @router.get("/me")
        async def me(user: dict = Depends(get_current_user)):
            return user
    """
    # Import here to avoid circular imports at module load time
    from api.database import Database

    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    db = Database()
    user = await db.get_user_by_id(payload.get("user_id"))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
