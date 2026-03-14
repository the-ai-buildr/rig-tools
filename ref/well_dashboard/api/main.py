"""
Well Dashboard API — Application Factory

This module creates the FastAPI application, wires up middleware, and registers
all route groups via ``api/routes/__init__.py``.

To add a new route group:
    1. Create api/routes/my_feature.py with an APIRouter named ``router``
    2. Import and register it in api/routes/__init__.py > register_routers()

Running locally (without Docker):
    uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
"""

from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import settings, ensure_directories
from api.database import Database
from api.routes import register_routers


# ── Database singleton shared across route modules ─────────────────────────────
db = Database()


# ── Application lifespan ───────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown hooks."""
    # Startup
    ensure_directories()
    await db.init_database()
    print("✅ Well Dashboard API started — database ready")
    yield
    # Shutdown
    await db.close()
    print("👋 Well Dashboard API stopped")


# ── App factory ────────────────────────────────────────────────────────────────

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Well Dashboard API",
        description=(
            "REST API for the Well Dashboard drilling project management system.\n\n"
            "**Authentication:** All endpoints (except /api/auth/login and /api/auth/register) "
            "require a Bearer token obtained from `POST /api/auth/login`.\n\n"
            "**Route Groups:**\n"
            "- `/api/auth` — Registration and login\n"
            "- `/api/projects` — Project CRUD\n"
            "- `/api/wells` — Well CRUD, status, and all sub-data\n"
            "- `/api/templates` — Pre-built and custom well templates\n"
            "- `/api/export` — Excel export and file download\n"
            "- `/api/dashboard` — Aggregate stats and recent activity\n"
        ),
        version="2.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ── CORS ───────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Route groups ───────────────────────────────────────────────────────────
    register_routers(app)

    # ── Utility endpoints ──────────────────────────────────────────────────────
    @app.get("/api/health", tags=["Health"])
    async def health_check():
        """Liveness probe — returns 200 when the API is ready to serve requests."""
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
        }

    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint — links to interactive documentation."""
        return {
            "message": "Well Dashboard API v2.0",
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/api/health",
        }

    return app


# ── Module-level app instance (used by uvicorn) ────────────────────────────────
app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )
