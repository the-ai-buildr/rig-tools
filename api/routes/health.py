from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check() -> dict:
    return {"status": "ok", "service": "rig-tools-api"}
