# Rig Tools — Master Claude Context (Supabase Edition)

<!--
Purpose: Master system prompt — project conventions, architecture rules, and agent routing.
Produced by: orchestrator-agent
-->

## What This Project Is

**Rig Tools** is a drilling calculations platform built with Streamlit + FastAPI + Supabase.

- **Frontend:** Streamlit 1.55 (multipage, `st.fragment` for partial rerenders, HTMX for lightweight interactivity)
- **Backend API:** FastAPI 0.109 (separate Docker service on :8000, communicates over HTTP)
- **Database/Auth:** Supabase (PostgreSQL + Auth + Row-Level Security)
- **Deployment:** Docker Compose (`api` on :8000, `frontend` on :8501)
- **Desktop mode:** stlite/Electron — fully offline, calls `calcs/` directly with no HTTP

**Target users:** Operations Supervisors, Rig Managers, and Engineers.

### Two Deployment Modes

| Mode | Entry Point | Run command | Use Case |
|---|---|---|-|
| Single-process (default) | `asgi.py` via uvicorn | `uvicorn asgi:app` | Docker, local dev, desktop |
| Desktop (stlite/Electron) | `app.py` | `npm run serve` | Offline field use — calls `calcs/` directly |

In both non-Electron modes, `asgi.py` is the ASGI entry point. It composes:
- **Streamlit** — handles every path except `/api/*`
- **FastAPI** — mounted at `/api/*` via Starlette `Mount`

All endpoints are on **one port (8501)**. There is no separate `:8000` API service.

> In Electron/stlite mode, API calls go directly to `calcs/` functions — no HTTP, no FastAPI.

> **context7 note:** This file was generated without context7 MCP access. API signatures
> match supabase-py ≥2.3, Streamlit 1.33–1.55, FastAPI 0.109, HTMX 1.9.x.
> Re-verify `supabase.auth.*` call signatures if upgrading past supabase-py 3.0.

---

## Project Structure Convention

```
asgi.py                            # ASGI entry point: App("app.py", routes=[Mount("/api", app=fastapi_app)])
app.py                             # Streamlit script (called by App() — NOT run directly)
start.sh                           # Docker one-command startup

api/
├── main.py                        # FastAPI app factory (create_app), lifespan hooks
├── config.py                      # pydantic-settings: all env vars (NO hardcoded secrets)
├── deps.py                        # FastAPI dependencies: get_db, get_current_user, get_user_db
├── middleware.py                  # Auth middleware, CORS, error handlers
├── routes/
│   ├── __init__.py                # register_routers() — single mount point
│   ├── health.py                  # GET /api/health
│   ├── calcs.py                   # POST /api/calcs/* — existing drilling calc endpoints
│   ├── auth.py                    # POST /api/auth/signup|login|logout|refresh
│   └── {feature}.py              # One router module per feature
├── db/
│   └── {table_name}.py            # One file per Supabase table — create_, read_, update_, delete_
└── models/
    ├── __init__.py
    ├── calc_models.py             # Existing Pydantic calc schemas
    ├── auth_models.py             # SignupRequest, LoginRequest, AuthResponse
    └── {table_name}.py            # {Table}Create, {Table}Read, {Table}Update

frontend/
└── api_client.py                  # HTTP bridge: api_request(), auth wrappers, feature wrappers

services/
└── supabase.py                    # Supabase client singleton + per-user client factory

pages/
└── {NN}_{name}.py                 # Streamlit pages — UI shells only

components/
├── layout.py                      # Re-export hub for all UI primitives
├── nav.py                         # nav_menu(), page_nav()
├── page.py                        # page_header(), page_content()
├── sidebar.py                     # sidebar_header(), sidebar_content()
└── {feature}/
    └── {component_name}.py        # @st.fragment-decorated components per feature

calcs/
└── {module}.py                    # Pure Python math — no framework imports

styles/
└── style.py                       # apply_custom_css(), render_top_bar()

utils/
└── global_init.py                 # global_init(), init_session_state()

supabase/
├── config.toml                    # Supabase CLI project config (commit this)
├── seed.sql                       # Dev/test seed data only — no real user data
└── migrations/
    └── {YYYYMMDDHHMMSS}_{desc}.sql # One file per schema change — immutable once pushed
```

---

## Existing Components Reference

All reusable layout is in `components/layout.py` (re-export hub). Never duplicate layout in pages.

| Function | Module | Purpose |
|---|---|---|
| `page_header(title, icon)` | `components/page.py` | Renders nav + title + horizontal rule |
| `page_content(container)` | `components/page.py` | Returns/wraps main content container |
| `sidebar_header(title, icon)` | `components/sidebar.py` | Centered sidebar title |
| `sidebar_content(container)` | `components/sidebar.py` | Wraps sidebar content area |
| `nav_menu()` | `components/nav.py` | Popover with links to all pages |
| `page_nav(title, icon)` | `components/nav.py` | 80/20 columns — title left, nav right |
| `horizontal_rule()` | `components/utils.py` | Thin `<hr>` divider |
| `rig_stats()` | `components/metric_cards.py` | Home page rig stat cards |

