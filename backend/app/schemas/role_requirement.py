"""
Pydantic Schemas for Target Role Requirements & Skill Benchmarks.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class RoleSkillRequirement(BaseModel):
    """Configuration for a single skill requirement within a career role benchmark."""

    name: str = Field(..., description="Normalized skill name (e.g., 'Python', 'Machine Learning')")
    required_proficiency: str = Field(
        "Intermediate",
        description="Required proficiency level: 'Beginner', 'Intermediate', 'Advanced', 'Expert'",
    )
    importance: str = Field(
        "high",
        description="Importance weight: 'high', 'medium', or 'low'",
    )
    prerequisites: List[str] = Field(
        default_factory=list,
        description="Prerequisite skill names required before learning this skill",
    )


class RoleRequirement(BaseModel):
    """Complete requirement benchmark for a target career role."""

    role_name: str = Field(..., description="Name of the target role (e.g., 'AI/ML Engineer')")
    description: str = Field(..., description="Description of the role scope and industry expectations")
    required_skills: List[RoleSkillRequirement] = Field(
        default_factory=list,
        description="List of required skills and proficiency benchmarks",
    )
