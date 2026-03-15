# Skill: FastAPI + Streamlit Mount

<!--
Purpose: Wiring patterns for the Streamlit+FastAPI single-process integration via streamlit.starlette.App.
Produced by: backend-agent
-->

## Purpose

Document the exact integration wiring between Streamlit and FastAPI using Streamlit 1.53+'s
built-in `streamlit.web.server.starlette.App` (also importable as `streamlit.starlette.App`).
Both run in one process on one port — no separate Docker services.

## When to Use

Activate when the task contains: **mount**, **wiring**, **asgi.py**, **single-process**, **ASGI**,
**integration point**, or when modifying `asgi.py`, `api/main.py`, `api/routes/__init__.py`, or
Docker service configuration.

## Conventions

1. **Primary mode: single-process via `asgi.py`.** Streamlit and FastAPI share port 8501. One uvicorn process, one Docker service.
2. `asgi.py` (project root) is the ASGI entry point — it creates `App("app.py", routes=[Mount("/api", app=fastapi_app)])`.
3. `app.py` is the Streamlit **script** — it is passed to `App()`, not run directly via `streamlit run`.
4. FastAPI routes inside `api/routes/` carry **no `/api` prefix** — the `Mount("/api", ...)` in `asgi.py` adds it externally.
5. `frontend/api_client.py` is the **only** file that calls FastAPI from Streamlit — default URL is `http://localhost:8501`.
6. `API_BASE_URL` env var overrides the default — same host/port as the app in all environments.
7. Streamlit's internal routes (`/_stcore/*`, `/media/*`, `/component/*`) are reserved and cannot be used by user routes.
8. User routes are evaluated **before** Streamlit's internal routes — FastAPI intercepts `/api/*` first.

> **Stability:** `streamlit.web.server.starlette.App` and `streamlit.starlette.App` are both
> available in Streamlit 1.53+. This is an official experimental API. Re-verify import path
> when upgrading past 1.55.

## Patterns

### Primary mode — single-process via `asgi.py` (Streamlit 1.53+ `App`)

**How data flows:**
```
User (browser :8501)
  → Starlette router
      → /api/*  →  FastAPI (Mount strips prefix: FastAPI sees /health, /calcs/*, etc.)
      → /*       →  Streamlit (app.py)
  ← JSON / HTML
```

**`asgi.py` (project root — ASGI entry point):**

```python
# asgi.py
"""
ASGI entry point — combines Streamlit + FastAPI in a single process on one port.
Uses Streamlit 1.53+ experimental starlette integration.

Run with:
    uvicorn asgi:app --host 0.0.0.0 --port 8501 [--reload]

Produced by: backend-agent / fastapi-streamlit-mount skill
"""
from starlette.routing import Mount
from streamlit.web.server.starlette import App   # also: from streamlit.starlette import App

from api.main import create_app

# FastAPI sub-app — routes have NO /api prefix (Mount adds it externally)
_api = create_app()

# User routes are prepended before Streamlit's internal routes (_stcore/*, media/*, etc.)
app = App(
    "app.py",                        # Streamlit script — resolved relative to cwd
    routes=[
        Mount("/api", app=_api),     # → /api/health, /api/calcs/*, /api/auth/*, etc.
    ],
)
```

**`App` constructor signature:**
```python
App(
    script_path: str,           # Path to Streamlit script
    *,
    lifespan=None,              # Optional asynccontextmanager lifespan
    routes=None,                # list[BaseRoute] — prepended before Streamlit routes
    middleware=None,            # list[Middleware]
    exception_handlers=None,    # dict[type, Callable]
    debug=False,
)
```

**Alternative — FastAPI-first (when FastAPI is the outer app):**
```python
# Use when FastAPI must be the primary ASGI app
streamlit_app = App("dashboard.py")
fastapi_app = FastAPI(lifespan=streamlit_app.lifespan())
fastapi_app.mount("/dashboard", streamlit_app)
```

---

### `api/routes/__init__.py` — no `/api` prefix

```python
# api/routes/__init__.py
"""
Router registry — routes have NO /api prefix here.
The Mount("/api", ...) in asgi.py applies the prefix externally.

Produced by: backend-agent / fastapi-routes skill
"""
from fastapi import FastAPI

from api.routes.health import router as health_router
from api.routes.calcs import router as calcs_router


def register_routers(app: FastAPI) -> None:
    app.include_router(health_router)                                         # /health  → external: /api/health
    app.include_router(calcs_router, prefix="/calcs", tags=["Calculations"])  # /calcs/* → external: /api/calcs/*
    # Add new routers here WITHOUT /api prefix:
    # app.include_router(auth_router, prefix="/auth", tags=["Auth"])
```

