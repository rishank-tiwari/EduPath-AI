"""
Pydantic Schemas for EduPath Learning Planner & Personalized Learning Path.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class LearningTask(BaseModel):
    """Actionable daily or single-session learning task."""

    task_id: str = Field(..., description="Unique task ID (e.g., 'task_w1_t1')")
    title: str = Field(..., description="Actionable task title (e.g., 'Learn Probability Basics')")
    description: str = Field(..., description="Short explanation of what to learn or perform")
    task_type: str = Field(
        ...,
        description="Type of task: 'learn', 'practice', 'project', or 'review'",
    )
    estimated_minutes: int = Field(..., ge=5, description="Estimated duration in minutes")
    skill_name: str = Field(..., description="Normalized target skill name")
    difficulty: str = Field(
        "Beginner",
        description="Task difficulty: 'Beginner', 'Intermediate', 'Advanced'",
    )
    status: str = Field(
        "not_started",
        description="Current task execution status: 'not_started', 'in_progress', 'completed', 'skipped'",
    )


class LearningModule(BaseModel):
    """Weekly study module containing related skills and daily tasks."""

    module_id: str = Field(..., description="Unique module ID (e.g., 'mod_w1_stats')")
    title: str = Field(..., description="User-facing module title (e.g., 'Statistics & Probability')")
    description: str = Field(..., description="High-level summary of module objectives")
    skill_name: str = Field(..., description="Primary skill addressed by this module")
    priority: str = Field(..., description="Module priority derived from gap analysis: 'high', 'medium', 'low'")
    week_number: int = Field(..., ge=1, description="Assigned week sequence number (1, 2, 3...)")
    estimated_hours: float = Field(..., ge=0.5, description="Total estimated study hours for module")
    prerequisites: List[str] = Field(default_factory=list, description="Skill names required before starting")
    tasks: List[LearningTask] = Field(default_factory=list, description="Ordered daily learning tasks")
    status: str = Field(
        "not_started",
        description="Module completion status: 'not_started', 'in_progress', 'completed', 'already_satisfied'",
    )
    completion_status: str = Field(
        "not_started",
        description="Persistent completion status: 'not_started', 'in_progress', 'completed'",
    )
    completed_at: Optional[str] = Field(None, description="ISO timestamp of when module practice was completed")
    latest_score: Optional[float] = Field(None, description="Latest percentage score achieved (0.0 to 100.0%)")
    best_score: Optional[float] = Field(None, description="Best percentage score achieved (0.0 to 100.0%)")
    practice_attempts: int = Field(0, description="Total practice session attempts for this module")
    last_practice_id: Optional[str] = Field(None, description="ID of the latest practice session completed")


class LearningPlanBase(BaseModel):
    """Base fields for Personalized Learning Plan."""

    plan_id: str = Field(..., description="Unique learning plan identifier")
    user_id: str = Field(..., description="Unique identifier of the learner")
    target_role: str = Field(..., description="Target career role (e.g., 'AI/ML Engineer')")
    title: str = Field(..., description="Plan title (e.g., 'AI/ML Engineer Learning Path')")
    summary: str = Field(..., description="Executive summary of the personalized roadmap")
    total_estimated_hours: float = Field(..., ge=0.0, description="Total planned study hours across all modules")
    duration_weeks: int = Field(..., ge=1, description="Total estimated duration in weeks")
    modules: List[LearningModule] = Field(default_factory=list, description="Chronological weekly modules")
    version: int = Field(1, ge=1, description="Learning plan version number for adaptation tracking")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class LearningPlanCreate(LearningPlanBase):
    """Payload schema for storing a generated learning plan."""

    pass


class LearningPlanResponse(LearningPlanBase):
    """Response schema for returning a stored learning plan."""

    model_config = ConfigDict(from_attributes=True)
