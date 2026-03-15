"""
Pydantic v2 models for authentication endpoints.
Used by api/routes/auth.py for request validation and response serialization.

Produced by: backend-agent / supabase-auth skill
"""
from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class AuthUserResponse(BaseModel):
    id: str
    email: str | None = None
    role: str | None = None


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: int | None = None
    user: AuthUserResponse


class MessageResponse(BaseModel):
    message: str
