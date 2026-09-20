"""
Practice Agent Domain Service for EduPath.

Coordinates practice session generation, learner answer evaluation, scoring, and persistence.
"""

from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException, status
from ai.agents.practice.practice_agent import PracticeAgent
from app.repositories.learning_plan_repository import learning_plan_repository
from app.repositories.practice_repository import practice_repository
from app.schemas.practice import LearnerAnswerItem, PracticeResultRecord, PracticeSession
from app.utils.logger import logger


class PracticeService:
    """Domain service managing practice activity workflow and evaluation."""

    def __init__(self):
        self.agent = PracticeAgent()

    def generate_practice(
        self,
        user_id: str,
        task_id: str,
        skill_name: str,
        difficulty: str = "beginner",
        practice_mode: str = "general",
        module_id: Optional[str] = None,
        skills: Optional[List[str]] = None,
    ) -> PracticeSession:
        """Generates a practice session for a learning task and persists session data."""
        if not user_id or not user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_id is required to generate a practice session.",
            )

        # Infer learner's improvement skills for General Practice mode if not provided
        if practice_mode == "general":
            module_id = None
            if not skills or len(skills) == 0:
                try:
                    from app.repositories.skill_gap_repository import skill_gap_repository
                    gap_doc = skill_gap_repository.get_latest_by_user_id(user_id)
                    if gap_doc and "skills" in gap_doc:
                        improvable = [
                            s["skill_name"]
                            for s in gap_doc["skills"]
                            if s.get("gap_status") in ("needs_improvement", "missing", "needs_practice", "weak", "struggling")
                        ]
                        if improvable:
                            skills = improvable
                except Exception as e:
                    logger.warning(f"Could not infer skill gap improvements for general practice: {e}")

        # Check if module is already completed
        if practice_mode == "module" and (module_id or task_id):
            plan_doc = learning_plan_repository.get_latest_by_user_id(user_id)
            if plan_doc and "modules" in plan_doc:
                for mod in plan_doc["modules"]:
                    if (module_id and mod.get("module_id") == module_id) or any(
                        t.get("task_id") == task_id for t in mod.get("tasks", [])
                    ):
                        if mod.get("status") == "completed" or mod.get("completion_status") == "completed":
                            raise HTTPException(
                                status_code=status.HTTP_409_CONFLICT,
                                detail=f"Module '{mod.get('title', skill_name)}' is already completed.",
                            )

        res = self.agent.generate_practice_session(
            user_id=user_id,
            task_id=task_id,
            skill_name=skill_name or "General",
            difficulty=difficulty,
            practice_mode=practice_mode,
            module_id=module_id,
            skills=skills,
        )

        session_data = res["session_data"]
        full_questions = res["full_questions"]

        # Persist session to MongoDB
        practice_repository.save_session(session_data, full_questions)

        return PracticeSession(**session_data)

    def submit_practice(
        self, practice_id: str, user_id: str, answers: List[LearnerAnswerItem]
    ) -> PracticeResultRecord:
        """Evaluates submitted answers for a practice session, updates module completion, and stores the result."""
        if not practice_id or not practice_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="practice_id is required to submit practice answers.",
            )

        # 1. Fetch practice session from database
        doc = practice_repository.get_session(practice_id)
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Practice session with practice_id '{practice_id}' not found.",
            )

        session_data = doc["session_data"]
        full_questions = doc["full_questions"]

        # 2. Evaluate submission via PracticeAgent
        record = self.agent.evaluate_submission(
            session_data=session_data,
            full_questions=full_questions,
            submitted_answers=[a.model_dump() for a in answers],
        )

        # 3. Override user_id if provided in submission request
        eff_user_id = user_id if (user_id and user_id.strip()) else session_data["user_id"]
        record.user_id = eff_user_id

        # 4. Save result record in MongoDB
        saved_record = practice_repository.save_result(record.model_dump())

        # 5. Persist Module Completion State in MongoDB LearningPlan
        try:
            mod_id = session_data.get("module_id")
            tsk_id = session_data.get("task_id")
            plan_doc = learning_plan_repository.get_latest_by_user_id(eff_user_id)
            if plan_doc and "modules" in plan_doc:
                updated_modules = []
                plan_changed = False
                for mod in plan_doc["modules"]:
                    if (mod_id and mod.get("module_id") == mod_id) or (
                        tsk_id and any(t.get("task_id") == tsk_id for t in mod.get("tasks", []))
                    ):
                        mod["status"] = "completed"
                        mod["completion_status"] = "completed"
                        mod["completed_at"] = datetime.utcnow().isoformat()
                        mod["latest_score"] = record.percentage
                        prev_best = mod.get("best_score") or 0.0
                        mod["best_score"] = max(prev_best, record.percentage)
                        mod["practice_attempts"] = (mod.get("practice_attempts") or 0) + 1
                        mod["last_practice_id"] = practice_id
                        plan_changed = True
                    updated_modules.append(mod)

                if plan_changed:
                    plan_doc["modules"] = updated_modules
                    plan_doc["updated_at"] = datetime.utcnow().isoformat()
                    learning_plan_repository.save_plan(plan_doc)
                    logger.info(f"Updated module completion status in MongoDB LearningPlan for user '{eff_user_id}'.")
        except Exception as e:
            logger.warning(f"Could not update module completion status in plan: {e}")

        return PracticeResultRecord(**saved_record)

    def get_user_history(self, user_id: str) -> List[PracticeResultRecord]:
        """Retrieves practice result history for user_id."""
        if not user_id or not user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_id query parameter is required to retrieve practice history.",
            )

        history_docs = practice_repository.get_user_history(user_id)
        return [PracticeResultRecord(**doc) for doc in history_docs]

    def get_result(self, identifier: str) -> PracticeResultRecord:
        """Retrieves practice result record by result_id or practice_id."""
        if not identifier or not identifier.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Result identifier is required.",
            )
        doc = practice_repository.get_result(identifier)
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Practice result with ID '{identifier}' not found.",
            )
        return PracticeResultRecord(**doc)


practice_service = PracticeService()
