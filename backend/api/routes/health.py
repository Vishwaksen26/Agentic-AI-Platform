from fastapi import APIRouter

from backend.core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "demo_mode": settings.demo_mode,
    }


@router.get("/ready")
async def readiness_check():
    return {"status": "ready"}