## Existing API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/calcs/hydrostatic-pressure` | Hydrostatic pressure (psi) |
| `POST` | `/api/calcs/equivalent-mud-weight` | Equivalent mud weight (ppg) |
| `POST` | `/api/calcs/kill-sheet` | Kill sheet — kill mud weight |
| `POST` | `/api/calcs/annular-velocity` | Annular velocity (ft/min or m/min) |

- Swagger UI: `http://localhost:8000/docs`
- All calc endpoints accept `unit_system: "us" | "metric"`

## Agent Routing Table

| Task keyword | Agent | Skills loaded |
|---|---|---|
| page, view, layout, UI | frontend-agent | streamlit-pages, streamlit-components |
| component, fragment, widget | frontend-agent | streamlit-components, htmx-integration |
| endpoint, route, API | backend-agent | fastapi-routes, supabase-crud |
| auth, login, signup, session, JWT | backend-agent | supabase-auth, fastapi-routes |
| mount, wiring, main.py, single-process | backend-agent | fastapi-streamlit-mount |
| htmx, swap, partial | frontend-agent + backend-agent | htmx-integration, fastapi-routes |
| crud, database, table, query | backend-agent | supabase-crud, fastapi-routes |
| migration, schema, DDL, table, column, RLS, policy, index, seed, rollback | migration-agent | supabase-migration, supabase-crud |
| review, audit, lint, check, rls | reviewer-agent | all skills |

---

## Code Conventions

### Layer Rules (strict — never cross)

| Layer | Location | Allowed imports | Forbidden |
|---|---|---|---|
| UI | `pages/`, `components/` | `streamlit`, `frontend.api_client` | Supabase, FastAPI, `calcs/` |
| API Bridge | `frontend/api_client.py` | `httpx`, `streamlit.session_state` | Supabase, business logic |
| API Routes | `api/routes/` | FastAPI, Pydantic, `api/deps`, `api/db/` | Streamlit, direct Supabase calls |
| DB Layer | `api/db/` | `supabase.Client`, `services.supabase` | FastAPI, Streamlit |
| Services | `services/` | `supabase`, `config` | All framework layers |
| Calculations | `calcs/` | stdlib, numpy, scipy | Everything else |

### Non-Negotiable Rules

1. **Pages never call Supabase directly.** Flow: `page → component → api_client → FastAPI → api/db/*`
2. **Every FastAPI route uses Pydantic request/response models** from `api/models/`.
3. **Dependency injection for all clients** — never instantiate `supabase.Client` inside a route handler.
4. **`st.fragment` on any component that rerenders independently** from the rest of the page.
5. **All `api/db/` functions return `(data, error)` tuples** — never raise inside DB functions.
6. **All Supabase queries assume RLS is active.** If using service-role key, add comment: `# SERVICE ROLE: bypasses RLS — [reason]`.
7. **HTMX targets are FastAPI endpoints only** — never internal Streamlit routes.
8. **HTMX responses are HTML fragments** — never full HTML pages.
9. **One Supabase client per request type** — service-role via `get_db()`, user-scoped via `get_user_db()`.
10. **`global_init()` is called before any rendering** on every page.
11. **`config.py` is the only place credentials are read** — via env vars, never hardcoded.
12. **Module-level docstrings** on every generated file stating purpose and which skill/agent produced it.

### `api/db/` Function Signature Contract

```python
def create_{table}(client: Client, data: dict) -> tuple[dict | None, str | None]: ...
def read_{table}s(client: Client, filters: dict | None = None) -> tuple[list, str | None]: ...
def read_{table}(client: Client, record_id: str) -> tuple[dict | None, str | None]: ...
def update_{table}(client: Client, record_id: str, data: dict) -> tuple[dict | None, str | None]: ...
def delete_{table}(client: Client, record_id: str) -> tuple[bool, str | None]: ...
```

### `config.py` Extension for Supabase

Add to `api/config.py` `Settings` class:

```python
supabase_url: str = ""
supabase_anon_key: str = ""
supabase_service_role_key: str = ""
```

And to `docker/.env`:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

### All Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | *(must change)* | JWT / secrets signing key |
| `API_BASE_URL` | `http://localhost:8501` | Base URL for `api_client.py` HTTP calls — same port as app |
| `CORS_ORIGINS` | `["*"]` | Lock down to domain in production |
| `DEBUG` | `false` | Enable uvicorn reload |
| `DATA_PATH` | `/app/data` | Volume-mounted data directory |
| `SUPABASE_URL` | *(set in .env)* | Supabase project URL |
| `SUPABASE_ANON_KEY` | *(set in .env)* | Supabase anon/public key |
| `SUPABASE_SERVICE_ROLE_KEY` | *(set in .env)* | Supabase service-role key (never expose to browser) |
| `SUPABASE_DB_URL` | *(set in .env for CLI use)* | Direct Postgres URL for `supabase db push` / migration scripts |
| `SUPABASE_PROJECT_REF` | *(set in .env for CLI use)* | Project ref for `supabase link` |

**Note:** `API_BASE_URL` defaults to `http://localhost:8501` because FastAPI and Streamlit share the same port via `asgi.py`. No separate `:8000` service exists.

**Volume mount:** `./data:/app/data` — reference data and persistent files survive container restarts.

> Never commit `docker/.env` to git — it contains secrets.

---

## Quick-Start Commands

### Docker (recommended)

```bash
bash start.sh            # First run — builds image and starts service
bash start.sh --build    # Rebuild after dependency changes
bash start.sh --logs     # Follow logs
bash start.sh --down     # Stop service
```

```bash
cp docker/.env.example docker/.env
# Edit docker/.env — set SECRET_KEY and Supabase keys at minimum
```

### Local development (no Docker)

```bash
# Single command — Streamlit + FastAPI on :8501
uvicorn asgi:app --reload --port 8501

# Swagger UI
open http://localhost:8501/api/docs
```

### Desktop build (stlite + Electron)

```bash
npm install
npm run dump           # compile stlite artifacts
npm run serve          # launch Electron dev window
npm run app:dist:mac   # macOS .dmg
npm run app:dist:win   # Windows .exe
npm run app:dist:all   # all platforms
```

---

## Session State Keys

| Key | Type | Default | Description |
|---|---|---|---|
| `unit_system` | `str` | `"us"` | `"us"` or `"metric"` |
| `auth_token` | `str \| None` | `None` | Supabase JWT access token |
| `auth_refresh_token` | `str \| None` | `None` | Supabase refresh token |
| `auth_user` | `dict \| None` | `None` | Supabase user object |
| `auth_expires_at` | `int \| None` | `None` | JWT expiry (unix timestamp) |

Add per-feature keys with namespaced names: `{feature}_{key}` (e.g., `digital_stamp_rig`).

---

## Key Conventions

| Rule | Reason |
|---|---|
| Copy `pages/00_template.py` for new pages | Consistent structure |
| `calcs/` has no framework imports | Independently testable; reusable in both Desktop and Docker modes |
| `api/routes/` has no Streamlit imports | Clean layer separation |
| `frontend/api_client.py` is the only HTTP layer | Single place to change base URL / auth headers |
| Global CSS applied once via `global_init()` | Avoid repeated injection on every rerender |
| Docker files live in `docker/` | Clean root directory |
| Never commit `docker/.env` | Contains secrets |
| New pages added to `nav_menu()` | All navigation in one place |
| `@st.fragment` on independently-rerenable components | Avoid full-page rerun for partial updates |
| All schema changes go into `supabase/migrations/` | Never run DDL manually in the SQL editor |
| Never edit a migration file that has been pushed | Create a new migration to fix it |
| Every new table: `ENABLE ROW LEVEL SECURITY` + four policies | No table is ever unprotected |

---

## Dependency Versions

| Package | Version | Notes |
|---|---|---|
| `streamlit` | `1.55.0` | `st.fragment` stable since 1.33 |
| `fastapi` | `0.109.0` | |
| `pydantic` | `2.5.3` | v2 syntax throughout |
| `pydantic-settings` | `2.1.0` | |
| `httpx` | `0.26.0` | |
| `supabase` | `>=2.3.0` | Add to requirements.txt |
| `python-jose[cryptography]` | `>=3.3.0` | Add — for local JWT decode if needed |
| `gotrue` | pinned by supabase-py | Do not import directly |
| Supabase CLI | latest | `brew install supabase/tap/supabase` — for migrations only, not a Python dep |

---

## Migration Quick-Reference

```bash
supabase migration new {name}   # Create blank migration file
supabase db reset               # Replay all migrations locally (destructive)
supabase db push                # Push pending migrations to remote Supabase
supabase db diff -f {name}      # Generate migration SQL from schema diff
supabase migration list         # Show applied/pending status
```

All migration files live in `supabase/migrations/`. See `.claude/skills/supabase-migration.md` for full conventions.

---

## Skill Index

| Skill | File | When to Use |
|---|---|---|
| Streamlit Pages | `.claude/skills/streamlit-pages.md` | Creating/editing pages |
| Streamlit Components | `.claude/skills/streamlit-components.md` | Reusable UI, `st.fragment` |
| FastAPI Routes | `.claude/skills/fastapi-routes.md` | Endpoint generation |
| FastAPI+Streamlit Mount | `.claude/skills/fastapi-streamlit-mount.md` | Integration wiring |
| Supabase CRUD | `.claude/skills/supabase-crud.md` | `api/db/` functions |
| Supabase Auth | `.claude/skills/supabase-auth.md` | Auth flows, JWT, RLS |
| HTMX Integration | `.claude/skills/htmx-integration.md` | HTMX patterns |
| Rig Tools (legacy) | `.claude/skills/streamlit.md` | Existing page/component conventions |
