# Well Dashboard — Architecture Reference

> **Version:** 3.0 — Modular Route + Component Architecture  
> **Stack:** FastAPI · Streamlit · SQLite (aiosqlite) · Docker Compose

---

## Directory Structure

```
well_dashboard/
│
├── api/                        ← FastAPI backend package
│   ├── __init__.py
│   ├── main.py                 ← App factory + lifespan hooks
│   ├── config.py               ← Settings (env vars via pydantic-settings)
│   ├── auth.py                 ← JWT creation/verification + FastAPI dependency
│   ├── database.py             ← Async SQLite CRUD (aiosqlite)
│   ├── excel_export.py         ← Excel workbook generation (openpyxl/xlsxwriter)
│   │
│   ├── models/                 ← Pydantic request/response models
│   │   ├── __init__.py         ← Re-exports all models for easy importing
│   │   ├── auth_models.py      ← UserCreate, UserLogin, UserResponse
│   │   ├── project_models.py   ← ProjectCreate, ProjectResponse, ProjectUpdate
│   │   ├── well_models.py      ← WellCreate, WellResponse, WellUpdate, StatusUpdate
│   │   ├── wellbore_models.py  ← Wellbore, Casing, Tubular, Survey models
│   │   ├── template_models.py  ← TemplateCreate, TemplateResponse
│   │   └── export_models.py    ← ExportRequest, ExportResponse
│   │
│   └── routes/                 ← One APIRouter per feature domain
│       ├── __init__.py         ← register_routers(app) — the single mount point
│       ├── auth.py             ← POST /register, POST /login, GET /me
│       ├── projects.py         ← Project CRUD
│       ├── wells.py            ← Well CRUD + status transitions
│       ├── wellbore.py         ← Hole sections, casing, tubulars, surveys
│       ├── templates.py        ← Template CRUD
│       ├── export.py           ← Excel export + file download
│       └── dashboard.py        ← Stats aggregates, recent activity
│
├── frontend/                   ← Streamlit frontend package
│   ├── __init__.py
│   ├── main.py                 ← Entry point: streamlit run frontend/main.py
│   ├── api_client.py           ← Shared HTTP client (api_request, login, logout)
│   │
│   ├── pages/                  ← One module per top-level tab
│   │   ├── __init__.py
│   │   ├── projects.py         ← 📋 Projects tab
│   │   ├── well_data.py        ← 🔧 Well Data tab (largest page)
│   │   ├── templates.py        ← 📐 Templates tab
│   │   ├── reports.py          ← 📊 Reports tab
│   │   └── settings.py         ← ⚙️ Settings tab
│   │
│   └── components/             ← Reusable UI widgets
│       ├── __init__.py
│       ├── auth.py             ← Login form, logout button
│       ├── navigation.py       ← Top tab bar, sidebar
│       ├── status_badge.py     ← Coloured status label + selector
│       ├── data_table.py       ← Standardised dataframe renderer
│       ├── survey_chart.py     ← Plan vs Actual Plotly charts
│       └── well_form.py        ← Create-well form (shared by 2 pages)
│
├── db/                         ← SQLite database (volume-mounted, git-ignored)
├── exports/                    ← Generated Excel files (volume-mounted)
├── templates/                  ← Template JSON storage (volume-mounted)
│
├── docker-compose.yml          ← Two-service orchestration
├── Dockerfile.api              ← FastAPI container image
├── Dockerfile.frontend         ← Streamlit container image
├── requirements.txt            ← Python dependencies (shared)
└── start.sh                    ← One-command startup script
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         WELL DASHBOARD v3.0                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
              ┌─────────────────────┴──────────────────────┐
              ▼                                            ▼
┌─────────────────────────┐                  ┌─────────────────────────────┐
│   Streamlit Frontend    │                  │     FastAPI Backend         │
│   frontend/main.py      │◄────── HTTP ────►│     api/main.py             │
│   Port 8501             │     (httpx)      │     Port 8000               │
│                         │                  │                             │
│  pages/                 │                  │  routes/                    │
│  ├── projects.py        │                  │  ├── auth.py                │
│  ├── well_data.py       │                  │  ├── projects.py            │
│  ├── templates.py       │                  │  ├── wells.py               │
│  ├── reports.py         │                  │  ├── wellbore.py            │
│  └── settings.py        │                  │  ├── templates.py           │
│                         │                  │  ├── export.py              │
│  components/            │                  │  └── dashboard.py           │
│  ├── auth.py            │                  │                             │
│  ├── navigation.py      │                  │  models/                    │
│  ├── status_badge.py    │                  │  ├── auth_models.py         │
│  ├── data_table.py      │                  │  ├── project_models.py      │
│  ├── survey_chart.py    │                  │  ├── well_models.py         │
│  └── well_form.py       │                  │  ├── wellbore_models.py     │
│                         │                  │  ├── template_models.py     │
│  api_client.py          │                  │  └── export_models.py       │
└─────────────────────────┘                  └──────────────┬──────────────┘
                                                            │
                                               ┌────────────▼───────────┐
                                               │     SQLite Database     │
                                               │     (aiosqlite)         │
                                               │                         │
                                               │  users                  │
                                               │  projects               │
                                               │  wells                  │
                                               │  wellbore_details       │
                                               │  casing_strings         │
                                               │  tubular_strings        │
                                               │  directional_surveys    │
                                               │  templates              │
                                               │  status_history         │
                                               └─────────────────────────┘
```

