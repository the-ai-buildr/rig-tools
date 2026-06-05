"""API package — registers FastAPI routers onto the Dash FastAPI backend."""
from __future__ import annotations


def register_api(app) -> None:
    """Initialize the database and mount REST routers on ``app.server``.

    Call this once from app.py after the Dash app is created.
    """
    from data.db import init_db
    from data.seed import seed_default_users
    from api.routes import projects, users, wells

    init_db()
    seed_default_users()

    server = app.server  # underlying FastAPI instance
    server.include_router(users.router)
    server.include_router(projects.router)
    server.include_router(wells.router)
