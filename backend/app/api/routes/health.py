"""
Health Check API Route for EduPath.
"""

from fastapi import APIRouter
from app.core.config import settings
from app.core.database import check_db_health

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check():
    """
    GET /api/v1/health
    Returns system status and database connectivity details.
    Safely catches any database connection exceptions to ensure system availability.
    """
    try:
        db_healthy = check_db_health()
    except Exception:
        db_healthy = False

    return {
        "status": "ok",
        "service": "EduPath API",
        "version": getattr(settings, "VERSION", "0.1.0"),
        "environment": getattr(settings, "ENVIRONMENT", "production"),
        "database": "connected" if db_healthy else "disconnected",
    }
