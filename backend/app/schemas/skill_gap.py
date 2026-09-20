"""
Pydantic Schemas for Skill Gap Analysis System.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.learner_profile import SkillEvidence


class SkillGapItem(BaseModel):
    """Detailed gap analysis for a single target role skill requirement."""

    skill_name: str = Field(..., description="Normalized skill name (e.g., 'Statistics')")
    required_proficiency: str = Field(..., description="Required proficiency: 'Beginner', 'Intermediate', 'Advanced', 'Expert'")
    current_proficiency: str = Field(..., description="Current learner proficiency: 'No evidence', 'Beginner', 'Intermediate', 'Advanced', 'Expert'")
    gap_status: str = Field(..., description="Classification: 'strong', 'meets_requirement', 'needs_improvement', 'missing'")
    priority: str = Field(..., description="Deterministic priority: 'high', 'medium', 'low'")
    importance: str = Field("high", description="Role skill importance: 'high', 'medium', 'low'")
    reason: str = Field(..., description="Human-readable explanation of why this skill is needed and its current status")
    evidence: List[SkillEvidence] = Field(default_factory=list, description="Preserved evidence items backing learner capability")


class SkillGapBase(BaseModel):
    """Base fields for Skill Gap Analysis."""

    user_id: str = Field(..., description="Unique identifier of the learner")
    target_role: str = Field(..., description="Target career role (e.g., 'AI/ML Engineer')")
    analyzed_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    skills: List[SkillGapItem] = Field(default_factory=list, description="Detailed skill gap items")
    overall_readiness: float = Field(
        0.0,
        ge=0.0,
        le=100.0,
        description="Calculated readiness percentage matching role benchmark (0.0 to 100.0%)",
    )
    summary: str = Field(..., description="Executive summary of skill gap analysis")


class SkillGapResponse(SkillGapBase):
    """Response schema for returning a stored skill gap analysis."""

    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    model_config = ConfigDict(from_attributes=True)
