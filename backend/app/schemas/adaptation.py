"""
Pydantic Schemas for EduPath Adaptation Agent & Plan Adaptation Decisions.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class AdaptationDecision(BaseModel):
    """Structured decision object produced by Adaptation Agent."""

    event_id: str = Field(..., description="Unique adaptation event ID (e.g., 'adapt_01')")
    user_id: str = Field(..., description="Learner user ID")
    trigger: str = Field("practice_result", description="Trigger mechanism: 'practice_result', 'manual', 'task_completion'")
    skill_name: str = Field(..., description="Target skill being evaluated")
    topic: str = Field(..., description="Target topic being evaluated")
    previous_status: str = Field(..., description="Performance status prior to adaptation ('struggling', 'needs_review', 'on_track', 'strong')")
    action: str = Field(
        ...,
        description="Adaptation action: 'continue', 'review', 'add_practice', 'revisit_prerequisite', 'move_forward'",
    )
    reason: str = Field(..., description="Explainable justification for the adaptation decision")
    affected_plan_version: int = Field(..., ge=1, description="Plan version before adaptation")
    new_plan_version: int = Field(..., ge=1, description="Plan version after adaptation")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class AdaptationAnalyzeRequest(BaseModel):
    """Payload schema for triggering an adaptation analysis."""

    user_id: str = Field(..., description="Target learner user ID")
    skill_name: Optional[str] = Field(None, description="Optional target skill filter")
    topic: Optional[str] = Field(None, description="Optional target topic filter")

    model_config = ConfigDict(from_attributes=True)
