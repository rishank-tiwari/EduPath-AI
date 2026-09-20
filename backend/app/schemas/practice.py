"""
Pydantic Schemas for EduPath Practice Agent, Question Generation & Submissions.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class PracticeQuestion(BaseModel):
    """Structured practice question item."""

    question_id: str = Field(..., description="Unique question ID (e.g., 'q_stat_01')")
    question: str = Field(..., description="The problem prompt or question text")
    question_type: str = Field(
        ...,
        description="Question type: 'mcq' or 'short_answer'",
    )
    options: Optional[List[str]] = Field(None, description="Multiple choice options if question_type is 'mcq'")
    correct_answer: str = Field(..., description="Authoritative correct answer string")
    explanation: str = Field(..., description="Concise explanation of why the correct answer is right")
    difficulty: str = Field("beginner", description="Question difficulty: 'beginner', 'intermediate', 'advanced'")
    skill_name: Optional[str] = Field(None, description="Associated skill name")
    topic: Optional[str] = Field(None, description="Associated topic name")


class PracticeQuestionPublic(BaseModel):
    """Public version of practice question presented to learner (omitting correct answer and explanation)."""

    question_id: str = Field(...)
    question: str = Field(...)
    question_type: str = Field(...)
    options: Optional[List[str]] = Field(None)
    difficulty: str = Field("beginner")
    skill_name: Optional[str] = Field(None)
    topic: Optional[str] = Field(None)


class PracticeSession(BaseModel):
    """Active practice session for a learning task."""

    practice_id: str = Field(..., description="Unique practice session ID")
    user_id: str = Field(..., description="Learner user ID")
    task_id: str = Field(..., description="Learning task ID")
    module_id: Optional[str] = Field(None, description="Optional associated learning module ID")
    skill_name: str = Field(..., description="Target skill name")
    topic: str = Field(..., description="Topic summary")
    difficulty: str = Field("beginner", description="Session difficulty level")
    practice_mode: str = Field("general", description="Practice mode: 'general' (10 questions) or 'module' (5 questions)")
    questions: List[PracticeQuestionPublic] = Field(default_factory=list, description="List of questions for learner")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class LearnerAnswerItem(BaseModel):
    """Submitted answer for an individual question."""

    question_id: str = Field(..., description="Question ID being answered")
    learner_answer: str = Field(..., description="Text of the answer provided by learner")


class PracticeSubmissionRequest(BaseModel):
    """Payload for submitting answers for a practice session."""

    user_id: str = Field(..., description="Learner user ID")
    answers: List[LearnerAnswerItem] = Field(..., description="List of submitted answers")


class QuestionEvaluationResult(BaseModel):
    """Evaluation output for an individual submitted question."""

    question_id: str = Field(...)
    question: str = Field(...)
    correct: bool = Field(...)
    learner_answer: str = Field(...)
    correct_answer: str = Field(...)
    explanation: str = Field(...)


class PracticeResultRecord(BaseModel):
    """Structured practice evaluation result record stored in MongoDB."""

    result_id: str = Field(..., description="Unique result record ID")
    user_id: str = Field(..., description="Learner user ID")
    practice_id: str = Field(..., description="Practice session ID")
    task_id: str = Field(..., description="Associated task ID")
    skill_name: str = Field(..., description="Target skill name")
    topic: str = Field(..., description="Topic summary")
    difficulty: str = Field("beginner", description="Difficulty level")
    score: int = Field(..., ge=0, description="Number of correctly answered questions")
    total_questions: int = Field(..., ge=1, description="Total questions evaluated")
    percentage: float = Field(..., ge=0.0, le=100.0, description="Percentage score (0.0 to 100.0%)")
    question_results: List[QuestionEvaluationResult] = Field(default_factory=list)
    completed_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    model_config = ConfigDict(from_attributes=True)