---

## Route Groups

All routes are registered in `api/routes/__init__.py > register_routers()`.

| Prefix | Module | Description |
|--------|--------|-------------|
| `/api/auth` | `routes/auth.py` | Register, login, me |
| `/api/projects` | `routes/projects.py` | Project CRUD |
| `/api/wells` | `routes/wells.py` | Well CRUD + status |
| `/api/wells/{id}/...` | `routes/wellbore.py` | Hole sections, casing, tubulars, surveys |
| `/api/templates` | `routes/templates.py` | Template CRUD |
| `/api/export` | `routes/export.py` | Excel export + download |
| `/api/dashboard` | `routes/dashboard.py` | Stats, recent activity |
| `/api/health` | `api/main.py` | Liveness probe (inline) |

### Adding a New Route Group

```python
# 1. Create api/routes/my_feature.py
from fastapi import APIRouter, Depends
from api.auth import get_current_user

router = APIRouter()

@router.get("")
async def list_items(current_user: dict = Depends(get_current_user)):
    return []

# 2. Register in api/routes/__init__.py
from api.routes import my_feature
app.include_router(my_feature.router, prefix="/api/my-feature", tags=["My Feature"])
```

---

## Frontend Architecture

### Pages vs Components

| Type | Location | Rule |
|------|----------|------|
| **Page** | `frontend/pages/` | Renders a complete tab. One function per file. Never imported by another page. |
| **Component** | `frontend/components/` | A reusable widget. Can be imported by any page. Must have no required Streamlit state side-effects. |

### Adding a New Page

```python
# 1. Create frontend/pages/my_page.py
import streamlit as st

def my_page() -> None:
    st.markdown("### My New Page")
    ...

# 2. Add tab in frontend/components/navigation.py
TABS = [
    ...,
    ("🆕 My Page", "my_page"),
]

# 3. Wire in frontend/main.py
from frontend.pages.my_page import my_page

with tabs[5]:
    my_page()
```

### Adding a New Component

```python
# frontend/components/my_widget.py
import streamlit as st

def render_my_widget(data: list) -> None:
    """Render a reusable widget."""
    ...

# Use in any page:
from frontend.components.my_widget import render_my_widget
render_my_widget(some_data)
```

---

## Authentication Flow

```
Frontend (Streamlit)                  Backend (FastAPI)
        │                                    │
        │  POST /api/auth/login              │
        │  { username, password }            │
        ├───────────────────────────────────►│
        │                                    │  verify_password()
        │                                    │  create_access_token()
        │  { access_token, user }            │
        │◄───────────────────────────────────┤
        │                                    │
        │  (stored in st.session_state)      │
        │                                    │
        │  GET /api/projects                 │
        │  Authorization: Bearer <token>     │
        ├───────────────────────────────────►│
        │                                    │  verify_token()
        │                                    │  get_current_user() [Depends]
        │  [...projects...]                  │
        │◄───────────────────────────────────┤
```

