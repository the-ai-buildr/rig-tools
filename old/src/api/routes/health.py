"""
Health check endpoint — validates that the API is reachable.
GET /health  (external: GET /api/health)

Produced by: backend-agent / fastapi-routes skill
"""
from fastapi import APIRouter
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str


router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", service="rig-tools-api")
