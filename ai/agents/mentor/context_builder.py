"""
Context Builder for EduPath Context-Aware AI Mentor Agent.

Assembles real, sanitized learner state from MongoDB repositories without inventing or fabricating data.
Priority hierarchy:
1. Current learning task
2. Current skill gaps
3. Recent practice performance
4. Learning plan
5. Target role
6. General learner information & Document Evidence
"""

from typing import Any, Dict, List, Optional
from app.repositories.adaptation_repository import adaptation_repository
from app.repositories.learning_plan_repository import learning_plan_repository
from app.repositories.practice_repository import practice_repository
from app.repositories.profile_repository import profile_repository
from app.repositories.progress_repository import progress_repository
from app.repositories.skill_gap_repository import skill_gap_repository
from app.schemas.mentor import SanitizedMentorContext


class MentorContextBuilder:
    """Retrieves and packages authorized learner state into a structured context model for the AI Mentor."""

    @staticmethod
    def build_context(user_id: str) -> SanitizedMentorContext:
        """
        Gathers live data for `user_id` from existing backend repositories.
        Safe against missing or partial data records.
        """
        # 1. Learner Profile
        try:
            profile_doc = profile_repository.get_by_user_id(user_id) or {}
        except Exception:
            profile_doc = {}

        target_role = profile_doc.get("target_role") or "AI/ML Engineer"
        career_goal = profile_doc.get("career_goal")

        current_skills = []
        document_evidence = []
        tech_skills = profile_doc.get("technical_skills") or []
        for s in tech_skills:
            if isinstance(s, dict):
                s_name = s.get("name")
                if s_name:
                    current_skills.append(s_name)
                for ev in s.get("evidence", []):
                    if isinstance(ev, dict):
                        document_evidence.append({
                            "skill_name": s_name,
                            "source_type": ev.get("source_type"),
                            "description": ev.get("description"),
                            "evidence_source": ev.get("evidence_source"),
                        })
            elif isinstance(s, str):
                current_skills.append(s)

        if not current_skills and profile_doc.get("current_skills"):
            for s in profile_doc.get("current_skills") or []:
                if isinstance(s, str):
                    current_skills.append(s)
                elif isinstance(s, dict) and s.get("name"):
                    current_skills.append(s["name"])

        # 2. Skill Gap Analysis
        try:
            gap_doc = skill_gap_repository.get_by_user_id(user_id) or {}
        except Exception:
            gap_doc = {}

        strong_skills = []
        for s in gap_doc.get("strong_skills") or []:
            if isinstance(s, dict) and s.get("skill_name"):
                strong_skills.append(s["skill_name"])
            elif isinstance(s, str):
                strong_skills.append(s)

        skills_to_improve = []
        for s in gap_doc.get("skills_to_improve") or []:
            if isinstance(s, dict) and s.get("skill_name"):
                skills_to_improve.append(s["skill_name"])
            elif isinstance(s, str):
                skills_to_improve.append(s)

        missing_skills = []
        for s in gap_doc.get("missing_skills") or []:
            if isinstance(s, dict) and s.get("skill_name"):
                missing_skills.append(s["skill_name"])
            elif isinstance(s, str):
                missing_skills.append(s)

        # 3. Learning Plan & Current Task
        try:
            plan_doc = learning_plan_repository.get_latest_by_user_id(user_id) or {}
        except Exception:
            plan_doc = {}

        current_learning_task = None
        plan_summary = None

        if plan_doc:
            modules = plan_doc.get("modules") or []
            plan_summary = {
                "plan_id": plan_doc.get("plan_id"),
                "version": plan_doc.get("version", 1),
                "target_role": plan_doc.get("target_role", target_role),
                "estimated_weeks": plan_doc.get("estimated_weeks", 4),
                "total_modules": len(modules),
            }

            if modules and len(modules) > 0:
                first_module = modules[0]
                tasks = first_module.get("tasks") if isinstance(first_module, dict) else []
                if tasks and len(tasks) > 0:
                    first_task = tasks[0]
                    if isinstance(first_task, dict):
                        current_learning_task = {
                            "task_id": first_task.get("task_id"),
                            "title": first_task.get("title", "Core Concepts"),
                            "skill_name": first_task.get("skill_name", "Statistics"),
                            "description": first_task.get("description", ""),
                            "difficulty": first_task.get("difficulty", "beginner"),
                            "estimated_minutes": first_task.get("estimated_minutes", 30),
                            "why_learning": first_task.get("why_learning", f"Required skill for {target_role}"),
                        }

        # 4. Recent Practice Results
        try:
            practice_results = practice_repository.get_user_history(user_id) or []
        except Exception:
            practice_results = []

        recent_practice = None
        if practice_results and len(practice_results) > 0:
            latest = practice_results[0]
            if isinstance(latest, dict):
                recent_practice = {
                    "result_id": latest.get("result_id"),
                    "practice_id": latest.get("practice_id"),
                    "skill_name": latest.get("skill_name"),
                    "topic": latest.get("topic"),
                    "score": latest.get("score"),
                    "total_questions": latest.get("total_questions"),
                    "percentage": latest.get("percentage"),
                    "difficulty": latest.get("difficulty"),
                }

        # 5. Progress Summary
        try:
            progress_summaries = progress_repository.get_user_progress(user_id) or []
        except Exception:
            progress_summaries = []

        progress_data = None
        if progress_summaries and len(progress_summaries) > 0:
            latest_prog = progress_summaries[-1]
            if isinstance(latest_prog, dict):
                progress_data = {
                    "skill_name": latest_prog.get("skill_name"),
                    "topic": latest_prog.get("topic"),
                    "performance_status": latest_prog.get("performance_status"),
                    "average_score": latest_prog.get("average_score"),
                    "latest_score": latest_prog.get("latest_score"),
                    "total_attempts": latest_prog.get("total_attempts"),
                }

        # 6. Recent Adaptation History
        try:
            adaptation_history = adaptation_repository.get_user_history(user_id) or []
        except Exception:
            adaptation_history = []

        recent_adaptation = None
        if adaptation_history and len(adaptation_history) > 0:
            latest_adapt = adaptation_history[-1]
            if isinstance(latest_adapt, dict):
                recent_adaptation = {
                    "event_id": latest_adapt.get("event_id"),
                    "action": latest_adapt.get("action"),
                    "reason": latest_adapt.get("reason"),
                    "skill_name": latest_adapt.get("skill_name"),
                    "topic": latest_adapt.get("topic"),
                    "affected_plan_version": latest_adapt.get("affected_plan_version"),
                    "new_plan_version": latest_adapt.get("new_plan_version"),
                }

        return SanitizedMentorContext(
            user_id=user_id,
            target_role=target_role,
            career_goal=career_goal,
            current_skills=current_skills,
            strong_skills=strong_skills,
            skills_to_improve=skills_to_improve,
            missing_skills=missing_skills,
            current_learning_task=current_learning_task,
            learning_plan_summary=plan_summary,
            recent_practice_result=recent_practice,
            progress_summary=progress_data,
            recent_adaptation=recent_adaptation,
            document_evidence=document_evidence,
        )
