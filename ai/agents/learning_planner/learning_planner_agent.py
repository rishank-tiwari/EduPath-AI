"""
Learning Planner Agent for EduPath (PLAN phase).

Generates structured, prerequisite-ordered, weekly-chunked personalized learning paths.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Set

from ai.agents.base_agent import BaseAgent
from app.schemas.learning_plan import LearningModule, LearningPlanResponse, LearningTask
from app.services.prerequisite_service import prerequisite_service
from app.utils.logger import logger
from app.utils.skill_normalizer import normalize_skill_name


class LearningPlannerAgent(BaseAgent):
    """
    Constructs deterministic, evidence-aware, prerequisite-ordered learning roadmaps
    tailored to a learner's skill gap analysis and available weekly study time.
    """

    def __init__(self, provider=None):
        super().__init__(
            name="LearningPlannerAgent",
            description="Constructs personalized, milestone-driven learning roadmaps designed to eliminate skill gaps.",
            provider=provider,
        )

    def generate_tasks_for_skill(
        self, skill_name: str, gap_status: str, difficulty: str
    ) -> List[LearningTask]:
        """
        Generates manageable, structured daily learning tasks for a target skill gap.
        Uses foundational task types: 'learn', 'practice', 'project', 'review'.
        """
        tasks: List[LearningTask] = []
        clean_name = skill_name.strip()

        if gap_status == "missing":
            # Missing skill: Needs foundational study, guided practice, hands-on task, and review
            tasks.append(
                LearningTask(
                    task_id=f"task_{uuid.uuid4().hex[:8]}",
                    title=f"Learn {clean_name} Core Concepts",
                    description=f"Study key theoretical concepts, formulas, and architecture of {clean_name}.",
                    task_type="learn",
                    estimated_minutes=60,
                    skill_name=clean_name,
                    difficulty=difficulty,
                    status="not_started",
                )
            )
            tasks.append(
                LearningTask(
                    task_id=f"task_{uuid.uuid4().hex[:8]}",
                    title=f"Practice {clean_name} Fundamentals",
                    description=f"Work through guided coding exercises and standard problems in {clean_name}.",
                    task_type="practice",
                    estimated_minutes=45,
                    skill_name=clean_name,
                    difficulty=difficulty,
                    status="not_started",
                )
            )
            tasks.append(
                LearningTask(
                    task_id=f"task_{uuid.uuid4().hex[:8]}",
                    title=f"Build {clean_name} Hands-On Task",
                    description=f"Implement a small practical component applying {clean_name}.",
                    task_type="project",
                    estimated_minutes=90,
                    skill_name=clean_name,
                    difficulty=difficulty,
                    status="not_started",
                )
            )
            tasks.append(
                LearningTask(
                    task_id=f"task_{uuid.uuid4().hex[:8]}",
                    title=f"Review & Consolidate {clean_name}",
                    description=f"Review quiz errors, code implementation, and key takeaways for {clean_name}.",
                    task_type="review",
                    estimated_minutes=30,
                    skill_name=clean_name,
                    difficulty=difficulty,
                    status="not_started",
                )
            )
        else:
            # needs_improvement skill: Targeted practice, refinement, project work
            tasks.append(
                LearningTask(
                    task_id=f"task_{uuid.uuid4().hex[:8]}",
                    title=f"Refine {clean_name} Advanced Patterns",
                    description=f"Review intermediate-to-advanced patterns and edge cases in {clean_name}.",
                    task_type="learn",
                    estimated_minutes=45,
                    skill_name=clean_name,
                    difficulty=difficulty,
                    status="not_started",
                )
            )
            tasks.append(
                LearningTask(
                    task_id=f"task_{uuid.uuid4().hex[:8]}",
                    title=f"Practice Applied {clean_name}",
                    description=f"Complete targeted problem solving focusing on weaker areas of {clean_name}.",
                    task_type="practice",
                    estimated_minutes=45,
                    skill_name=clean_name,
                    difficulty=difficulty,
                    status="not_started",
                )
            )
            tasks.append(
                LearningTask(
                    task_id=f"task_{uuid.uuid4().hex[:8]}",
                    title=f"Mini Project: {clean_name} Application",
                    description=f"Enhance existing portfolio project using advanced {clean_name} techniques.",
                    task_type="project",
                    estimated_minutes=60,
                    skill_name=clean_name,
                    difficulty=difficulty,
                    status="not_started",
                )
            )

        return tasks

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the learning planner engine using inputs:
        - learner_profile (dict/obj)
        - skill_gap_analysis (dict/obj)
        - role_requirements (dict/obj)
        """
        learner_profile = inputs.get("learner_profile") or {}
        skill_gap_analysis = inputs.get("skill_gap_analysis") or {}

        # Handle object or dict inputs gracefully
        if hasattr(learner_profile, "model_dump"):
            learner_profile = learner_profile.model_dump()
        if hasattr(skill_gap_analysis, "model_dump"):
            skill_gap_analysis = skill_gap_analysis.model_dump()

        user_id = learner_profile.get("user_id") or skill_gap_analysis.get("user_id") or "unknown_user"
        target_role = skill_gap_analysis.get("target_role") or learner_profile.get("target_role") or "Software Engineer"
        weekly_hours = learner_profile.get("weekly_learning_hours") or 10

        skills_gaps = skill_gap_analysis.get("skills") or skill_gap_analysis.get("skill_gaps") or []

        logger.info(f"Generating Personalized Learning Plan for user '{user_id}', role '{target_role}'...")

        # 1. Separate satisfied skills vs active gaps needing study
        satisfied_skills: Set[str] = set()
        active_gap_items: List[Dict[str, Any]] = []

        for gap in skills_gaps:
            s_name = gap.get("skill_name", "")
            status = gap.get("gap_status", "")
            if status in ("strong", "meets_requirement"):
                satisfied_skills.add(normalize_skill_name(s_name))
            elif status in ("needs_improvement", "missing"):
                active_gap_items.append(gap)

        # 2. Extract active skill names & order them via prerequisite graph topology
        active_skill_names = [g["skill_name"] for g in active_gap_items]
        ordered_skill_names = prerequisite_service.order_by_prerequisites(active_skill_names)

        # Re-index active gaps according to topological order & priority
        gap_map = {normalize_skill_name(g["skill_name"]): g for g in active_gap_items}
        
        priority_weight = {"high": 3, "medium": 2, "low": 1}

        def sort_key(skill_name: str):
            g = gap_map.get(skill_name, {})
            p_val = priority_weight.get(g.get("priority", "medium"), 2)
            imp_val = priority_weight.get(g.get("importance", "medium"), 2)
            # High priority/importance should come earlier among prerequisite-equivalent skills
            return (-p_val, -imp_val)

        ordered_skills = sorted(ordered_skill_names, key=sort_key)

        # 3. Create Weekly Modules and Tasks
        modules: List[LearningModule] = []
        current_week = 1
        current_week_hours = 0.0

        for skill_norm in ordered_skills:
            gap = gap_map.get(skill_norm)
            if not gap:
                continue

            skill_name = gap.get("skill_name", skill_norm)
            gap_status = gap.get("gap_status", "missing")
            priority = gap.get("priority", "medium")
            required_prof = gap.get("required_proficiency", "Intermediate")
            prereqs = prerequisite_service.get_prerequisites(skill_name)

            tasks = self.generate_tasks_for_skill(
                skill_name=skill_name,
                gap_status=gap_status,
                difficulty=required_prof,
            )

            mod_minutes = sum(t.estimated_minutes for t in tasks)
            mod_hours = round(mod_minutes / 60.0, 1)

            # Check if adding this module exceeds weekly capacity limit
            if current_week_hours > 0 and (current_week_hours + mod_hours > weekly_hours * 1.2):
                current_week += 1
                current_week_hours = 0.0

            module_id = f"mod_w{current_week}_{uuid.uuid4().hex[:6]}"
            mod_title = f"{skill_name} Mastery" if gap_status == "needs_improvement" else f"{skill_name} Foundations"

            module = LearningModule(
                module_id=module_id,
                title=mod_title,
                description=f"Focus on {gap_status.replace('_', ' ')} in {skill_name} to meet {target_role} requirements.",
                skill_name=skill_name,
                priority=priority,
                week_number=current_week,
                estimated_hours=mod_hours,
                prerequisites=prereqs,
                tasks=tasks,
                status="not_started",
            )
            modules.append(module)
            current_week_hours += mod_hours

        # Fallback if learner has 0 skill gaps (all requirements already met)
        if not modules:
            modules.append(
                LearningModule(
                    module_id=f"mod_w1_{uuid.uuid4().hex[:6]}",
                    title="Skill Maintenance & Advanced Specialization",
                    description=f"All benchmark requirements for {target_role} are satisfied. Review advanced topics.",
                    skill_name="General Engineering",
                    priority="low",
                    week_number=1,
                    estimated_hours=2.0,
                    prerequisites=[],
                    tasks=[
                        LearningTask(
                            task_id=f"task_{uuid.uuid4().hex[:8]}",
                            title=f"Explore Advanced {target_role} Trends",
                            description="Read latest technical blogs and architecture whitepapers.",
                            task_type="review",
                            estimated_minutes=120,
                            skill_name="General Engineering",
                            difficulty="Advanced",
                            status="not_started",
                        )
                    ],
                    status="already_satisfied",
                )
            )

        total_hours = round(sum(m.estimated_hours for m in modules), 1)
        duration_weeks = max(m.week_number for m in modules)
        plan_id = f"plan_{uuid.uuid4().hex[:12]}"

        summary = (
            f"Personalized {duration_weeks}-week learning roadmap for {target_role}. "
            f"Contains {len(modules)} study modules across {total_hours} total hours, "
            f"addressing {len(active_gap_items)} identified skill gaps in priority order."
        )

        plan_data = {
            "plan_id": plan_id,
            "user_id": user_id,
            "target_role": target_role,
            "title": f"{target_role} Learning Path",
            "summary": summary,
            "total_estimated_hours": total_hours,
            "duration_weeks": duration_weeks,
            "modules": [m.model_dump() for m in modules],
            "version": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        return plan_data
