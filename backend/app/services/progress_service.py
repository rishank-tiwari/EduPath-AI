"""
Progress Domain Service for EduPath.

Coordinates progress recording, practice result consumption, performance analysis, and history retrieval.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import HTTPException, status
from ai.agents.progress.progress_agent import ProgressAgent
from app.repositories.practice_repository import practice_repository
from app.repositories.progress_repository import progress_repository
from app.schemas.progress import (
    ProgressEvent,
    ProgressSummary,
    SkillProgressSummary,
)
from app.utils.logger import logger


class ProgressService:
    """Domain service managing learner progress analysis and event recording."""

    def __init__(self):
        self.agent = ProgressAgent()

    def record_event(
        self, user_id: str, event_type: str, skill_name: str, topic: str, metadata: Dict = None
    ) -> ProgressEvent:
        """Records a new progress event in MongoDB."""
        if not user_id or not user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_id is required to record a progress event.",
            )

        event = ProgressEvent(
            event_id=f"evt_{uuid.uuid4().hex[:10]}",
            user_id=user_id,
            event_type=event_type,
            skill_name=skill_name,
            topic=topic,
            metadata=metadata or {},
            created_at=datetime.utcnow().isoformat(),
        )

        saved = progress_repository.save_event(event.model_dump())
        return ProgressEvent(**saved)

    def compute_and_save_progress_for_topic(
        self, user_id: str, skill_name: str, topic: str
    ) -> ProgressSummary:
        """
        Fetches all practice results for user_id, filters by skill_name and topic,
        runs ProgressAgent analysis, and saves the summary in MongoDB.
        """
        all_results = practice_repository.get_user_history(user_id)
        matching_results = [
            r for r in all_results
            if r.get("skill_name") == skill_name and r.get("topic") == topic
        ]

        summary = self.agent.analyze_practice_results(
            user_id=user_id,
            skill_name=skill_name,
            topic=topic,
            practice_results=matching_results,
        )

        progress_repository.save_summary(summary.model_dump())
        return summary

    def get_user_progress(self, user_id: str) -> List[ProgressSummary]:
        """Retrieves or re-computes progress summaries for user_id."""
        if not user_id or not user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_id query parameter is required to retrieve progress.",
            )

        # Ingest practice results to ensure summaries are up to date
        all_results = practice_repository.get_user_history(user_id)
        if all_results:
            grouped: Dict[tuple, List] = {}
            for r in all_results:
                key = (r.get("skill_name", "General"), r.get("topic", "General Topic"))
                grouped.setdefault(key, []).append(r)

            for (skill, topic), res_list in grouped.items():
                summary = self.agent.analyze_practice_results(
                    user_id=user_id, skill_name=skill, topic=topic, practice_results=res_list
                )
                progress_repository.save_summary(summary.model_dump())

        raw_summaries = progress_repository.get_user_summaries(user_id)
        return [ProgressSummary(**doc) for doc in raw_summaries]

    def get_skill_progress(self, user_id: str) -> List[SkillProgressSummary]:
        """Returns progress summaries grouped by skill_name."""
        summaries = self.get_user_progress(user_id)
        grouped: Dict[str, List[ProgressSummary]] = {}
        for s in summaries:
            grouped.setdefault(s.skill_name, []).append(s)

        result: List[SkillProgressSummary] = []
        for skill_name, topic_list in grouped.items():
            avg = round(sum(t.latest_score for t in topic_list) / len(topic_list), 1) if topic_list else 0.0
            overall = "on_track"
            if any(t.performance_status == "struggling" for t in topic_list):
                overall = "struggling"
            elif any(t.performance_status == "needs_review" for t in topic_list):
                overall = "needs_review"
            elif all(t.performance_status == "strong" for t in topic_list):
                overall = "strong"

            result.append(
                SkillProgressSummary(
                    skill_name=skill_name,
                    overall_status=overall,
                    average_score=avg,
                    topics=topic_list,
                )
            )
        return result

    def get_event_history(self, user_id: str) -> List[ProgressEvent]:
        """Retrieves progress events history for user_id."""
        if not user_id or not user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_id query parameter is required to retrieve event history.",
            )
        raw_events = progress_repository.get_event_history(user_id)
        return [ProgressEvent(**doc) for doc in raw_events]


progress_service = ProgressService()
