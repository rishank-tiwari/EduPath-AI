"""
FastAPI Route Endpoints for EduPath Personalized Learning Plans.
"""

from fastapi import APIRouter, HTTPException, Query, status
from app.core.database import DatabaseConnectionError
from app.schemas.learning_plan import LearningPlanResponse
from app.services.learning_plan_service import learning_plan_service

router = APIRouter(prefix="/plans", tags=["Learning Plans"])


@router.post(
    "/generate",
    response_model=LearningPlanResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Personalized Learning Plan",
    description="Generates an ordered, weekly, daily-task learning roadmap based on learner profile, skill gap analysis, and role prerequisites.",
)
async def generate_learning_plan(
    user_id: str = Query(..., description="Unique learner user ID"),
):
    """Generates and persists a personalized learning plan."""
    try:
        return await learning_plan_service.generate_plan(user_id=user_id)
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
            detail=f"Failed to generate learning plan: {str(e)}",
        )


@router.get(
    "",
    response_model=LearningPlanResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Latest Learning Plan",
    description="Retrieves the current/latest stored personalized learning plan for a learner.",
)
def get_learning_plan(
    user_id: str = Query(..., description="Unique learner user ID"),
):
    """Retrieves the latest learning plan for user_id."""
    try:
        return learning_plan_service.get_plan(user_id=user_id)
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
            detail=f"Failed to retrieve learning plan: {str(e)}",
        )


@router.get(
    "/{plan_id}",
    response_model=LearningPlanResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Learning Plan by ID",
    description="Retrieves a specific learning plan document by its unique plan_id.",
)
def get_learning_plan_by_id(
    plan_id: str,
):
    """Retrieves a specific learning plan by plan_id."""
    try:
        return learning_plan_service.get_plan_by_id(plan_id=plan_id)
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
            detail=f"Failed to retrieve learning plan by ID: {str(e)}",
        )
