"""
FastAPI Route Endpoints for EduPath Adaptation Agent & Decision History.
"""

from typing import List
from fastapi import APIRouter, HTTPException, Query, status

from app.core.database import DatabaseConnectionError
from app.schemas.adaptation import (
    AdaptationAnalyzeRequest,
    AdaptationDecision,
)
from app.services.adaptation_service import adaptation_service

router = APIRouter(prefix="/adaptation", tags=["Adaptive Learning Engine"])


@router.post(
    "/analyze",
    response_model=AdaptationDecision,
    status_code=status.HTTP_200_OK,
    summary="Analyze Performance & Adapt Plan",
    description="Analyzes learner progress, applies adaptation rules, modifies learning plan, and increments plan version.",
)
async def analyze_and_adapt_plan(
    payload: AdaptationAnalyzeRequest,
):
    """Triggers performance analysis and plan adaptation."""
    try:
        return await adaptation_service.analyze_and_adapt(
            user_id=payload.user_id,
            skill_name=payload.skill_name,
            topic=payload.topic,
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
            detail=f"Failed to analyze and adapt learning plan: {str(e)}",
        )


@router.get(
    "/history",
    response_model=List[AdaptationDecision],
    status_code=status.HTTP_200_OK,
    summary="Get Adaptation History",
    description="Retrieves a learner's previous adaptation decisions and plan version history.",
)
def get_adaptation_history(
    user_id: str = Query(..., description="Target learner user ID"),
):
    """Retrieves adaptation history records for user_id."""
    try:
        return adaptation_service.get_user_adaptation_history(user_id=user_id)
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
            detail=f"Failed to retrieve adaptation history: {str(e)}",
        )
