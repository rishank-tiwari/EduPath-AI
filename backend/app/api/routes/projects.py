"""
API Routes for Project Idea Generation.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from ai.agents.practice.project_agent import ProjectAgent
from app.repositories.profile_repository import profile_repository
from app.repositories.skill_gap_repository import skill_gap_repository

router = APIRouter(prefix="/projects", tags=["Project Generation"])


class ProjectGenerateRequest(BaseModel):
    user_id: str = Field("demo_user_1", description="Learner ID")
    target_role: Optional[str] = Field(None, description="Target role name")
    skill_gaps: Optional[List[str]] = Field(None, description="Target skill gaps to address")
    experience_level: Optional[str] = Field("Entry-Level", description="Experience level")


@router.post("/generate", status_code=status.HTTP_200_OK)
async def generate_projects(payload: ProjectGenerateRequest) -> Dict[str, Any]:
    """
    POST /api/v1/projects/generate
    Generates personalized project ideas based on target role, skill gaps, and experience level.
    """
    profile = profile_repository.get_by_user_id(payload.user_id) or {}
    gaps_doc = skill_gap_repository.get_by_user_id(payload.user_id) or {}

    target_role = payload.target_role or profile.get("target_role") or "AI/ML Engineer"
    experience_level = payload.experience_level or profile.get("experience_level") or "Entry-Level"

    gaps = payload.skill_gaps
    if not gaps:
        gaps = [s.get("skill_name") if isinstance(s, dict) else s for s in gaps_doc.get("skills_to_improve", [])]
        if not gaps:
            gaps = [s.get("skill_name") if isinstance(s, dict) else s for s in gaps_doc.get("missing_skills", [])]
    if not gaps:
        gaps = ["Statistics", "Model Evaluation", "MLOps"]

    agent = ProjectAgent()
    res = await agent.execute({
        "target_role": target_role,
        "skill_gaps": gaps,
        "experience_level": experience_level,
    })

    return res


@router.get("", status_code=status.HTTP_200_OK)
async def list_recommended_projects(user_id: str = "demo_user_1") -> Dict[str, Any]:
    """
    GET /api/v1/projects
    Retrieves recommended project proposals for user_id.
    """
    agent = ProjectAgent()
    res = await agent.execute({
        "user_id": user_id,
        "target_role": "AI/ML Engineer",
        "skill_gaps": ["Statistics", "Model Evaluation", "MLOps"],
    })
    return res
