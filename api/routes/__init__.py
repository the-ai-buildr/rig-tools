from fastapi import FastAPI
from .health import router as health_router
from .calcs import router as calcs_router


def register_routers(app: FastAPI) -> None:
    app.include_router(health_router, prefix="/api")
    app.include_router(calcs_router, prefix="/api/calcs", tags=["Calculations"])