---

## Models Architecture

Models are split by domain and re-exported from `api/models/__init__.py`:

```python
# Route modules import cleanly from the package:
from api.models import WellCreate, WellResponse, ProjectCreate

# Adding a new model group:
# 1. Create api/models/my_models.py with Pydantic classes
# 2. Import and add to __all__ in api/models/__init__.py
```

---

## Data Flow — Complete Well Fetch

```
GET /api/wells/{id}
        │
        ▼
routes/wells.py > get_well()
        │  Depends(get_current_user) verifies JWT
        │
        ▼
database.py > get_complete_well_data(well_id)
        │
        ├── get_well_by_id()
        ├── get_wellbore_sections(is_plan=True)
        ├── get_wellbore_sections(is_plan=False)
        ├── get_casing_strings(is_plan=True)
        ├── get_casing_strings(is_plan=False)
        ├── get_tubular_strings(is_plan=True)
        ├── get_tubular_strings(is_plan=False)
        ├── get_survey_points(survey_type="plan")
        ├── get_survey_points(survey_type="actual")
        └── _get_status_history()
        │
        ▼
WellResponse (Pydantic) → JSON → Streamlit
```

---

## Adding the Agno AI Route Group

When Agno integration is added, follow this pattern:

```python
# api/routes/agno.py
from fastapi import APIRouter, Depends
from api.auth import get_current_user

router = APIRouter()

@router.post("/chat")
async def agno_chat(
    message: str,
    well_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Send a message to an Agno AI agent with well context."""
    # Fetch well context from db, send to Agno, return response
    ...

@router.get("/agents")
async def list_agents(current_user: dict = Depends(get_current_user)):
    """Return available Agno agents."""
    ...
```

Then uncomment the registration in `api/routes/__init__.py`.

---

## Database Schema (ERD)

```
users ──────────────── projects ──────────────── wells
  id                     id                        id
  username               project_name              project_id  ──FK→ projects
  password_hash          project_type              well_name
  email                  created_by  ──FK→ users   current_status
                                                   ...
                                      │
              ┌───────────────────────┼──────────────────────────────────────┐
              ▼               ▼               ▼               ▼              ▼
      wellbore_details  casing_strings  tubular_strings  directional_  status_
                                                         surveys       history
         well_id             well_id        well_id       well_id      well_id
         section_name        string_name    string_name   md           old_status
         hole_size           casing_od      outer_diam    inclination  new_status
         is_plan             is_plan        is_plan       survey_type  changed_by
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_PATH` | `/app/db/well_database.db` | SQLite file path |
| `EXPORT_PATH` | `/app/exports` | Excel output directory |
| `TEMPLATE_PATH` | `/app/templates` | Template JSON storage |
| `SECRET_KEY` | *(change in prod)* | JWT signing key |
| `API_HOST` | `0.0.0.0` | FastAPI bind address |
| `API_PORT` | `8000` | FastAPI port |
| `DEBUG` | `false` | Enable uvicorn reload |
| `API_BASE_URL` | `http://localhost:8000` | Streamlit → API base URL |

---

## Migration Path to Supabase / PostgreSQL

The architecture is designed for a clean database layer swap:

1. **Replace `database.py`** with a Supabase client implementation preserving all method signatures.
2. **Replace `auth.py`** JWT with Supabase Auth (same `get_current_user` dependency interface).
3. **No route changes required** — routes call `db.*()` methods; the underlying implementation is swapped transparently.

```python
# Future database.py (Supabase)
from supabase import create_client

class Database:
    def __init__(self):
        self.client = create_client(SUPABASE_URL, SUPABASE_KEY)

    async def get_project_by_id(self, project_id: int) -> Optional[Dict]:
        result = self.client.table("projects").select("*").eq("id", project_id).execute()
        return result.data[0] if result.data else None
    # ... same interface, different implementation
```
