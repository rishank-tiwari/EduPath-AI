"""
Pydantic Schemas for EduPath Learning Resources & Resource Recommendation System.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class LearningResource(BaseModel):
    """Structured learning resource item (video, documentation, article, tutorial, course, project)."""

    resource_id: str = Field(..., description="Unique resource identifier (e.g., 'res_stat_01')")
    title: str = Field(..., description="Resource title (e.g., 'Khan Academy — Probability & Statistics')")
    description: str = Field(..., description="Short overview of what the resource teaches")
    resource_type: str = Field(
        ...,
        description="Type of resource: 'video', 'documentation', 'article', 'tutorial', 'course', 'project'",
    )
    url: str = Field(..., description="Direct authoritative URL or placeholder status")
    skill_name: str = Field(..., description="Normalized target skill name (e.g., 'Statistics')")
    difficulty: str = Field(
        "beginner",
        description="Target difficulty level: 'beginner', 'intermediate', 'advanced'",
    )
    estimated_minutes: int = Field(..., ge=5, description="Estimated duration to complete/read resource")
    source: str = Field(..., description="Publishing organization or platform (e.g., 'FastAPI Docs', 'PyTorch Tutorials')")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ResourceRecommendationRequest(BaseModel):
    """Payload schema for requesting resource recommendations for a learning task."""

    task_id: str = Field(..., description="Unique learning task identifier")
    skill_name: str = Field(..., description="Target skill name")
    difficulty: str = Field("beginner", description="Learner skill difficulty: 'beginner', 'intermediate', 'advanced'")
    user_id: Optional[str] = Field(None, description="Learner user ID")


class ResourceRecommendationResponse(BaseModel):
    """Response schema for returning recommended learning resources."""

    task_id: str = Field(..., description="Unique learning task identifier")
    skill_name: str = Field(..., description="Target skill name")
    topic: str = Field(..., description="Topic summary")
    resources: List[LearningResource] = Field(default_factory=list, description="Curated learning resources")

    model_config = ConfigDict(from_attributes=True)
