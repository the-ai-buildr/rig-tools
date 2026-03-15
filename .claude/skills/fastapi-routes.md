# Skill: FastAPI Routes

<!--
Purpose: Patterns for FastAPI router/endpoint generation in Rig Tools.
Produced by: backend-agent
-->

## Purpose

Define every rule and pattern for creating FastAPI routers, endpoints, dependencies, and Pydantic models in this project.

## When to Use

Activate when the task contains: **endpoint**, **route**, **API**, **router**, **handler**, or when touching `api/routes/`, `api/deps.py`, `api/models/`, or `api/middleware.py`.

## Conventions

1. Every feature gets its own router module in `api/routes/{feature}.py`.
2. All routers are registered in `api/routes/__init__.py → register_routers()` — never directly in `api/main.py`.
3. Every endpoint uses a Pydantic request model for body params and a Pydantic response model for the return type.
4. The Supabase client is **always** injected via `Depends(get_db)` or `Depends(get_user_db)` — never instantiated in a handler.
5. All handlers are `async def`. DB functions in `api/db/` may be sync (supabase-py is sync by default); call them directly.
6. Route paths use kebab-case: `/kill-sheet`, not `/kill_sheet`.
7. Error handling: check `(data, error)` tuple; raise `HTTPException` if `error` is not None.
8. HTMX partial endpoints use `response_class=HTMLResponse` and live in `api/routes/partials.py`.
9. Auth endpoints live in `api/routes/auth.py`.
10. Prefix all routes with `/api` (enforced in `register_routers`).

## Patterns

### Router module

```python
# api/routes/items.py
"""
Items CRUD endpoints — create, read, update, delete items.
Produced by: backend-agent / fastapi-routes skill
"""
from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client

from api.deps import get_current_user, get_user_db
from api.db import items as items_db
from api.models.item_models import ItemCreate, ItemRead, ItemUpdate, ItemListResponse

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("", response_model=ItemListResponse)
async def list_items(
    db: Client = Depends(get_user_db),
    _user: dict = Depends(get_current_user),
) -> ItemListResponse:
    """Return all items visible to the authenticated user (respects RLS)."""
    data, error = items_db.read_items(db)
    if error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)
    return ItemListResponse(items=[ItemRead(**item) for item in data])


@router.get("/{item_id}", response_model=ItemRead)
async def get_item(
    item_id: str,
    db: Client = Depends(get_user_db),
    _user: dict = Depends(get_current_user),
) -> ItemRead:
    """Return a single item by ID."""
    data, error = items_db.read_item(db, item_id)
    if error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return ItemRead(**data)


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    payload: ItemCreate,
    db: Client = Depends(get_user_db),
    current_user: dict = Depends(get_current_user),
) -> ItemRead:
    """Create a new item owned by the authenticated user."""
    row = payload.model_dump()
    row["user_id"] = str(current_user["user"].id)
    data, error = items_db.create_item(db, row)
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return ItemRead(**data)


@router.patch("/{item_id}", response_model=ItemRead)
async def update_item(
    item_id: str,
    payload: ItemUpdate,
    db: Client = Depends(get_user_db),
    _user: dict = Depends(get_current_user),
) -> ItemRead:
    """Update item fields. Only provided fields are changed (partial update)."""
    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
    data, error = items_db.update_item(db, item_id, updates)
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return ItemRead(**data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: str,
    db: Client = Depends(get_user_db),
    _user: dict = Depends(get_current_user),
) -> None:
    """Delete an item by ID."""
    success, error = items_db.delete_item(db, item_id)
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
```

### Registering the router

```python
# api/routes/__init__.py
"""
Router registry — single mount point for all FastAPI routers.
Produced by: backend-agent / fastapi-routes skill
"""
from fastapi import FastAPI

from api.routes.health import router as health_router
from api.routes.calcs import router as calcs_router
from api.routes.auth import router as auth_router
from api.routes.items import router as items_router
# Import additional routers here


def register_routers(app: FastAPI) -> None:
    app.include_router(health_router, prefix="/api")
    app.include_router(calcs_router, prefix="/api/calcs", tags=["Calculations"])
    app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(items_router, prefix="/api", tags=["Items"])
    # Register additional routers here
```

