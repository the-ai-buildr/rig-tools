"""
Router registry — single mount point for all FastAPI routers.

ROUTE PREFIX NOTE: Routes here carry NO /api prefix. The Starlette Mount("/api", ...)
in asgi.py applies the /api prefix externally. This keeps FastAPI's internal
routing clean and allows standalone use without path duplication.

    register_routers →  /health          (external: /api/health)
    register_routers →  /calcs/*         (external: /api/calcs/*)
    register_routers →  /auth/*          (external: /api/auth/*  — future)

Produced by: backend-agent / fastapi-routes skill
"""
from fastapi import FastAPI

from api.routes.health import router as health_router
from api.routes.calcs import router as calcs_router


def register_routers(app: FastAPI) -> None:
    app.include_router(health_router)                                      # → /health
    app.include_router(calcs_router, prefix="/calcs", tags=["Calculations"])  # → /calcs/*
    # Add future routers here, e.g.:
    # app.include_router(auth_router, prefix="/auth", tags=["Authentication"])  # → /auth/*
    # app.include_router(items_router, tags=["Items"])                          # → /items/*
