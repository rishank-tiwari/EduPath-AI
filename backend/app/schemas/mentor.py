"""
Pydantic Schemas for EduPath Context-Aware AI Mentor Agent.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class MentorChatRequest(BaseModel):
    """Payload for asking a question to the AI Mentor."""

    user_id: str = Field(..., description="Learner user ID (e.g. 'demo_user_1')")
    message: str = Field(..., description="The learner's input question or prompt")


class MentorResponse(BaseModel):
    """Structured response output from the Context-Aware AI Mentor Agent."""

    response: str = Field(..., description="Natural language response text tailored to learner state")
    context_topic: str = Field(..., description="Primary topic or skill area referenced in response")
    suggested_action: Optional[str] = Field(None, description="Recommended next action or task title")
    response_mode: str = Field("fallback", description="Response generation mode: 'llm', 'gemini', or 'fallback'")
    related_skill: Optional[str] = Field(None, description="Skill name associated with question/context")
    related_task: Optional[str] = Field(None, description="Task title associated with question/context")
    related_gap: Optional[str] = Field(None, description="Missing or weak skill gap associated with question/context")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    model_config = ConfigDict(from_attributes=True)


class SanitizedMentorContext(BaseModel):
    """Sanitized, structured context assembled for the AI Mentor from real learner state."""

    user_id: str
    target_role: Optional[str] = None
    career_goal: Optional[str] = None
    current_skills: List[str] = Field(default_factory=list)
    strong_skills: List[str] = Field(default_factory=list)
    skills_to_improve: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    current_learning_task: Optional[Dict[str, Any]] = None
    learning_plan_summary: Optional[Dict[str, Any]] = None
    recent_practice_result: Optional[Dict[str, Any]] = None
    progress_summary: Optional[Dict[str, Any]] = None
    recent_adaptation: Optional[Dict[str, Any]] = None
    document_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    assembled_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
