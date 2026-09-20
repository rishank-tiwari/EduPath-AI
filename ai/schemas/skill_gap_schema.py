"""
Pydantic Schemas for Skill Gap Agent Structured Outputs.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.skill_gap import SkillGapItem


class SkillGapAnalysisInput(BaseModel):
    """Input payload container for Skill Gap Agent analysis."""

    user_id: str
    target_role: Optional[str] = None


class SkillGapAnalysisResult(BaseModel):
    """Validated structured output produced by Skill Gap Agent analysis."""

    user_id: str
    target_role: str
    analyzed_at: str
    skills: List[SkillGapItem] = Field(default_factory=list)
    overall_readiness: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Calculated readiness percentage matching role benchmark (0.0 to 100.0%)",
    )
    summary: str = Field(..., description="Executive summary of skill gap analysis")
