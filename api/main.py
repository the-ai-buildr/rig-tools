from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import settings, ensure_directories
from api.routes import register_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    ensure_directories()
    yield
    # Shutdown (add cleanup here if needed)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Rig Tools API",
        description="Drilling calculation engine for Rig Tools",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_routers(app)

    return app


app = create_app()
