"""API package — registers FastAPI routers onto the Dash FastAPI backend."""
from __future__ import annotations


def register_api(app) -> None:
    """Mount REST routers on ``app.server`` and seed default users.

    Call this once from app.py after the Dash app is created.
    """
    from fastapi.responses import Response

    from data.seed import seed_default_users
    from api.routes import projects, settings, users, wells

    seed_default_users()

    server = app.server  # underlying FastAPI instance
    server.include_router(users.router)
    server.include_router(projects.router)
    server.include_router(wells.router)
    server.include_router(settings.router)

    # Dash's FastAPI backend only serves the index at "/", so deep links and
    # browser refreshes on client-side routes (e.g. /login, /home) 404. Add a
    # catch-all — registered last so API/Dash internal routes keep priority —
    # that returns the Dash index HTML and lets client-side routing take over.
    @server.get("/{full_path:path}", include_in_schema=False)
    async def serve_dash_index(full_path: str) -> Response:
        return Response(content=app.index(), media_type="text/html")
