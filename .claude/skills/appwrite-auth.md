# Skill: Appwrite Auth

<!--
Purpose: Auth flows — signup, login, logout, session, JWT middleware, and permission wiring.
Produced by: backend-agent
-->

## Purpose

Define every rule and pattern for Appwrite authentication: signup/login/logout/session endpoints, JWT or session validation as a FastAPI dependency, session state management in Streamlit, and document-level permission wiring.

## When to Use

Activate when the task contains: **appwrite auth**, **account**, **login**, **signup**, **logout**, **session**, **JWT**, **token**, or when touching `api/routes/auth.py`, `api/models/auth_models.py`, `api/deps.py`, `components/auth/`, or `services/appwrite.py`.

## Conventions

1. Auth endpoints live exclusively in `api/routes/auth.py`.
2. Session/JWT validation is a FastAPI dependency (`get_current_user` in `api/deps.py`) — never inline in route handlers.
3. Streamlit stores auth state in `session_state`: `auth_token`, `auth_session_id`, `auth_user`, `auth_expires_at`. Init to `None` in `global_init()`.
4. `auth_token` is an Appwrite JWT; it is passed as `X-Appwrite-JWT: <token>` (or `Authorization: Bearer <token>` via custom middleware) to every protected API call.
5. The API key is **only** used for server-side admin operations and session validation — never exposed to the browser.
6. User data operations always use a client with `.set_jwt(jwt)` or `.set_session(session_id)` so Appwrite document permissions are enforced.
7. Login/signup components use `st.rerun(scope="app")` after a successful auth to apply auth-guard logic.
8. Logout clears all `auth_*` session state keys and calls the logout endpoint.
9. Token expiry: check `auth_expires_at` before making API calls and refresh proactively using `account.create_jwt()`.
10. Appwrite document permissions are the last line of defence; never rely on application-level filtering alone.

> **⚠️ appwrite-py v6+ auth note:**
> - `Account.create_email_password_session(email, password)` returns a `Session` object with `.id`, `.provider_access_token`, `.expire` (ISO string)
> - `Account.get_jwt()` returns a `Jwt` object with `.jwt` (the token string) — short-lived (15 min)
> - `Account.create_email_password_session` is the correct method name (not `create_session`)
> - `Account.delete_session(session_id)` invalidates a specific session
> - `Account.create()` registers a new user (`user_id`, `email`, `password`, `name`)
> - `Users.get(user_id)` (server-side, API key) validates that a user exists

## Patterns

### Appwrite Pydantic models (`api/models/auth_models.py`)

```python
# api/models/auth_models.py
"""
Pydantic v2 schemas for Appwrite authentication endpoints.
Produced by: backend-agent / appwrite-auth skill
"""
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    name: str = Field(..., min_length=1, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)


class AuthResponse(BaseModel):
    access_token: str          # Appwrite JWT (short-lived, 15 min)
    session_id: str            # Appwrite session ID (longer-lived)
    token_type: str = "bearer"
    expires_at: str            # ISO 8601 timestamp from session.expire
    user_id: str
    email: str
    name: str


class RefreshRequest(BaseModel):
    session_id: str            # Exchange existing session for a new JWT


class LogoutRequest(BaseModel):
    session_id: str
```

### Auth routes (`api/routes/auth.py`)

