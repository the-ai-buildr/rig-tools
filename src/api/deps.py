"""
FastAPI dependency injection — all shared dependencies are defined here.

  get_db()             — yields a service-role Supabase client (bypasses RLS)
  get_user_db(token)   — yields a user-scoped Supabase client (respects RLS)
  get_current_user()   — validates the Bearer JWT and returns the Supabase user dict

NEVER instantiate supabase.Client directly inside a route handler.
Always use Depends(get_db) or Depends(get_current_user).

Produced by: backend-agent / supabase-auth skill
"""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from supabase import Client

from services.supabase import get_supabase_client, get_user_supabase_client

_bearer = HTTPBearer(auto_error=False)


def get_db() -> Client:
    """
    Dependency that returns the service-role Supabase client.
    # SERVICE ROLE: bypasses RLS — only for internal operations not tied to a user.
    """
    return get_supabase_client()


def get_user_db(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> Client:
    """
    Dependency that returns a user-scoped Supabase client.
    Requires a valid Bearer token in the Authorization header.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return get_user_supabase_client(credentials.credentials)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    db: Annotated[Client, Depends(get_db)],
) -> dict:
    """
    Dependency that validates the Bearer JWT via Supabase and returns the user dict.
    Use Depends(get_current_user) on any protected endpoint.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        response = db.auth.get_user(credentials.credentials)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    if response is None or response.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return response.user.model_dump()
