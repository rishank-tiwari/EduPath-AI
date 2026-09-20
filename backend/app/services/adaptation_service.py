"""
Adaptation Domain Service for EduPath.

Coordinates performance analysis, adaptation decision making, plan version incrementation, and adaptation event tracking.
"""

from typing import List, Optional
from fastapi import HTTPException, status
from ai.agents.adaptation.adaptation_agent import AdaptationAgent
from app.repositories.adaptation_repository import adaptation_repository
from app.repositories.learning_plan_repository import learning_plan_repository
from app.schemas.adaptation import AdaptationDecision
from app.services.progress_service import progress_service
from app.utils.logger import logger


class AdaptationService:
    """Domain service orchestrating adaptive learning plan updates based on learner performance."""

    def __init__(self):
        self.agent = AdaptationAgent()

    async def analyze_and_adapt(
        self, user_id: str, skill_name: Optional[str] = None, topic: Optional[str] = None
    ) -> AdaptationDecision:
        """
        Analyzes learner progress, applies adaptation rules, modifies learning plan,
        increments plan version (v1 -> v2), and persists AdaptationDecision.
        """
        if not user_id or not user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_id is required to trigger adaptation analysis.",
            )

        # 1. Fetch current Learning Plan (or auto-generate if none exists yet)
        plan_dict = learning_plan_repository.get_latest_by_user_id(user_id)
        if not plan_dict:
            try:
                from app.services.learning_plan_service import learning_plan_service
                plan_resp = await learning_plan_service.generate_plan(user_id)
                plan_dict = plan_resp.model_dump()
            except Exception as gen_err:
                logger.warning(f"Adaptation failed: Could not auto-generate plan for user '{user_id}': {gen_err}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Learning plan for user_id '{user_id}' not found and could not be generated.",
                )

        # 2. Fetch progress summaries for user
        progress_summaries = progress_service.get_user_progress(user_id)

        target_summary: Optional[Dict] = None
        if skill_name:
            matching = [s for s in progress_summaries if s.skill_name == skill_name]
            if matching:
                target_summary = matching[0].model_dump()

        if not target_summary and progress_summaries:
            # Default to most recently updated or lowest performance summary
            sorted_by_status = sorted(
                progress_summaries,
                key=lambda s: 0 if s.performance_status == "struggling" else 1 if s.performance_status == "needs_review" else 2
            )
            target_summary = sorted_by_status[0].model_dump()

        if not target_summary:
            # Fallback if no practice has been taken yet
            target_summary = {
                "user_id": user_id,
                "skill_name": skill_name or plan_dict.get("modules", [{}])[0].get("skill_name", "General"),
                "topic": topic or "General Topic",
                "performance_status": "on_track",
                "latest_score": 75.0,
            }

        # 3. Execute AdaptationAgent
        decision, updated_plan = self.agent.adapt_learning_plan(
            plan_data=plan_dict,
            progress_summary=target_summary,
        )

        # 4. Save updated Learning Plan in MongoDB (v1 -> v2)
        learning_plan_repository.save_plan(updated_plan)

        # 5. Save AdaptationDecision event in MongoDB
        adaptation_repository.save_adaptation(decision.model_dump())

        # 6. Record progress event log
        progress_service.record_event(
            user_id=user_id,
            event_type="plan_updated",
            skill_name=decision.skill_name,
            topic=decision.topic,
            metadata={
                "action": decision.action,
                "reason": decision.reason,
                "affected_plan_version": decision.affected_plan_version,
                "new_plan_version": decision.new_plan_version,
            },
        )

        return decision

    def get_user_adaptation_history(self, user_id: str) -> List[AdaptationDecision]:
        """Retrieves adaptation event history for user_id."""
        if not user_id or not user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_id query parameter is required to retrieve adaptation history.",
            )
        docs = adaptation_repository.get_user_history(user_id)
        return [AdaptationDecision(**d) for d in docs]


adaptation_service = AdaptationService()
