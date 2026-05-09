# Skill: Supabase Auth

<!--
Purpose: Auth flows — signup, login, logout, session, JWT middleware, and RLS wiring.
Produced by: backend-agent
-->

## Purpose

Define every rule and pattern for Supabase authentication: signup/login/logout/refresh endpoints, JWT validation as a FastAPI dependency, session state management in Streamlit, and Row-Level Security policy wiring.

## When to Use

Activate when the task contains: **auth**, **login**, **signup**, **logout**, **session**, **JWT**, **token**, **RLS**, **row-level security**, or when touching `api/routes/auth.py`, `api/models/auth_models.py`, `api/deps.py`, `components/auth/`, or `services/supabase.py`.

## Conventions

1. Auth endpoints live exclusively in `api/routes/auth.py`.
2. JWT validation is a FastAPI dependency (`get_current_user` in `api/deps.py`) — never inline in route handlers.
3. Streamlit stores auth state in `session_state`: `auth_token`, `auth_refresh_token`, `auth_user`, `auth_expires_at`. Init to `None` in `global_init()`.
4. `auth_token` is a Supabase JWT; it is passed as `Authorization: Bearer <token>` to every protected API call.
5. The service-role key is **only** used for auth validation (`db.auth.get_user(jwt)`) and admin operations — never for user data queries.
6. User data queries always use the anon-key client with the user's JWT set via `client.postgrest.auth(jwt)`.
7. Login/signup components use `st.rerun(scope="app")` after a successful auth to apply auth-guard logic.
8. Logout clears all `auth_*` session state keys and calls the logout endpoint.
9. Supabase handles token expiry — check `auth_expires_at` before making API calls and refresh proactively.
10. RLS policies are the last line of defence; never rely on application-level filtering alone for security.

> **⚠️ supabase-py v2 auth note:**
> - `sign_up`/`sign_in_with_password` accept a single dict: `{"email": ..., "password": ...}`
> - `AuthResponse` has `.user` (User | None) and `.session` (Session | None)
> - `Session` has `.access_token`, `.refresh_token`, `.expires_at` (unix int)
> - `get_user(jwt)` returns `UserResponse` with `.user` (User | None)
> - `sign_out()` invalidates the server-side session; also clear client-side state

## Patterns

### Auth Pydantic models (`api/models/auth_models.py`)

```python
# api/models/auth_models.py
"""
Pydantic v2 schemas for authentication endpoints.
Produced by: backend-agent / supabase-auth skill
"""
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: int           # Unix timestamp
    user_id: str
    email: str


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    # Body is optional; relies on Bearer token in Authorization header
    pass
```

### Auth routes (`api/routes/auth.py`)

```python
# api/routes/auth.py
"""
Authentication endpoints — signup, login, logout, token refresh.
Produced by: backend-agent / supabase-auth skill
"""
from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client

from api.deps import get_current_user, get_db
from api.models.auth_models import AuthResponse, LoginRequest, RefreshRequest, SignupRequest

router = APIRouter(tags=["Authentication"])


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(data: SignupRequest, db: Client = Depends(get_db)) -> AuthResponse:
    """
    Register a new user. Supabase sends a confirmation email if email confirm is enabled.
    # SERVICE ROLE: bypasses RLS — required to create the auth.users record.
    """
    try:
        response = db.auth.sign_up({"email": data.email, "password": data.password})
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if response.user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Signup failed. Email may already be registered.",
        )

    # session is None when email confirmation is required
    if response.session is None:
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="Confirmation email sent. Please verify your email before logging in.",
        )

    return AuthResponse(
        access_token=response.session.access_token,
        refresh_token=response.session.refresh_token,
        expires_at=response.session.expires_at,
        user_id=str(response.user.id),
        email=response.user.email,
    )


@router.post("/login", response_model=AuthResponse)
async def login(data: LoginRequest, db: Client = Depends(get_db)) -> AuthResponse:
    """
    Authenticate with email and password. Returns JWT access + refresh tokens.
    # SERVICE ROLE: bypasses RLS — required for auth.sign_in_with_password.
    """
    try:
        response = db.auth.sign_in_with_password(
            {"email": data.email, "password": data.password}
        )
    except Exception as exc:
        # Supabase raises on invalid credentials — catch and return 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    if response.user is None or response.session is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login failed.")

    return AuthResponse(
        access_token=response.session.access_token,
        refresh_token=response.session.refresh_token,
        expires_at=response.session.expires_at,
        user_id=str(response.user.id),
        email=response.user.email,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db),
) -> None:
    """
    Invalidate the current session server-side.
    Client must also clear session_state auth keys.
    """
    try:
        # Sign out using the user's own JWT to invalidate only their session
        user_db = __import__(
            "services.supabase", fromlist=["get_user_supabase_client"]
        ).get_user_supabase_client(current_user["token"])
        user_db.auth.sign_out()
    except Exception:
        pass  # Always succeed — client clears state regardless


@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(
    data: RefreshRequest, db: Client = Depends(get_db)
) -> AuthResponse:
    """
    Exchange a refresh token for a new access token.
    # SERVICE ROLE: bypasses RLS — required for token refresh.
    """
    try:
        response = db.auth.refresh_session(data.refresh_token)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token.",
        ) from exc

    if response.session is None or response.user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh failed.")

    return AuthResponse(
        access_token=response.session.access_token,
        refresh_token=response.session.refresh_token,
        expires_at=response.session.expires_at,
        user_id=str(response.user.id),
        email=response.user.email,
    )
```

