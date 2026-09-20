"""
Progress Agent for EduPath (MEASURE phase).

Analyzes historical practice results and tracks learner performance trajectory, trends, and weak areas.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from ai.agents.base_agent import BaseAgent
from app.schemas.progress import ProgressSummary
from app.utils.logger import logger

# Configurable performance thresholds
PERFORMANCE_THRESHOLDS = {
    "strong": 90.0,
    "on_track": 70.0,
    "needs_review": 50.0,
}


def classify_performance(score: float) -> str:
    """Classifies a percentage score into a performance status deterministically."""
    if score >= PERFORMANCE_THRESHOLDS["strong"]:
        return "strong"
    elif score >= PERFORMANCE_THRESHOLDS["on_track"]:
        return "on_track"
    elif score >= PERFORMANCE_THRESHOLDS["needs_review"]:
        return "needs_review"
    else:
        return "struggling"


def calculate_trend(scores: List[float]) -> str:
    """Calculates performance trend across chronological attempt scores."""
    if not scores or len(scores) < 2:
        return "insufficient_data"

    latest = scores[-1]
    previous = scores[-2]

    diff = latest - previous
    if diff > 5.0:
        return "improving"
    elif diff < -5.0:
        return "declining"
    else:
        return "stable"


class ProgressAgent(BaseAgent):
    """
    Analyzes historical learner assessment events and evaluates skill progression,
    trajectory trends, and weakness detection.
    """

    def __init__(self, provider=None):
        super().__init__(
            name="ProgressAgent",
            description="Tracks historical assessment results and monitors skill growth velocity and performance trajectory.",
            provider=provider,
        )

    def analyze_practice_results(
        self, user_id: str, skill_name: str, topic: str, practice_results: List[Dict[str, Any]]
    ) -> ProgressSummary:
        """
        Analyzes a list of practice result records for a given user, skill, and topic.
        Produces a validated ProgressSummary model.
        """
        if not practice_results:
            return ProgressSummary(
                progress_id=f"prog_{uuid.uuid4().hex[:8]}",
                user_id=user_id,
                skill_name=skill_name,
                topic=topic,
                total_attempts=0,
                total_questions=0,
                correct_answers=0,
                average_score=0.0,
                latest_score=0.0,
                performance_status="on_track",
                trend="insufficient_data",
            )

        # Sort practice results chronologically by completed_at
        sorted_results = sorted(practice_results, key=lambda r: r.get("completed_at", ""))

        scores = [float(r.get("percentage", 0.0)) for r in sorted_results]
        total_attempts = len(sorted_results)
        total_questions = sum(int(r.get("total_questions", 0)) for r in sorted_results)
        correct_answers = sum(int(r.get("score", 0)) for r in sorted_results)

        average_score = round(sum(scores) / total_attempts, 1) if total_attempts > 0 else 0.0
        latest_score = round(scores[-1], 1)

        status = classify_performance(latest_score)
        trend = calculate_trend(scores)
        last_activity = sorted_results[-1].get("completed_at", datetime.utcnow().isoformat())

        return ProgressSummary(
            progress_id=f"prog_{uuid.uuid4().hex[:8]}",
            user_id=user_id,
            skill_name=skill_name,
            topic=topic,
            total_attempts=total_attempts,
            total_questions=total_questions,
            correct_answers=correct_answers,
            average_score=average_score,
            latest_score=latest_score,
            performance_status=status,
            trend=trend,
            last_activity_at=last_activity,
            updated_at=datetime.utcnow().isoformat(),
        )

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Executes progress analysis for provided practice results."""
        user_id = inputs.get("user_id", "demo_user")
        skill_name = inputs.get("skill_name", "General Engineering")
        topic = inputs.get("topic", "General Topic")
        results = inputs.get("practice_results", [])

        summary = self.analyze_practice_results(
            user_id=user_id,
            skill_name=skill_name,
            topic=topic,
            practice_results=results,
        )

        return summary.model_dump()
