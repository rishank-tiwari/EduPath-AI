"""
Pydantic Schemas for EduPath Learning Activity & Progress Event System.
"""

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class LearningActivityCreate(BaseModel):
    """Payload for recording a learning activity event."""

    user_id: str = Field(..., description="Unique learner ID")
    activity_type: str = Field(
        ...,
        description="Event type: 'resource_started', 'resource_completed', 'practice_started', 'practice_completed', 'assessment_completed', 'project_started', 'project_completed', 'mentor_interaction', 'module_completed'",
    )
    activity_id: Optional[str] = Field(None, description="Unique activity ID or task ID")
    resource_id: Optional[str] = Field(None, description="Associated learning resource ID")
    skill_name: Optional[str] = Field(None, description="Associated technical skill name")
    topic: Optional[str] = Field(None, description="Specific learning topic")
    status: str = Field("completed", description="Status: 'started', 'in_progress', 'completed', 'failed'")
    score: Optional[float] = Field(None, ge=0.0, le=100.0, description="Quantitative score if applicable")
    completion_percentage: Optional[float] = Field(100.0, ge=0.0, le=100.0, description="Completion percentage")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context payload")


class LearningActivityRecord(LearningActivityCreate):
    """Persisted activity record schema."""

    record_id: str = Field(..., description="Unique MongoDB record ID")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
