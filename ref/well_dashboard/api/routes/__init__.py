"""
API Routes Package — Well Dashboard

Each module in this package is a self-contained FastAPI ``APIRouter``.
All routers are registered in ``api/main.py`` via ``register_routers()``.

Adding a new route group
-------------------------
1. Create ``api/routes/my_feature.py`` with an ``APIRouter`` named ``router``.
2. Import and register it inside ``register_routers()`` in this file.
3. That's it — the router will be mounted automatically.

Modules
-------
auth        User registration and login (JWT issuance)
projects    Project CRUD
wells       Well CRUD and status management
wellbore    Hole-section, casing, tubular, and survey sub-data
templates   Pre-built and custom well templates
export      Excel export and file download
dashboard   Aggregate stats and recent activity
agno        Placeholder for Agno AI agent routes (add as needed)
"""

from fastapi import FastAPI

from api.routes import auth, projects, wells, wellbore, templates, export, dashboard


def register_routers(app: FastAPI) -> None:
    """
    Mount every route module onto the FastAPI *app*.

    This is the single place to add/remove route groups.
    Called once at application startup from ``api/main.py``.
    """
    # Authentication — no auth dependency; issues tokens
    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

    # Core data resources — all protected by JWT (dependency defined per-router)
    app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
    app.include_router(wells.router, prefix="/api/wells", tags=["Wells"])
    app.include_router(wellbore.router, prefix="/api/wells", tags=["Well Sub-Data"])
    app.include_router(templates.router, prefix="/api/templates", tags=["Templates"])

    # Utility routes
    app.include_router(export.router, prefix="/api/export", tags=["Export"])
    app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])

    # ── Future route groups ────────────────────────────────────────────────────
    # Uncomment and implement as the project grows:
    #
    # from api.routes import agno
    # app.include_router(agno.router, prefix="/api/agno", tags=["Agno AI"])
    #
    # from api.routes import reports
    # app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
    #
    # from api.routes import notifications
    # app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
