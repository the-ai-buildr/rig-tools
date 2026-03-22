# Skills Index — Quick Reference for Orchestrator

<!--
Purpose: Compact summary of all skills — lets the orchestrator route tasks and check key rules
         without reading full skill files. Load this instead of individual skills at routing time.
         Full skill files are loaded by frontend-agent / backend-agent when implementing.
Produced by: orchestrator-agent
-->

---

## How to Use This Index

1. **Routing:** Match the user's task keywords against the Trigger column below to identify the required skill(s).
2. **Constraint check:** Use the Key Rules column to catch obvious violations before delegating.
3. **Deep implementation:** Tell the assigned agent to read the full skill file. Do not implement from this index alone.

---

## Skill Summary Table

| Skill | Full File | Trigger Keywords | Owner Agent |
|---|---|---|---|
| Streamlit Pages | `skills/streamlit-pages.md` | page, view, layout, UI, `pages/` | frontend-agent |
| Streamlit Components | `skills/streamlit-components.md` | component, fragment, widget, reusable, `st.fragment`, `components/` | frontend-agent |
| FastAPI Routes | `skills/fastapi-routes.md` | endpoint, route, API, router, handler, `api/routes/` | backend-agent |
| FastAPI+Streamlit Mount | `skills/fastapi-streamlit-mount.md` | mount, wiring, `main.py`, single-process, ASGI, Docker | backend-agent |
| Supabase CRUD | `skills/supabase-crud.md` | crud, database, table, query, supabase, `api/db/` | backend-agent |
| Supabase Auth | `skills/supabase-auth.md` | auth, login, signup, logout, session, JWT, token, RLS | backend-agent |
| Supabase Migration | `skills/supabase-migration.md` | migration, schema, DDL, table, column, alter, index, RLS policy, seed, rollback, `supabase db` | migration-agent |
| HTMX Integration | `skills/htmx-integration.md` | htmx, partial, swap, `hx-get`, `hx-post`, `hx-target`, `partials/` | both agents |
| Streamline | `skills/streamline.md` | design, layout, widget, chart, display, cache, performance, session state, dashboard, metric, badge, icon, theme | frontend-agent |
| Rig Tools (legacy) | `skills/streamlit.md` | existing page/component conventions, legacy patterns | frontend-agent |

---

## Key Rules Per Skill (Constraint Cheat-Sheet)

### Streamlit Pages
- `global_init()` is the first call — always, no exceptions.
- No `st.set_page_config` in page files — it lives in `app.py` only.
- Pages never import `supabase`, `fastapi`, or `calcs/` directly.
- Auth-gated pages redirect when `st.session_state.get("auth_token")` is `None`.
- New pages must be added to `nav_menu()` in `components/nav.py`.

### Streamlit Components
- Any component that rerenders independently **must** use `@st.fragment`.
- Static helpers (dividers, headers) must **not** use `@st.fragment`.
- `st.rerun(scope="fragment")` for self-contained updates; `scope="app"` only for full auth state change.
- Do not use `st.experimental_rerun()` (deprecated since 1.27).
- Never use `unsafe_allow_html=True` with user-supplied content.

### FastAPI Routes
- Every endpoint must have `response_model=` pointing to a named Pydantic class.
- All clients via `Depends(get_db)` or `Depends(get_user_db)` — no inline `create_client()`.
- Protected endpoints must have `Depends(get_current_user)`.
- Route paths are kebab-case: `/kill-sheet`, not `/kill_sheet`.
- All routers registered through `register_routers()` in `api/routes/__init__.py`.

### FastAPI+Streamlit Mount
- Primary architecture: **single-process** — `asgi.py` mounts FastAPI at `/api/*` via `streamlit.starlette.App`, all on port 8501.
- `API_BASE_URL` env var default is `http://localhost:8501` — never hardcode.
- FastAPI internal routes have **no `/api` prefix** — `Mount("/api", ...)` adds it externally.
- All Streamlit→FastAPI HTTP calls go through `frontend/api_client.py` only.

### Supabase Migration
- All schema changes go into `supabase/migrations/{YYYYMMDDHHMMSS}_{name}.sql` — never run DDL manually.
- Migration files are **immutable once pushed** — create a new file to correct.
- Every table migration must: enable RLS + create four owner-only policies (`auth.uid() = user_id`).
- All `CREATE`/`ALTER`/`DROP` use `IF NOT EXISTS` / `IF EXISTS` guards.
- Primary keys: always `uuid DEFAULT gen_random_uuid()` — never `serial`.
- Destructive changes (DROP COLUMN, type change) require a multi-step migration — always ask user first.