### FastAPI dependencies (`api/deps.py`)

```python
# api/deps.py
"""
FastAPI dependency providers — Supabase clients and authenticated user.
Produced by: backend-agent / fastapi-routes skill
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client

from services.supabase import get_supabase_client, get_user_supabase_client

security = HTTPBearer()


async def get_db() -> Client:
    """
    Dependency: returns the service-role Supabase client.
    # SERVICE ROLE: bypasses RLS — use only for auth validation and admin operations.
    """
    return get_supabase_client()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Client = Depends(get_db),
) -> dict:
    """
    Dependency: validates the Bearer JWT via Supabase and returns the user.
    Raises 401 if the token is missing, expired, or invalid.
    """
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
    """
    Dependency: returns a Supabase client scoped to the authenticated user's JWT.
    All queries through this client respect Row-Level Security policies.
    """
    return get_user_supabase_client(current_user["token"])
```

### Pydantic models

```python
# api/models/item_models.py
"""
Pydantic v2 schemas for the items resource.
Produced by: backend-agent / fastapi-routes skill
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    quantity: int = Field(default=1, ge=0)
    description: Optional[str] = Field(default=None, max_length=500)


class ItemCreate(ItemBase):
    """Request schema for POST /items."""
    pass


class ItemUpdate(BaseModel):
    """Request schema for PATCH /items/{id} — all fields optional."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    quantity: Optional[int] = Field(default=None, ge=0)
    description: Optional[str] = Field(default=None, max_length=500)


class ItemRead(ItemBase):
    """Response schema for item endpoints."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class ItemListResponse(BaseModel):
    """Response schema for list endpoints."""
    items: list[ItemRead]
    count: int = 0

    def model_post_init(self, __context: object) -> None:
        self.count = len(self.items)
```

### CORS and error middleware (`api/middleware.py`)

```python
# api/middleware.py
"""
Middleware: CORS, global exception handler.
Produced by: backend-agent / fastapi-routes skill
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.config import settings


def add_middleware(app: FastAPI) -> None:
    """Register all middleware. Called from create_app() in api/main.py."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        # Log in production; return generic message to avoid leaking internals
        return JSONResponse(
            status_code=500,
            content={"detail": "An internal error occurred. Please try again."},
        )
```

## Anti-Patterns

- **Instantiating `supabase.create_client()` inside a route handler** — always use `Depends(get_db)` or `Depends(get_user_db)`.
- **Importing from `streamlit` in any `api/` module** — strict layer separation.
- **Using `response_model=dict`** — always use a named Pydantic model.
- **Putting auth logic in individual route handlers** — use `Depends(get_current_user)`.
- **snake_case route paths** — use kebab-case (`/kill-sheet`, not `/kill_sheet`).
- **`app.include_router` inside `api/main.py`** — all registration goes through `register_routers()`.
- **Catching bare `Exception` and returning 200** — always re-raise as a typed `HTTPException`.

## Checklist

- [ ] Router registered in `api/routes/__init__.py → register_routers()`
- [ ] Every endpoint has a `response_model` Pydantic class
- [ ] Every endpoint uses `Depends(get_db)` or `Depends(get_user_db)` — no inline client creation
- [ ] Protected endpoints use `Depends(get_current_user)`
- [ ] `(data, error)` tuple checked; errors raise `HTTPException`
- [ ] Route paths are kebab-case
- [ ] Pydantic models are in `api/models/{feature}_models.py`
- [ ] Module-level docstring present

## User Preferences

<!-- This section is updated during use. Start with defaults below. -->
- preferred_pattern: async def with Depends injection
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
