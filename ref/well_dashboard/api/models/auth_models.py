"""
Authentication Pydantic Models

Defines request/response shapes for user registration and login.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Request body for POST /api/auth/register"""
    username: str
    password: str
    email: Optional[str] = None


class UserLogin(BaseModel):
    """Request body for POST /api/auth/login"""
    username: str
    password: str


class UserResponse(BaseModel):
    """Response shape returned for authenticated user info"""
    id: int
    username: str
    email: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