### `get_current_user` dependency (`api/deps.py`)

```python
# api/deps.py — already shown in fastapi-routes skill; reproduced here for auth context

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client

from services.supabase import get_supabase_client, get_user_supabase_client

security = HTTPBearer()


async def get_db() -> Client:
    # SERVICE ROLE: bypasses RLS — only for auth validation
    return get_supabase_client()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Client = Depends(get_db),
) -> dict:
    """Validates Bearer JWT via Supabase get_user. Raises 401 if invalid."""
    try:
        response = db.auth.get_user(credentials.credentials)
        if response.user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"user": response.user, "token": credentials.credentials}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


async def get_user_db(current_user: dict = Depends(get_current_user)) -> Client:
    """Returns user-scoped Supabase client; all queries respect RLS."""
    return get_user_supabase_client(current_user["token"])
```

### Streamlit session state — init (`utils/global_init.py` extension)

```python
# utils/global_init.py — extend init_session_state()
def init_session_state() -> bool:
    defaults = {
        "unit_system": "us",
        "auth_token": None,
        "auth_refresh_token": None,
        "auth_user": None,
        "auth_expires_at": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    return True
```

### Streamlit proactive token refresh helper

```python
# utils/auth_utils.py
"""
Client-side auth utilities — token expiry check and refresh.
Produced by: backend-agent / supabase-auth skill
"""
import time

import streamlit as st

from frontend.api_client import api_request


def is_token_expired() -> bool:
    """Returns True if auth_token is missing or within 60 seconds of expiry."""
    exp = st.session_state.get("auth_expires_at")
    if exp is None:
        return True
    return int(time.time()) >= exp - 60


def refresh_session_if_needed() -> bool:
    """
    Proactively refreshes the JWT if it is expired or close to expiry.
    Returns True if session is valid after the call; False if refresh failed.
    """
    if not is_token_expired():
        return True

    refresh_token = st.session_state.get("auth_refresh_token")
    if not refresh_token:
        return False

    result = api_request("POST", "/auth/refresh", json={"refresh_token": refresh_token})
    if result is None:
        # Refresh failed — force re-login
        for key in ("auth_token", "auth_refresh_token", "auth_user", "auth_expires_at"):
            st.session_state[key] = None
        return False

    st.session_state["auth_token"] = result["access_token"]
    st.session_state["auth_refresh_token"] = result["refresh_token"]
    st.session_state["auth_expires_at"] = result["expires_at"]
    return True
```

### RLS policy reference (SQL — for documentation, not generated code)

```sql
-- Enable RLS on the items table
ALTER TABLE items ENABLE ROW LEVEL SECURITY;

-- Users can only see their own rows
CREATE POLICY "items: select own" ON items
  FOR SELECT USING (auth.uid() = user_id);

-- Users can insert rows assigned to themselves
CREATE POLICY "items: insert own" ON items
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Users can update their own rows
CREATE POLICY "items: update own" ON items
  FOR UPDATE USING (auth.uid() = user_id);

-- Users can delete their own rows
CREATE POLICY "items: delete own" ON items
  FOR DELETE USING (auth.uid() = user_id);
```

## Anti-Patterns

- **Validating JWT locally with `python-jose` instead of calling `db.auth.get_user(jwt)`** — use Supabase validation to ensure revoked tokens are rejected.
- **Using the service-role key for user data queries** — bypasses RLS, creating a privilege escalation risk.
- **Storing `auth_token` in cookies or `localStorage` from Streamlit** — use `st.session_state` only; it is server-side.
- **Not clearing `auth_*` keys on logout** — stale token remains accessible in session.
- **Checking `response.error` (supabase-py v1)** — removed in v2; errors raise exceptions.
- **Sign-in inside a route handler without `get_db` dependency** — always use DI.
- **Skipping email validation** — use `pydantic.EmailStr` on signup/login models.

## Checklist

- [ ] `SignupRequest`, `LoginRequest`, `AuthResponse` present in `api/models/auth_models.py`
- [ ] Auth router registered in `register_routers()` with `prefix="/auth"` — NO `/api` prefix (external path `/api/auth/*` is applied by `Mount` in `asgi.py`)
- [ ] `get_current_user` dependency validates via `db.auth.get_user(jwt)`, not local decode
- [ ] Protected routes use `Depends(get_current_user)`
- [ ] User data routes use `Depends(get_user_db)` (RLS-respecting client)
- [ ] `auth_token`, `auth_refresh_token`, `auth_user`, `auth_expires_at` initialized in `init_session_state()`
- [ ] Login component calls `st.rerun(scope="app")` after success
- [ ] Logout clears all `auth_*` session state keys
- [ ] RLS policies exist in Supabase for every table accessed by user routes
- [ ] No service-role usage in user-facing query functions

## User Preferences

<!-- This section is updated during use. Start with defaults below. -->
- preferred_pattern: Supabase JWT validation via get_user dep
- style_overrides: {}
- avoid: []
- learned_corrections: []
- notes: []

### Self-Update Rules

1. When the user corrects output from this skill, append the correction to `learned_corrections` with date and context.
2. When the user expresses a preference, add it to `style_overrides`.
3. When a pattern causes an error traceable to a doc change, add the old pattern to `avoid` and update Patterns above.
4. Before generating any output, read the full User Preferences section and apply every entry.
5. After every 5 iterations, summarize `learned_corrections` into consolidated rules and prune resolved entries.
