"""
FastAPI Routes for Skill Gap Agent & Skill Gap Intelligence Analysis.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status
from app.core.database import DatabaseConnectionError
from app.schemas.skill_gap import SkillGapItem, SkillGapResponse
from app.services.skill_gap_service import skill_gap_service

router = APIRouter(prefix="/skill-gaps", tags=["Skill Gap Intelligence"])


@router.post("/analyze", response_model=SkillGapResponse)
async def analyze_skill_gaps(user_id: str = Query("demo_user_1", description="Learner User ID")):
    """
    POST /api/v1/skill-gaps/analyze
    Runs Skill Gap Agent analysis against stored Learner Profile for user_id,
    classifies gaps, calculates priorities, and persists structured analysis in MongoDB.
    """
    try:
        analysis = await skill_gap_service.analyze_and_save_gaps(user_id)
        return analysis
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        )
    except DatabaseConnectionError as err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database service unavailable: {str(err)}",
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Skill Gap Agent analysis failed: {str(err)}",
        )


@router.get("", response_model=SkillGapResponse)
async def get_skill_gap_analysis(user_id: str = Query("demo_user_1", description="Learner User ID")):
    """
    GET /api/v1/skill-gaps
    Retrieve latest stored skill gap analysis for a specific learner user_id.
    """
    try:
        analysis = skill_gap_service.get_analysis(user_id)
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Skill gap analysis for user_id '{user_id}' not found.",
            )
        return analysis
    except DatabaseConnectionError as err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database service unavailable: {str(err)}",
        )


@router.get("/{skill_name}", response_model=SkillGapItem)
async def get_single_skill_gap(
    skill_name: str,
    user_id: str = Query("demo_user_1", description="Learner User ID"),
):
    """
    GET /api/v1/skill-gaps/{skill_name}
    Retrieve skill gap analysis for a specific skill item.
    """
    try:
        item = skill_gap_service.get_skill_analysis(user_id, skill_name)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Skill gap item for '{skill_name}' under user_id '{user_id}' not found.",
            )
        return item
    except DatabaseConnectionError as err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database service unavailable: {str(err)}",
        )
