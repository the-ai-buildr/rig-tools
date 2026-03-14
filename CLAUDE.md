# Rig Tools — Claude Code Context

## What This Project Is

**Rig Tools** is a drilling calculations platform built with Streamlit + FastAPI.

- **Desktop mode**: Packaged with [stlite](https://github.com/whitphx/stlite) (Streamlit + WebAssembly + Electron) — fully offline, no server required.
- **Server / Docker mode**: FastAPI backend + Streamlit frontend, orchestrated with Docker Compose.

Target users: Operations Supervisors, Rig Managers, and Engineers.

---

## Project Structure

```
app.py                         # Streamlit entry point (stlite + Docker)
start.sh                       # One-command Docker startup script
requirements.txt               # All Python dependencies

api/                           # FastAPI backend
  main.py                      # App factory (create_app), lifespan hooks
  config.py                    # Settings via pydantic-settings + .env
  routes/
    __init__.py                # register_routers() — single mount point
    health.py                  # GET /api/health
    calcs.py                   # POST /api/calcs/* — drilling calculation endpoints
  models/
    __init__.py
    calc_models.py             # Pydantic request/response schemas

frontend/                      # Streamlit → API bridge
  __init__.py
  api_client.py                # HTTP client (api_request, convenience wrappers)

pages/                         # Streamlit multipage pages
  00_template.py               # Template — copy for new pages
  01_home.py                   # Landing page
  02_digital_stamp.py          # Digital stamp tool

components/
  comp_page_layout.py          # All reusable UI components

styles/
  style.py                     # apply_custom_css(), render_top_bar()

utils/
  global_init.py               # global_init() — called at startup

calcs/                         # Pure Python calculation logic (no Streamlit, no FastAPI)
data/                          # Reference data + persistent storage (volume-mounted)
assets/                        # App icons and images

docker/
  Dockerfile.api               # FastAPI container
  Dockerfile.frontend          # Streamlit container
  docker-compose.yml           # Two-service orchestration
  .env.example                 # Environment variable template
  .env                         # Local secrets — NOT committed to git
```

---

## Architecture

### Two Deployment Modes

| Mode | Entry Point | API | Use Case |
|---|---|---|---|
| Desktop (stlite/Electron) | `app.py` | Inline `calcs/` | Offline field use |
| Server (Docker) | `app.py` via Docker | FastAPI on `:8000` | Multi-user / hosted |

### Separation of Concerns

| Layer | Location | Rule |
|---|---|---|
| **UI** | `pages/`, `components/` | Streamlit only — no business logic |
| **API Bridge** | `frontend/api_client.py` | HTTP only — no UI rendering |
| **API** | `api/routes/` | FastAPI only — no Streamlit imports |
| **Calculations** | `calcs/` | Pure Python — no framework imports |
| **Styling** | `styles/style.py` | CSS only — called once via `global_init()` |

### Communication Flow (Docker mode)

```
User (localhost:8501)
  → Streamlit page (pages/*.py)
  → frontend/api_client.py  →  POST http://api:8000/api/calcs/*
                             ←  JSON result
  → Render result in UI
```

---

## Pages

- Every page lives in `pages/` numbered with a two-digit prefix (`01_`, `02_`, …).
- Pages are **UI shells** — they call components and `api_client` wrappers, not raw math.
- Every page calls `global_init()` before any rendering.
- New pages start from `pages/00_template.py`.

### Adding a New Page
1. Copy `pages/00_template.py` → `pages/NN_<name>.py`
2. Add the link in `nav_menu()` inside `components/comp_page_layout.py`
3. Add calculation logic in `calcs/<name>.py` (pure Python)
4. Add API endpoint in `api/routes/calcs.py` (or a new route module)
5. Add a convenience wrapper in `frontend/api_client.py`

---

## Components

All reusable layout lives in `components/comp_page_layout.py`. Never duplicate layout code in pages.

| Function | Purpose |
|---|---|
| `page_header(title, icon)` | Full page header — applies CSS, renders nav, adds rule |
| `page_content(container)` | Wraps main content area |
| `sidebar_header(title, icon)` | Centered sidebar title |
| `sidebar_content(container)` | Wraps sidebar content area |
| `nav_menu()` | Popover with links to all pages |
| `horizontal_rule()` | Lightweight divider |

---

## FastAPI Backend

### Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/calcs/hydrostatic-pressure` | Hydrostatic pressure |
| `POST` | `/api/calcs/equivalent-mud-weight` | Equivalent mud weight |
| `POST` | `/api/calcs/kill-sheet` | Kill sheet (kill mud weight) |
| `POST` | `/api/calcs/annular-velocity` | Annular velocity |

- Docs available at `http://localhost:8000/docs` (Swagger UI)
- All calc endpoints accept `unit_system: "us" | "metric"`

### Adding a New Route Group
1. Create `api/routes/<feature>.py` with `router = APIRouter()`
2. Import and register in `api/routes/__init__.py > register_routers()`
3. Add Pydantic schemas to `api/models/<feature>_models.py`

---

## Calculations (`calcs/`)

- Pure Python functions — **no Streamlit, no FastAPI imports**
- Independently testable
- `calcs/` functions are called directly by API route handlers
- Unit system is a parameter — never global state

```python
# calcs/mud_weight.py
def hydrostatic_pressure(mud_weight: float, depth: float) -> float:
    """Returns pressure in psi. mud_weight in ppg, depth in ft."""
    return mud_weight * 0.052 * depth
```

---

## Session State

| Key | Type | Default | Description |
|---|---|---|---|
| `unit_system` | `str` | `"us"` | `"us"` or `"metric"` |

Add per-feature keys with feature-namespaced names (e.g., `digital_stamp_rig`).

---

## Docker

### Quick Start
```bash
bash start.sh            # First run (builds images)
bash start.sh --build    # Rebuild after dependency changes
bash start.sh --logs     # Follow logs
bash start.sh --down     # Stop everything
```

### Services
| Service | Port | Description |
|---|---|---|
| `api` | `8000` | FastAPI + uvicorn |
| `frontend` | `8501` | Streamlit |

### Environment
```bash
cp docker/.env.example docker/.env
# Edit docker/.env — set SECRET_KEY at minimum
```

### Key Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | *(must change)* | JWT / secrets signing key |
| `API_BASE_URL` | `http://api:8000` | Internal Docker hostname for frontend→API |
| `CORS_ORIGINS` | `["*"]` | Lock down to domain in production |
| `DEBUG` | `false` | Enable uvicorn reload |
| `DATA_PATH` | `/app/data` | Volume-mounted data directory |

### Volumes
- `./data:/app/data` — reference data and persistent files survive restarts

---

## Desktop Build (stlite + Electron)

```bash
npm install
npm run dump          # compile stlite artifacts
npm run serve         # launch Electron dev window
npm run app:dist:mac  # macOS .dmg
npm run app:dist:win  # Windows .exe
npm run app:dist:all  # all platforms
```

In Electron mode: API calls go to inline `calcs/` functions directly (no HTTP).

---

## Development (local, no Docker)

```bash
# Run Streamlit only
streamlit run app.py

# Run FastAPI only
uvicorn api.main:app --reload --port 8000

# Run both (separate terminals)
uvicorn api.main:app --reload --port 8000
API_BASE_URL=http://localhost:8000 streamlit run app.py
```

---

## Key Conventions

| Rule | Reason |
|---|---|
| Copy `00_template.py` for new pages | Consistent structure |
| `calcs/` has no framework imports | Independently testable, reusable in both modes |
| `api/routes/` has no Streamlit imports | Clean separation |
| `frontend/api_client.py` is the only HTTP layer | Single place to change base URL / auth |
| Global CSS applied once via `global_init()` | Avoid repeated injection |
| Docker files live in `docker/` | Clean root directory |
| Never commit `docker/.env` | Contains secrets |

---

## Skill

Use `/streamlit` (`.claude/skills/streamlit.md`) for guided assistance with page creation, components, API endpoints, and Docker deployment in this project.
