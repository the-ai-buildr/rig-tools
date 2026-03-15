"""
ASGI entry point — combines Streamlit frontend + FastAPI backend in a single process.

Uses Streamlit 1.53+ experimental Starlette integration:
    streamlit.web.server.starlette.App

Architecture
------------
Streamlit's App class is an ASGI application that accepts user-defined Starlette
routes. User routes are evaluated BEFORE Streamlit's internal routes, so FastAPI
receives /api/* requests and Streamlit handles every other path — all on one port.

    /api/*          → FastAPI (mounted via starlette.routing.Mount)
    anything else   → Streamlit runtime (pages, WebSocket, static assets)

Run
---
    uvicorn asgi:app --host 0.0.0.0 --port 8501 [--reload]

Docker
------
    CMD ["uvicorn", "asgi:app", "--host", "0.0.0.0", "--port", "8501"]

Produced by: backend-agent / fastapi-streamlit-mount skill
"""
from starlette.routing import Mount

from streamlit.web.server.starlette import App

from api.main import create_app

# ── FastAPI sub-application ──────────────────────────────────────────────────
# Routes inside create_app() have NO /api prefix — the Mount below adds it.
# External URL:  GET /api/health  →  Mount strips /api  →  FastAPI sees GET /health
# External URL:  POST /api/calcs/kill-sheet  →  FastAPI sees POST /calcs/kill-sheet
_api = create_app()

# ── Combined ASGI app ────────────────────────────────────────────────────────
# App("app.py") resolves the script path relative to cwd when launched via uvicorn.
# Reserved Streamlit prefixes (/_stcore/, /media/, /component/) are not affected.
app = App(
    "app.py",
    routes=[
        Mount("/api", app=_api),
    ],
)
