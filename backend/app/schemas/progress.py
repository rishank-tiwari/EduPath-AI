"""
Pydantic Schemas for EduPath Progress Agent, Performance Summaries & Progress Events.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ProgressSummary(BaseModel):
    """Structured progress summary for a specific skill and topic."""

    progress_id: str = Field(..., description="Unique progress record ID (e.g., 'prog_stat_01')")
    user_id: str = Field(..., description="Learner user ID")
    skill_name: str = Field(..., description="Target skill name")
    topic: str = Field(..., description="Specific topic name")
    total_attempts: int = Field(0, ge=0, description="Total practice attempts recorded")
    total_questions: int = Field(0, ge=0, description="Total questions attempted")
    correct_answers: int = Field(0, ge=0, description="Total correct answers achieved")
    average_score: float = Field(0.0, ge=0.0, le=100.0, description="Average percentage score")
    latest_score: float = Field(0.0, ge=0.0, le=100.0, description="Most recent practice percentage score")
    performance_status: str = Field(
        "on_track",
        description="Performance status: 'strong', 'on_track', 'needs_review', or 'struggling'",
    )
    trend: str = Field(
        "insufficient_data",
        description="Performance trend: 'improving', 'stable', 'declining', or 'insufficient_data'",
    )
    last_activity_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ProgressEvent(BaseModel):
    """Event log record for learner actions and milestone progression."""

    event_id: str = Field(..., description="Unique progress event ID")
    user_id: str = Field(..., description="Learner user ID")
    event_type: str = Field(
        ...,
        description="Event type: 'practice_completed', 'practice_result', 'task_completed', 'plan_updated'",
    )
    skill_name: str = Field(..., description="Associated skill name")
    topic: str = Field(..., description="Associated topic name")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional structured event details")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class SkillProgressSummary(BaseModel):
    """Aggregated progress summary for a single skill containing topic breakdowns."""

    skill_name: str = Field(..., description="Skill name")
    overall_status: str = Field("on_track", description="Aggregated skill status")
    average_score: float = Field(0.0, ge=0.0, le=100.0)
    topics: List[ProgressSummary] = Field(default_factory=list)


class ProgressRecordRequest(BaseModel):
    """Payload schema for manually recording a progress event."""

    user_id: str = Field(...)
    event_type: str = Field(...)
    skill_name: str = Field(...)
    topic: str = Field(...)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)