### Supabase CRUD
- One file per table: `api/db/{table}.py` — five functions: `create_`, `read_s`, `read_`, `update_`, `delete_`.
- All DB functions return `(data, error)` tuples — never raise out of `api/db/`.
- Single-row returns: `response.data[0] if response.data else None` (v2 returns a list, never raises).
- `services/supabase.py` is the **only** place `create_client()` is called.
- Service-role usage requires: `# SERVICE ROLE: bypasses RLS — [reason]` comment.

### Supabase Auth
- JWT validated via `db.auth.get_user(jwt)` in `get_current_user` dep — not local decode.
- User data queries use `get_user_db` (anon key + JWT) — never the service-role client.
- Auth endpoints only in `api/routes/auth.py`.
- Streamlit stores: `auth_token`, `auth_refresh_token`, `auth_user`, `auth_expires_at` in session_state.
- Login/signup components call `st.rerun(scope="app")` on success.
- Logout clears all `auth_*` keys.

### Streamline
- Use `st.container(border=True)` and `st.container(horizontal=True)` for KPI card layouts — not CSS hacks.
- Icons: `:material/icon_name:` (Material icons) everywhere — never emoji for UI elements.
- Use `st.segmented_control` instead of `st.radio(..., horizontal=True)`.
- `st.badge()` / `:green-badge[...]` for status indicators; `st.toast()` for transient confirmations.
- `@st.cache_data(ttl=...)` for data/DataFrames; `@st.cache_resource` for connections (never mutate).
- Cache keys that include user identity must use `st.session_state["auth_user"]["id"]` — no cross-user leakage.
- `st.set_page_config()` is called once in `app.py` — never in pages or components.
- Initialize session state with `st.session_state.setdefault(key, default)` — never overwrite on every run.

### HTMX Integration
- Partial endpoints live in `api/routes/partials.py`, prefix `/api/partials`.
- Every partial endpoint: `response_class=HTMLResponse` + `Depends(_require_htmx)`.
- HTMX fragments are plain HTML — no `<html>`, `<head>`, `<body>` wrappers.
- Auth token via `hx-headers='{"Authorization": "Bearer <token>"}'` — never query params.
- `hx-target` values must match real `id` attributes in the same HTML block.
- HTMX `<script>` tag embedded **once** per `st.html()` block — not once per loop/component call.

---

## Dependency Ordering (Fast Reference)

```
Pydantic models
    ↓
api/db/{table}.py  (CRUD functions)
    ↓
api/routes/{feature}.py  (FastAPI endpoints)  +  api/routes/partials.py (if HTMX needed)
    ↓
frontend/api_client.py  (HTTP wrappers)
    ↓
components/{feature}/  (@st.fragment components)
    ↓
pages/{NN}_{name}.py  (page shell)
    ↓
components/nav.py  (nav_menu registration)
```

---

## Critical Security Checks (Reviewer Fast-Path)

Before accepting any generated code, verify:

| # | Check | Severity |
|---|---|---|
| 1 | No `create_client()` outside `services/supabase.py` | CRITICAL |
| 2 | No `import supabase` in `pages/` or `components/` | CRITICAL |
| 3 | No hardcoded Supabase keys or `secret_key` defaults | CRITICAL |
| 4 | Service-role usage has `# SERVICE ROLE:` comment | CRITICAL |
| 5 | User-facing DB functions use `get_user_db` (not `get_db`) | CRITICAL |
| 6 | HTMX partials check `HX-Request: true` | WARNING |
| 7 | Auth token not in query params | CRITICAL |
| 8 | `unsafe_allow_html=True` not used on user-supplied content | CRITICAL |
| 9 | Every FastAPI endpoint has `response_model=` | WARNING |
| 10 | `(data, error)` tuple checked before using `data` | WARNING |
| 11 | Every new table has `ENABLE ROW LEVEL SECURITY` + 4 policies | CRITICAL |
| 12 | Migration files not edited after being pushed | CRITICAL |
| 13 | No `serial`/`bigint` primary keys — only `uuid` | WARNING |
