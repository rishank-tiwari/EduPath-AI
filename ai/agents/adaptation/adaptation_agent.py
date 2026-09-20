"""
Adaptation Agent for EduPath (ADAPT phase).

Evaluates learner progress analysis against current learning plan and dynamically adjusts next steps.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Tuple

from ai.agents.base_agent import BaseAgent
from app.schemas.adaptation import AdaptationDecision
from app.schemas.learning_plan import LearningTask
from app.utils.logger import logger


class AdaptationAgent(BaseAgent):
    """
    Evaluates learner performance status and automatically modifies the learning plan
    with incremented plan version and explicit next-action tasks.
    """

    def __init__(self, provider=None):
        super().__init__(
            name="AdaptationAgent",
            description="Dynamically recalculates learning milestones and adds review or practice tasks based on performance status.",
            provider=provider,
        )

    def determine_adaptation_action(
        self, performance_status: str, latest_score: float
    ) -> Tuple[str, str]:
        """
        Determines the appropriate adaptation action and human-readable justification.
        """
        if performance_status == "strong":
            return (
                "move_forward",
                f"Learner achieved strong score ({latest_score}%). Advancing directly to next milestone without redundant review.",
            )
        elif performance_status == "on_track":
            return (
                "continue",
                f"Learner is on track ({latest_score}%). Continuing planned learning roadmap.",
            )
        elif performance_status == "needs_review":
            return (
                "add_practice",
                f"Learner score ({latest_score}%) indicates room for improvement. Added additional targeted practice task.",
            )
        else:  # struggling
            return (
                "review",
                f"Learner score ({latest_score}%) fell below requirement threshold. Inserted foundational review task and practice step.",
            )

    def adapt_learning_plan(
        self,
        plan_data: Dict[str, Any],
        progress_summary: Dict[str, Any],
    ) -> Tuple[AdaptationDecision, Dict[str, Any]]:
        """
        Modifies a learning plan based on progress summary analysis.
        Increments plan version (v1 -> v2) and returns AdaptationDecision + updated plan dict.
        """
        user_id = plan_data.get("user_id") or progress_summary.get("user_id") or "unknown_user"
        skill_name = progress_summary.get("skill_name", "General Engineering")
        topic = progress_summary.get("topic", "General Topic")
        status = progress_summary.get("performance_status", "on_track")
        latest_score = float(progress_summary.get("latest_score", 0.0))

        current_version = int(plan_data.get("version", 1))
        new_version = current_version + 1

        action, reason = self.determine_adaptation_action(status, latest_score)

        # Make a copy of plan_data for modification
        updated_plan = dict(plan_data)
        updated_plan["version"] = new_version
        updated_plan["updated_at"] = datetime.utcnow().isoformat()

        modules = list(updated_plan.get("modules", []))
        target_mod_idx = -1

        # Find matching module by skill_name
        for idx, mod in enumerate(modules):
            if mod.get("skill_name") == skill_name:
                target_mod_idx = idx
                break

        if target_mod_idx != -1:
            mod = dict(modules[target_mod_idx])
            tasks = list(mod.get("tasks", []))

            if action == "review":
                # Prepend a new foundational review task
                review_task = LearningTask(
                    task_id=f"task_review_{uuid.uuid4().hex[:6]}",
                    title=f"Review {topic} Core Concepts",
                    description=f"Focus review session on {topic} based on recent practice score ({latest_score}%).",
                    task_type="learn",
                    estimated_minutes=30,
                    skill_name=skill_name,
                    difficulty="Beginner",
                    status="not_started",
                ).model_dump()

                # Also append a re-assessment practice task
                practice_task = LearningTask(
                    task_id=f"task_reprac_{uuid.uuid4().hex[:6]}",
                    title=f"Re-test {topic} Skills",
                    description=f"Follow-up practice session to verify retention of {topic}.",
                    task_type="practice",
                    estimated_minutes=30,
                    skill_name=skill_name,
                    difficulty="Beginner",
                    status="not_started",
                ).model_dump()

                tasks = [review_task] + tasks + [practice_task]
                mod["title"] = f"{skill_name} (Review & Reinforcement)"
                mod["priority"] = "high"

            elif action == "add_practice":
                # Append targeted practice task
                practice_task = LearningTask(
                    task_id=f"task_extra_{uuid.uuid4().hex[:6]}",
                    title=f"Targeted Practice: {topic}",
                    description=f"Additional practice set to solidify {topic} (previous score: {latest_score}%).",
                    task_type="practice",
                    estimated_minutes=30,
                    skill_name=skill_name,
                    difficulty="Intermediate",
                    status="not_started",
                ).model_dump()
                tasks.append(practice_task)

            mod["tasks"] = tasks
            modules[target_mod_idx] = mod
            updated_plan["modules"] = modules

        decision = AdaptationDecision(
            event_id=f"adapt_{uuid.uuid4().hex[:10]}",
            user_id=user_id,
            trigger="practice_result",
            skill_name=skill_name,
            topic=topic,
            previous_status=status,
            action=action,
            reason=reason,
            affected_plan_version=current_version,
            new_plan_version=new_version,
            created_at=datetime.utcnow().isoformat(),
        )

        return decision, updated_plan

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Executes adaptation decision and plan updating."""
        plan_data = inputs.get("plan_data", {})
        progress_summary = inputs.get("progress_summary", {})

        decision, updated_plan = self.adapt_learning_plan(plan_data, progress_summary)

        return {
            "decision": decision.model_dump(),
            "updated_plan": updated_plan,
        }