```python
# api/routes/auth.py
"""
Appwrite authentication endpoints — signup, login, logout, JWT refresh.
Produced by: backend-agent / appwrite-auth skill
"""
from appwrite.exception import AppwriteException
from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_appwrite_account, get_current_user
from api.models.auth_models import AuthResponse, LoginRequest, RefreshRequest, SignupRequest
from services.appwrite import get_appwrite_client

router = APIRouter(tags=["Authentication"])


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(data: SignupRequest) -> AuthResponse:
    """
    Register a new user and create an initial session + JWT.
    Uses server-side API key client to create the user account.
    """
    from appwrite.id import ID
    from appwrite.services.account import Account

    client = get_appwrite_client()  # API-key client
    account = Account(client)

    try:
        user = account.create(ID.unique(), data.email, data.password, data.name)
    except AppwriteException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message) from exc

    # Create session immediately after registration
    try:
        session = account.create_email_password_session(data.email, data.password)
        # Set session on client to get a JWT
        client.set_session(session.id)
        jwt_response = account.create_jwt()
    except AppwriteException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message) from exc

    return AuthResponse(
        access_token=jwt_response.jwt,
        session_id=session.id,
        expires_at=session.expire,
        user_id=user.id,
        email=user.email,
        name=user.name,
    )


@router.post("/login", response_model=AuthResponse)
async def login(data: LoginRequest) -> AuthResponse:
    """
    Authenticate with email and password. Returns JWT + session ID.
    """
    from appwrite.services.account import Account

    client = get_appwrite_client()
    account = Account(client)

    try:
        session = account.create_email_password_session(data.email, data.password)
        client.set_session(session.id)
        jwt_response = account.create_jwt()
        user = account.get()
    except AppwriteException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return AuthResponse(
        access_token=jwt_response.jwt,
        session_id=session.id,
        expires_at=session.expire,
        user_id=user.id,
        email=user.email,
        name=user.name,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    current_user: dict = Depends(get_current_user),
) -> None:
    """
    Invalidate the current Appwrite session server-side.
    Client must also clear session_state auth keys.
    """
    from appwrite.services.account import Account

    session_id = current_user.get("session_id", "current")
    try:
        client = get_appwrite_client()
        client.set_jwt(current_user["token"])
        account = Account(client)
        account.delete_session(session_id)
    except AppwriteException:
        pass  # Always succeed — client clears state regardless


@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(data: RefreshRequest) -> AuthResponse:
    """
    Exchange an existing session ID for a new short-lived JWT.
    """
    from appwrite.services.account import Account

    try:
        client = get_appwrite_client()
        client.set_session(data.session_id)
        account = Account(client)
        jwt_response = account.create_jwt()
        user = account.get()
        session = account.get_session(data.session_id)
    except AppwriteException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session.",
        ) from exc

    return AuthResponse(
        access_token=jwt_response.jwt,
        session_id=data.session_id,
        expires_at=session.expire,
        user_id=user.id,
        email=user.email,
        name=user.name,
    )
```

### `get_current_user` dependency (`api/deps.py`)

```python
# api/deps.py — Appwrite variant

from appwrite.exception import AppwriteException
from appwrite.services.account import Account
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from services.appwrite import get_appwrite_client

security = HTTPBearer()


async def get_appwrite_account():
    """Returns an Account service using the server-side API key client."""
    return Account(get_appwrite_client())


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Validates Bearer JWT via Appwrite Account.get(). Raises 401 if invalid."""
    try:
        client = get_appwrite_client()
        client.set_jwt(credentials.credentials)
        account = Account(client)
        user = account.get()
        return {
            "user": user,
            "user_id": user.id,
            "email": user.email,
            "name": user.name,
            "token": credentials.credentials,
        }
    except AppwriteException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
```

### Appwrite client singleton (`services/appwrite.py`)

```python
# services/appwrite.py
"""
Appwrite client factory — single source of truth for all client instances.
Produced by: backend-agent / appwrite-auth skill
"""
from functools import lru_cache

from appwrite.client import Client

from api.config import settings


@lru_cache(maxsize=1)
def get_appwrite_client() -> Client:
    """
    Returns a cached server-side Appwrite client using the API key.
    This client bypasses document-level permissions for admin operations.
    Per-request user-scoped clients should call get_user_appwrite_client().
    """
    if not settings.appwrite_endpoint or not settings.appwrite_project_id or not settings.appwrite_api_key:
        raise RuntimeError(
            "APPWRITE_ENDPOINT, APPWRITE_PROJECT_ID, and APPWRITE_API_KEY must be set."
        )
    client = Client()
    (
        client
        .set_endpoint(settings.appwrite_endpoint)
        .set_project(settings.appwrite_project_id)
        .set_key(settings.appwrite_api_key)
    )
    return client


def get_user_appwrite_client(jwt: str) -> Client:
    """
    Returns an Appwrite client scoped to the authenticated user's JWT.
    All document operations through this client respect Appwrite permissions.
    A new client object is created per request.
    """
    client = Client()
    (
        client
        .set_endpoint(settings.appwrite_endpoint)
        .set_project(settings.appwrite_project_id)
        .set_jwt(jwt)
    )
    return client
```

