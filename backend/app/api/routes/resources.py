"""
FastAPI Route Endpoints for EduPath Resource Recommendations.
"""

from fastapi import APIRouter, HTTPException, status
from app.core.database import DatabaseConnectionError
from app.schemas.resource import (
    ResourceRecommendationRequest,
    ResourceRecommendationResponse,
)
from app.services.resource_service import resource_service

router = APIRouter(prefix="/resources", tags=["Resource Recommendations"])


@router.post(
    "/recommend",
    response_model=ResourceRecommendationResponse,
    status_code=status.HTTP_200_OK,
    summary="Recommend Resources for Task",
    description="Recommends curated learning resources (documentation, courses, videos, tutorials) matched to a learning task.",
)
async def recommend_resources(
    payload: ResourceRecommendationRequest,
):
    """Recommends curated resources matching task skill and difficulty."""
    try:
        return await resource_service.recommend_resources(
            task_id=payload.task_id,
            skill_name=payload.skill_name,
            difficulty=payload.difficulty,
            user_id=payload.user_id,
        )
    except HTTPException:
        raise
    except DatabaseConnectionError as db_err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database service unavailable: {str(db_err)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to recommend resources: {str(e)}",
        )
