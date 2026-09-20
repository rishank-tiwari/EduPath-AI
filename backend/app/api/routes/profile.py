"""
FastAPI Routes for Learner Profile & Profile Agent Analysis.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from ai.schemas.profile_schema import ProfileAnalysisInput
from app.core.database import DatabaseConnectionError
from app.repositories.profile_repository import profile_repository
from app.schemas.learner_profile import LearnerProfileCreate, LearnerProfileResponse
from app.services.profile_service import profile_service

router = APIRouter(prefix="/profile", tags=["Learner Profile"])


@router.post("", response_model=LearnerProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_or_update_profile(payload: LearnerProfileCreate):
    """
    POST /api/v1/profile
    Create or update a learner profile document in MongoDB.
    """
    try:
        saved_profile = profile_service.save_profile(payload)
        return saved_profile
    except DatabaseConnectionError as err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database service unavailable: {str(err)}",
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save profile: {str(err)}",
        )


@router.get("", response_model=LearnerProfileResponse)
async def get_profile(user_id: str = Query("demo_user_1", description="Learner User ID")):
    """
    GET /api/v1/profile
    Retrieve stored profile for a specific learner user_id from MongoDB.
    """
    try:
        profile = profile_service.get_profile(user_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Learner profile for user_id '{user_id}' not found.",
            )
        return profile
    except DatabaseConnectionError as err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE if hasattr(status, 'HTTP_503_SERVICE_UNAVAILABLE') else 503,
            detail=f"Database service unavailable: {str(err)}",
        )


@router.get("/evidence", status_code=status.HTTP_200_OK)
async def get_profile_evidence(user_id: str = Query("demo_user_1", description="Learner User ID")) -> Dict[str, Any]:
    """
    GET /api/v1/profile/evidence
    Retrieves evidence-backed skills, confidence scores, evidence snippets,
    and profile completeness for user_id.
    """
    profile = profile_repository.get_by_user_id(user_id)
    if not profile:
        return {
            "user_id": user_id,
            "target_role": "AI/ML Engineer",
            "profile_completeness": 0.0,
            "total_skills": 0,
            "evidence_cards": [],
            "projects": [],
        }

    technical_skills = profile.get("technical_skills", [])
    evidence_cards = []

    for sk in technical_skills:
        if isinstance(sk, dict):
            s_name = sk.get("name")
            s_conf = sk.get("confidence", 0.5)
            s_src = sk.get("source", "self_declared")
            s_ev = sk.get("evidence", [])
            evidence_cards.append({
                "skill_name": s_name,
                "source": s_src,
                "confidence": s_conf,
                "proficiency": sk.get("proficiency", "Intermediate"),
                "evidence_count": len(s_ev),
                "evidence": s_ev,
                "verified": sk.get("verified", True),
            })

    return {
        "user_id": user_id,
        "target_role": profile.get("target_role", "AI/ML Engineer"),
        "profile_completeness": profile.get("profile_completeness", 85.0),
        "total_skills": len(evidence_cards),
        "evidence_cards": evidence_cards,
        "projects": profile.get("projects", []),
    }


@router.post("/analyze", response_model=LearnerProfileResponse)
async def analyze_profile(payload: ProfileAnalysisInput):
    """
    POST /api/v1/profile/analyze
    Run Profile Agent analysis against input background data, compute evidence-backed skills,
    and persist the resulting structured LearnerProfile in MongoDB.
    """
    try:
        analyzed_profile = await profile_service.analyze_and_save_profile(payload)
        return analyzed_profile
    except DatabaseConnectionError as err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE if hasattr(status, 'HTTP_503_SERVICE_UNAVAILABLE') else 503,
            detail=f"Database service unavailable: {str(err)}",
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profile Agent analysis failed: {str(err)}",
        )
