# Streamlit Development Skill — Rig Tools

You are helping build **Rig Tools**, a drilling calculations platform built with Streamlit + FastAPI. It runs as a single-process service — Streamlit + FastAPI on `:8501` via `uvicorn asgi:app` (Streamlit 1.53+ `starlette.App`).

> **⚠️ Architecture note (updated 2026-03):** This is a legacy reference skill. The project now uses
> `asgi.py` as the ASGI entry point — FastAPI is mounted at `/api/*` via `streamlit.starlette.App`.
> All patterns here still apply for UI; for FastAPI patterns see `fastapi-routes.md` and
> `fastapi-streamlit-mount.md`. Do NOT use two-service Docker or two-terminal local dev.

---

## Project Structure

```
app.py                         # Streamlit entry point
start.sh                       # One-command Docker startup

api/                           # FastAPI backend
  main.py                      # App factory (create_app), lifespan hooks
  config.py                    # Settings via pydantic-settings + .env
  routes/
    __init__.py                # register_routers()
    health.py                  # GET /api/health
    calcs.py                   # POST /api/calcs/* endpoints
  models/
    calc_models.py             # Pydantic request/response schemas

frontend/
  api_client.py                # HTTP client bridge (Streamlit → FastAPI)

pages/                         # Streamlit pages (numbered: 01_, 02_, …)
  00_template.py               # Copy this for new pages
components/
  comp_page_layout.py          # All reusable UI components
styles/
  style.py                     # apply_custom_css(), render_top_bar()
utils/
  global_init.py               # global_init() — called at startup on every page

calcs/                         # Pure Python math — no framework imports
data/                          # Reference data + persistent storage
docker/
  Dockerfile.api
  Dockerfile.frontend
  docker-compose.yml
  .env.example
```

---

## Pages

### Rules
- Every page lives in `pages/` and is numbered (`01_`, `02_`, …) to control sidebar order.
- Pages are **UI shells** — they call components and `api_client` wrappers, no raw math.
- Every page must call `global_init()` before any rendering.
- Always start a new page by copying `pages/00_template.py`.

### Page Anatomy
```python
import streamlit as st
from utils.global_init import global_init
from components.comp_page_layout import page_header, sidebar_header, sidebar_content, page_content
from frontend.api_client import calc_hydrostatic_pressure  # import relevant wrappers

st.set_page_config(page_title="Page Name", layout="wide", initial_sidebar_state="expanded")
global_init()

# --- Sidebar (inputs) ---
with st.sidebar:
    sidebar_header("Page Title", ":material/icon_name:")
    with sidebar_content(st.container()):
        depth = st.number_input("Depth (ft)", value=5000.0)
        mud_wt = st.number_input("Mud Weight (ppg)", value=10.5)

# --- Main (outputs) ---
page_header("Page Title", ":material/icon_name:")
with page_content(st.container()):
    result = calc_hydrostatic_pressure(mud_wt, depth)
    if result:
        st.metric("Hydrostatic Pressure", f"{result['pressure']:,.1f} psi")
```

### Adding a New Page
1. Copy `pages/00_template.py` → `pages/NN_<name>.py`
2. Add a link in `nav_menu()` in `components/comp_page_layout.py`
3. Add calculation logic in `calcs/<name>.py`
4. Add API endpoint in `api/routes/calcs.py` (or a new route file)
5. Add a convenience wrapper in `frontend/api_client.py`

---

## Components

All reusable UI lives in `components/comp_page_layout.py`. Never duplicate layout code in pages.

| Function | Usage |
|---|---|
| `page_header(title, icon)` | Full page header — applies CSS, nav, rule |
| `page_content(container)` | Wraps main content area |
| `sidebar_header(title, icon)` | Centered sidebar title |
| `sidebar_content(container)` | Wraps sidebar content |
| `nav_menu()` | Popover with links to all pages |
| `horizontal_rule()` | Lightweight `<hr>` divider |

Adding a component: add a stateless function to `comp_page_layout.py` — accept params, render or return.

---

## API Client (`frontend/api_client.py`)

The **only** place that makes HTTP calls. Pages import wrappers, never call `httpx` directly.

```python
# In a page:
from frontend.api_client import calc_kill_sheet

result = calc_kill_sheet(sidpp=200, current_mud_weight=10.5, depth=5000)
if result:
    st.metric("Kill Mud Weight", f"{result['kill_mud_weight_rounded']} ppg")
```

Adding a new wrapper:
```python
def calc_my_feature(param_a: float, param_b: float, unit_system: str = "us") -> dict | None:
    return api_request("POST", "/calcs/my-feature", json={
        "param_a": param_a,
        "param_b": param_b,
        "unit_system": unit_system,
    })
```

