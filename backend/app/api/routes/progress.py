"""
FastAPI Route Endpoints for EduPath Progress Agent & Progress Event Tracking.
"""

from typing import List
from fastapi import APIRouter, HTTPException, Query, status

from app.core.database import DatabaseConnectionError
from app.schemas.progress import (
    ProgressEvent,
    ProgressRecordRequest,
    ProgressSummary,
    SkillProgressSummary,
)
from app.services.progress_service import progress_service

router = APIRouter(prefix="/progress", tags=["Progress Tracking"])


@router.post(
    "/record",
    response_model=ProgressEvent,
    status_code=status.HTTP_200_OK,
    summary="Record Progress Event",
    description="Records a new learning or practice progress event log.",
)
def record_progress_event(
    payload: ProgressRecordRequest,
):
    """Records a progress event in MongoDB."""
    try:
        return progress_service.record_event(
            user_id=payload.user_id,
            event_type=payload.event_type,
            skill_name=payload.skill_name,
            topic=payload.topic,
            metadata=payload.metadata,
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
            detail=f"Failed to record progress event: {str(e)}",
        )


@router.get(
    "",
    response_model=List[ProgressSummary],
    status_code=status.HTTP_200_OK,
    summary="Get User Progress Summary",
    description="Retrieves learner progress summaries across skills and topics.",
)
def get_user_progress(
    user_id: str = Query(..., description="Target learner user ID"),
):
    """Retrieves progress summary records for user_id."""
    try:
        return progress_service.get_user_progress(user_id=user_id)
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
            detail=f"Failed to retrieve user progress: {str(e)}",
        )


@router.get(
    "/skills",
    response_model=List[SkillProgressSummary],
    status_code=status.HTTP_200_OK,
    summary="Get Skill Progress Grouped",
    description="Retrieves progress summaries grouped by skill.",
)
def get_skill_progress(
    user_id: str = Query(..., description="Target learner user ID"),
):
    """Retrieves progress grouped by skill for user_id."""
    try:
        return progress_service.get_skill_progress(user_id=user_id)
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
            detail=f"Failed to retrieve skill progress: {str(e)}",
        )


@router.get(
    "/history",
    response_model=List[ProgressEvent],
    status_code=status.HTTP_200_OK,
    summary="Get Progress Event History",
    description="Retrieves progress event logs for a learner.",
)
def get_progress_history(
    user_id: str = Query(..., description="Target learner user ID"),
):
    """Retrieves progress event history for user_id."""
    try:
        return progress_service.get_event_history(user_id=user_id)
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
            detail=f"Failed to retrieve progress event history: {str(e)}",
        )
