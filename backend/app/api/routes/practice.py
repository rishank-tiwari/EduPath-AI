"""
FastAPI Route Endpoints for EduPath Practice Generation, Answer Evaluation & Results.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.core.database import DatabaseConnectionError
from app.schemas.practice import (
    PracticeResultRecord,
    PracticeSession,
    PracticeSubmissionRequest,
)
from app.services.practice_service import practice_service

router = APIRouter(prefix="/practice", tags=["Practice & Assessment"])


class PracticeGenerateRequest(BaseModel):
    """Payload schema for generating a new practice session."""

    user_id: str = Field(..., description="Learner user ID")
    task_id: Optional[str] = Field("task_default", description="Learning task ID")
    module_id: Optional[str] = Field(None, description="Associated module ID if launched from My Path")
    skill_name: Optional[str] = Field("General", description="Target skill name")
    skills: Optional[List[str]] = Field(None, description="List of improvement skills for general practice")
    difficulty: str = Field("beginner", description="Practice difficulty: 'beginner', 'intermediate', 'advanced'")
    practice_mode: str = Field(
        "general", description="Practice mode: 'general' (10 questions) or 'module' (5 questions)"
    )


@router.post(
    "/generate",
    response_model=PracticeSession,
    status_code=status.HTTP_200_OK,
    summary="Generate Practice Session",
    description="Generates a practice session (MCQ and Short Answer questions) aligned with a target learning task.",
)
def generate_practice(
    payload: PracticeGenerateRequest,
):
    """Generates a practice session for a learning task."""
    try:
        return practice_service.generate_practice(
            user_id=payload.user_id,
            task_id=payload.task_id or "task_default",
            skill_name=payload.skill_name or "General",
            difficulty=payload.difficulty,
            practice_mode=payload.practice_mode,
            module_id=payload.module_id,
            skills=payload.skills,
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
            detail=f"Failed to generate practice session: {str(e)}",
        )


@router.post(
    "/{practice_id}/submit",
    response_model=PracticeResultRecord,
    status_code=status.HTTP_200_OK,
    summary="Submit Practice Answers",
    description="Evaluates submitted practice answers, computes score & percentage, and stores result in MongoDB.",
)
def submit_practice(
    practice_id: str,
    payload: PracticeSubmissionRequest,
):
    """Submits practice answers for evaluation and persistence."""
    try:
        return practice_service.submit_practice(
            practice_id=practice_id,
            user_id=payload.user_id,
            answers=payload.answers,
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
            detail=f"Failed to evaluate practice submission: {str(e)}",
        )


@router.get(
    "/history",
    response_model=List[PracticeResultRecord],
    status_code=status.HTTP_200_OK,
    summary="Get Practice History",
    description="Retrieves a learner's previous practice evaluation results from MongoDB.",
)
def get_practice_history(
    user_id: str = Query(..., description="Target learner user ID"),
):
    """Retrieves practice result history for user_id."""
    try:
        return practice_service.get_user_history(user_id=user_id)
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
            detail=f"Failed to retrieve practice history: {str(e)}",
        )


@router.get(
    "/results/{identifier}",
    response_model=PracticeResultRecord,
    status_code=status.HTTP_200_OK,
    summary="Get Practice Result by ID",
    description="Retrieves a specific practice evaluation result by practice_id or result_id.",
)
def get_practice_result(
    identifier: str,
):
    """Retrieves a practice result record by practice_id or result_id."""
    try:
        return practice_service.get_result(identifier)
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
            detail=f"Failed to retrieve practice result: {str(e)}",
        )