`API_BASE_URL` is read from env: defaults to `http://localhost:8501`. Same port as the app — FastAPI is mounted at `/api/*` on the same port via `asgi.py`. No separate service.

---

## FastAPI Backend (`api/`)

### App Factory (`api/main.py`)
```python
app = create_app()  # uvicorn api.main:app
```

### Adding a New Route Group
1. Create `api/routes/<feature>.py` with `router = APIRouter()`
2. Import and register in `api/routes/__init__.py`:
   ```python
   from .my_feature import router as my_feature_router
   # NO /api prefix — Mount("/api", ...) in asgi.py adds it externally
   app.include_router(my_feature_router, prefix="/my-feature", tags=["My Feature"])
   ```
3. Add Pydantic schemas to `api/models/<feature>_models.py`

### Endpoint Pattern
```python
from fastapi import APIRouter
from api.models.calc_models import MyRequest, MyResponse
import calcs.my_module as my_calc

router = APIRouter()

@router.post("/my-endpoint", response_model=MyResponse)
async def my_endpoint(req: MyRequest) -> MyResponse:
    result = my_calc.compute(req.value, req.unit_system)
    return MyResponse(result=result, unit_system=req.unit_system)
```

### Current Endpoints
| Method | Path | Description |
|---|---|---|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/calcs/hydrostatic-pressure` | HP from mud weight + depth |
| `POST` | `/api/calcs/equivalent-mud-weight` | EMW from pressure + depth |
| `POST` | `/api/calcs/kill-sheet` | Kill mud weight from SIDPP |
| `POST` | `/api/calcs/annular-velocity` | AV from flow rate + geometry |

All accept `unit_system: "us" | "metric"`. Docs at `http://localhost:8501/api/docs`.

---

## Calculations (`calcs/`)

Pure Python — **no Streamlit, no FastAPI imports**. Called by API routes only.

```python
# calcs/mud_weight.py
def hydrostatic_pressure(mud_weight: float, depth: float) -> float:
    """Returns pressure in psi. mud_weight in ppg, depth in ft."""
    return mud_weight * 0.052 * depth
```

Unit system is always a parameter, never global state.

---

## Styling

- `apply_custom_css()` is called once via `global_init()` — never call it per-page.
- Streamlit header/toolbar is hidden — use `render_top_bar()` for the custom top bar.
- Sidebar nav items are hidden — `nav_menu()` handles navigation.
- Scoped overrides: `st.markdown("<style>...</style>", unsafe_allow_html=True)`.
- Global styles: only via `styles/style.py > apply_custom_css()`.

---

## Session State

| Key | Default | Description |
|---|---|---|
| `unit_system` | `"us"` | `"us"` or `"metric"` |

Initialize in `global_init()`. Name per-feature keys with a prefix: `digital_stamp_rig`.

---

## Docker

### Start
```bash
bash start.sh            # build + start (first run)
bash start.sh --build    # rebuild after dep changes
bash start.sh --logs     # follow logs
bash start.sh --down     # stop
```

### Services
| Service | Port |
|---|---|
| `app` (Streamlit + FastAPI combined) | `8501` |

### Environment
```bash
cp docker/.env.example docker/.env
# Set SECRET_KEY before production use
```

Key variables:
- `SECRET_KEY` — must be changed for production
- `CORS_ORIGINS=["*"]` — restrict to domain in production
- `DEBUG=false` — set `true` for uvicorn reload
- `API_BASE_URL` — defaults to `http://localhost:8501`; override only if running behind a proxy

### Dockerfile locations
- `docker/Dockerfile.frontend` — combined Streamlit + FastAPI image (CMD: `uvicorn asgi:app`)
- `docker/docker-compose.yml` — single service orchestration
- `docker/.env.example` — environment template

---

## Local Development (no Docker)

```bash
# Single command — Streamlit + FastAPI on :8501
uvicorn asgi:app --reload --port 8501

# Swagger UI
open http://localhost:8501/api/docs
```

> **Do NOT use `streamlit run app.py` for local dev** — this starts Streamlit only and bypasses
> the FastAPI wiring in `asgi.py`. All `/api/*` calls will fail with connection errors.

---

## Key Conventions

| Rule | Reason |
|---|---|
| Copy `00_template.py` for new pages | Consistent structure |
| Pages import from `frontend/api_client.py`, not `httpx` | Single HTTP layer |
| `calcs/` has no framework imports | Independently testable; no framework coupling |
| `api/routes/` has no Streamlit imports | Clean separation |
| Docker files live in `docker/` | Clean root directory |
| Never commit `docker/.env` | Contains secrets |
| `requirements.txt` is minimal | Keeps the Docker image lean |