---

### `api/main.py` — factory (no changes needed for wiring)

```python
# api/main.py
"""
FastAPI application factory.
Produced by: backend-agent / fastapi-streamlit-mount skill
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.config import ensure_directories
from api.middleware import add_middleware
from api.routes import register_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_directories()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Rig Tools API",
        version="1.0.0",
        docs_url="/docs",      # External: /api/docs
        redoc_url="/redoc",    # External: /api/redoc
        lifespan=lifespan,
    )
    add_middleware(app)
    register_routers(app)
    return app


app = create_app()  # Retained for standalone uvicorn use: uvicorn api.main:app
```

---

### `frontend/api_client.py` — same-port default

```python
# frontend/api_client.py
"""
HTTP bridge between Streamlit and FastAPI — same process, same port.
Produced by: backend-agent / fastapi-streamlit-mount skill
"""
import os
from typing import Any

import httpx
import streamlit as st


def get_api_base_url() -> str:
    # Same host/port as the app — FastAPI is at /api/* on the same port
    return os.getenv("API_BASE_URL", "http://localhost:8501").rstrip("/")


def api_request(
    method: str,
    endpoint: str,
    token: str | None = None,
    **kwargs: Any,
) -> dict | None:
    url = f"{get_api_base_url()}/api{endpoint}"
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        detail = exc.response.json().get("detail", str(exc)) if exc.response.content else str(exc)
        st.error(f"API error {exc.response.status_code}: {detail}")
        return None
    except httpx.RequestError as exc:
        st.error(f"Could not reach API: {exc}")
        return None
```

---

### Docker (single service)

```yaml
# docker/docker-compose.yml
services:
  app:
    build:
      context: ..
      dockerfile: docker/Dockerfile.frontend
    ports:
      - "8501:8501"
    env_file: docker/.env
    volumes:
      - ../data:/app/data
```

```dockerfile
# docker/Dockerfile.frontend  (CMD runs uvicorn, not streamlit)
CMD ["uvicorn", "asgi:app", "--host", "0.0.0.0", "--port", "8501"]
```

---

### Adding Supabase env vars to Docker

```bash
# docker/.env  (add these lines)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

```python
# api/config.py  (extend Settings class)
class Settings(BaseSettings):
    # ... existing fields ...
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
```

## Reserved Prefixes

These paths are used by Streamlit internally — do NOT mount user routes at them:

| Prefix | Owner |
|--------|-------|
| `/_stcore/` | Streamlit core (WebSocket, health, metrics) |
| `/media/` | Streamlit media serving |
| `/component/` | Streamlit custom components |

`/api/` is safe to use for FastAPI.

## Anti-Patterns

- **Adding `/api` prefix in `api/routes/__init__.py`** — the Mount already adds it; double-prefix causes 404.
- **Running `streamlit run app.py` instead of `uvicorn asgi:app`** — bypasses `App()` wiring; FastAPI not served.
- **Hardcoding `http://localhost:8000` in `api_client.py`** — use `API_BASE_URL` env var (default is now `:8501`).
- **Importing `fastapi` in `app.py` or any Streamlit page** — strict layer separation.
- **Using subprocess/threading to run separate processes** — defeats single-process architecture.
- **Mounting at a reserved prefix** (`/_stcore/`, `/media/`, `/component/`) — will break Streamlit.
- **`app.mount("/", fastapi_app)` inside Streamlit** — wrong direction; `App()` wraps Streamlit, not the other way.
- **Calling `api_request` outside `frontend/api_client.py`** — all HTTP is funneled through this module.

## Checklist

- [ ] `asgi.py` exists at project root and imports `streamlit.web.server.starlette.App`
- [ ] `api/routes/__init__.py` has NO `/api` prefix on any `include_router` call
- [ ] `frontend/api_client.py` default URL is `http://localhost:8501`
- [ ] Docker CMD is `uvicorn asgi:app --host 0.0.0.0 --port 8501`
- [ ] Docker Compose has one service (no separate `api` service)
- [ ] `API_BASE_URL` is set via environment variable, never hardcoded
- [ ] `app.py` has no FastAPI imports
- [ ] `api/main.py` exports `app = create_app()`
- [ ] All HTTP calls from Streamlit go through `frontend/api_client.py`
- [ ] Supabase credentials added to `docker/.env` and `api/config.py`

## User Preferences

<!-- This section is updated during use. Start with defaults below. -->
- preferred_pattern: single-process Starlette App
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