### `api/config.py` extension for Appwrite

```python
# api/config.py — add to Settings class
appwrite_endpoint: str = "https://cloud.appwrite.io/v1"
appwrite_project_id: str = ""
appwrite_api_key: str = ""
appwrite_database_id: str = ""   # Main database ID
```

And to `docker/.env`:

```
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your-project-id
APPWRITE_API_KEY=your-api-key
APPWRITE_DATABASE_ID=your-database-id
```

### Streamlit session state — init (`utils/global_init.py` extension)

```python
# utils/global_init.py — extend init_session_state()
def init_session_state() -> bool:
    defaults = {
        "unit_system": "us",
        "auth_token": None,         # Appwrite JWT (short-lived)
        "auth_session_id": None,    # Appwrite session ID (long-lived)
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
Client-side auth utilities — JWT expiry check and session-based refresh for Appwrite.
Produced by: backend-agent / appwrite-auth skill
"""
from datetime import datetime, timezone

import streamlit as st

from frontend.api_client import api_request


def is_token_expired() -> bool:
    """Returns True if auth_token is missing or within 60 seconds of expiry."""
    exp = st.session_state.get("auth_expires_at")
    if exp is None:
        return True
    try:
        # Appwrite expires_at is an ISO 8601 string
        expiry = datetime.fromisoformat(exp.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        return (expiry - now).total_seconds() < 60
    except (ValueError, TypeError):
        return True


def refresh_session_if_needed() -> bool:
    """
    Proactively refreshes the JWT using the long-lived session ID.
    Returns True if session is valid after the call; False if refresh failed.
    """
    if not is_token_expired():
        return True

    session_id = st.session_state.get("auth_session_id")
    if not session_id:
        return False

    result = api_request("POST", "/auth/refresh", json={"session_id": session_id})
    if result is None:
        for key in ("auth_token", "auth_session_id", "auth_user", "auth_expires_at"):
            st.session_state[key] = None
        return False

    st.session_state["auth_token"] = result["access_token"]
    st.session_state["auth_session_id"] = result["session_id"]
    st.session_state["auth_expires_at"] = result["expires_at"]
    return True
```

## Anti-Patterns

- **Validating JWT locally** — always call `account.get()` with the JWT set to let Appwrite validate it.
- **Using the API key client for user data document queries** — bypasses permissions; use `get_user_appwrite_client(jwt)`.
- **Storing `auth_token` or `session_id` in cookies/localStorage from Streamlit** — use `st.session_state` only.
- **Not clearing `auth_*` keys on logout** — stale token remains accessible in session.
- **Using `account.create_session()` (deprecated)** — use `account.create_email_password_session(email, password)`.
- **Using Appwrite client from `api/db/` without receiving it as a parameter** — always inject via DI.
- **Skipping email validation** — use `pydantic.EmailStr` on signup/login models.
- **Reusing the cached API key client across user requests without resetting JWT** — create a fresh client per user request via `get_user_appwrite_client()`.

## Checklist

- [ ] `SignupRequest`, `LoginRequest`, `AuthResponse` present in `api/models/auth_models.py`
- [ ] Auth router registered in `register_routers()` with `prefix="/auth"`
- [ ] `get_current_user` dependency validates via `account.get()` with JWT set — not local decode
- [ ] Protected routes use `Depends(get_current_user)`
- [ ] User data routes use `get_user_appwrite_client(jwt)` (permission-respecting client)
- [ ] `auth_token`, `auth_session_id`, `auth_user`, `auth_expires_at` initialized in `init_session_state()`
- [ ] Login component calls `st.rerun(scope="app")` after success
- [ ] Logout clears all `auth_*` session state keys and calls `account.delete_session()`
- [ ] Appwrite collection permissions exist for every collection accessed by user routes
- [ ] No API key usage in user-facing document query functions
- [ ] `APPWRITE_ENDPOINT`, `APPWRITE_PROJECT_ID`, `APPWRITE_API_KEY` set in `docker/.env` (not committed)

## User Preferences

<!-- This section is updated during use. Start with defaults below. -->
- preferred_pattern: Appwrite JWT validation via account.get() dep
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
