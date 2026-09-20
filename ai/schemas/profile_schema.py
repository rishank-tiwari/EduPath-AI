"""
Pydantic Schemas for Profile Agent Structured Outputs.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.schemas.learner_profile import Certification, Education, Project, TechnicalSkill


class ProfileAnalysisInput(BaseModel):
    """Raw input container sent to Profile Agent for analysis."""

    user_id: str
    target_role: str
    career_goal: str
    raw_background: Optional[str] = None
    declared_skills: List[str] = Field(default_factory=list)
    declared_projects: List[Dict[str, Any]] = Field(default_factory=list)
    declared_education: List[Dict[str, Any]] = Field(default_factory=list)
    declared_certifications: List[Dict[str, Any]] = Field(default_factory=list)


class ProfileAnalysisResult(BaseModel):
    """Validated structured output produced by Profile Agent analysis."""

    user_id: str
    target_role: str
    career_goal: str
    inferred_experience_level: str = Field(
        "Entry-Level",
        description="Inferred level: 'Student', 'Entry-Level', 'Mid-Level', 'Senior', 'Lead'",
    )
    profile_summary: str = Field(..., description="Synthesized executive bio summary of candidate capabilities")
    technical_skills: List[TechnicalSkill] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    certifications: List[Certification] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    profile_completeness: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Score representing how completely the learner profile is documented",
    )
