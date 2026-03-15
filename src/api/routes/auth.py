"""
Authentication endpoints — signup, login, logout, token refresh.

POST /auth/signup    — create a new Supabase user account
POST /auth/login     — exchange email/password for JWT tokens
POST /auth/logout    — invalidate the current session
POST /auth/refresh   — exchange a refresh token for new access token

All tokens are issued and validated by Supabase Auth; no local JWT signing.

Produced by: backend-agent / supabase-auth skill
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client

from api.deps import get_db, get_current_user
from api.models.auth_models import (
    AuthResponse,
    AuthUserResponse,
    LoginRequest,
    MessageResponse,
    RefreshRequest,
    SignupRequest,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


def _build_auth_response(session) -> AuthResponse:
    """Convert a Supabase session object to AuthResponse."""
    return AuthResponse(
        access_token=session.access_token,
        refresh_token=session.refresh_token,
        expires_at=session.expires_at,
        user=AuthUserResponse(
            id=str(session.user.id),
            email=session.user.email,
            role=session.user.role,
        ),
    )


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    body: SignupRequest,
    db: Annotated[Client, Depends(get_db)],
) -> AuthResponse:
    """Create a new user account and return tokens."""
    try:
        response = db.auth.sign_up({"email": body.email, "password": body.password})
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if response.session is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Signup failed — check email/password requirements.",
        )
    return _build_auth_response(response.session)


@router.post("/login", response_model=AuthResponse)
async def login(
    body: LoginRequest,
    db: Annotated[Client, Depends(get_db)],
) -> AuthResponse:
    """Authenticate with email/password and return JWT tokens."""
    try:
        response = db.auth.sign_in_with_password(
            {"email": body.email, "password": body.password}
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        ) from exc

    if response.session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    return _build_auth_response(response.session)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[Client, Depends(get_db)],
) -> MessageResponse:
    """Invalidate the current user session."""
    try:
        db.auth.sign_out()
    except Exception:
        pass  # Best-effort logout — token expiry will handle cleanup
    return MessageResponse(message="Logged out successfully.")


@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(
    body: RefreshRequest,
    db: Annotated[Client, Depends(get_db)],
) -> AuthResponse:
    """Exchange a refresh token for a new access token."""
    try:
        response = db.auth.refresh_session(body.refresh_token)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token.",
        ) from exc

    if response.session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token refresh failed.",
        )
    return _build_auth_response(response.session)
