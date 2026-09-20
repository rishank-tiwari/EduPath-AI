"""
Skill Gap Agent Implementation for EduPath (GAP ANALYSIS phase).

Consumes structured LearnerProfile from Task 1.1, compares evidence-backed skills against target role benchmarks,
classifies skill gaps, calculates deterministic priorities, preserves evidence traceability, and computes overall readiness.
"""

from datetime import datetime
import uuid
from typing import Any, Dict, List, Optional
from ai.agents.base_agent import AgentTrace, BaseAgent
from ai.providers.factory import get_ai_provider
from ai.schemas.skill_gap_schema import SkillGapAnalysisResult
from app.schemas.learner_profile import LearnerProfileResponse, SkillEvidence, TechnicalSkill
from app.schemas.skill_gap import SkillGapItem
from app.services.role_service import role_service
from app.utils.skill_normalizer import normalize_skill_name

# Proficiency numerical mapping
PROFICIENCY_LEVELS = {
    "no evidence": 0,
    "beginner": 1,
    "intermediate": 2,
    "advanced": 3,
    "expert": 4,
}


class SkillGapAgent(BaseAgent):
    """
    Skill Gap Agent (GAP ANALYSIS Phase).
    Evaluates missing skills and proficiencies required to achieve target career role.
    """

    def __init__(self, provider=None):
        super().__init__(
            name="SkillGapAgent",
            description="Compares evidence-backed learner skills against target role benchmarks to calculate skill gaps, priorities, and readiness.",
            provider=provider or get_ai_provider(),
        )

    async def execute(self, profile: LearnerProfileResponse) -> SkillGapAnalysisResult:
        """
        Executes Skill Gap Agent analysis for a given LearnerProfileResponse.
        Returns validated SkillGapAnalysisResult.
        """
        trace_id = f"tr_{uuid.uuid4().hex[:10]}"
        start_time = datetime.utcnow()

        user_id = profile.user_id
        target_role = profile.target_role

        if not target_role:
            raise ValueError("Learner profile must specify a valid target_role")

        # 1. Fetch Target Role Benchmark Requirements
        role_benchmark = role_service.get_role_requirements(target_role)

        # 2. Build map of learner's normalized skills
        learner_skill_map: Dict[str, TechnicalSkill] = {}
        for skill in profile.technical_skills:
            norm_name = normalize_skill_name(skill.name).strip().lower()
            learner_skill_map[norm_name] = skill

        # 3. Analyze each required role skill
        gap_items: List[SkillGapItem] = []
        earned_points = 0.0
        max_points = 0.0
        matched_learner_keys = set()

        for req in role_benchmark.required_skills:
            norm_req_name = normalize_skill_name(req.name).strip().lower()
            learner_skill = learner_skill_map.get(norm_req_name)
            if learner_skill:
                matched_learner_keys.add(norm_req_name)

            current_prof = learner_skill.proficiency if learner_skill else "No evidence"
            current_level = PROFICIENCY_LEVELS.get(current_prof.lower(), 0)
            required_level = PROFICIENCY_LEVELS.get(req.required_proficiency.lower(), 2)

            # Classify Gap Status
            if current_level > required_level:
                gap_status = "strong"
                match_factor = 1.0
            elif current_level == required_level:
                gap_status = "meets_requirement"
                match_factor = 1.0
            elif current_level > 0:
                gap_status = "needs_improvement"
                match_factor = 0.5
            else:
                gap_status = "missing"
                match_factor = 0.0

            # Calculate Priority (Deterministic)
            priority = self._calculate_priority(gap_status, req.importance)

            # Preserve Evidence from Task 1.1 Profile
            evidence_list = learner_skill.evidence if learner_skill else []

            # Generate Human-Readable Reason
            reason = self._generate_reason(req.name, req.required_proficiency, current_prof, gap_status, target_role)

            gap_item = SkillGapItem(
                skill_name=req.name,
                required_proficiency=req.required_proficiency,
                current_proficiency=current_prof,
                gap_status=gap_status,
                priority=priority,
                importance=req.importance,
                reason=reason,
                evidence=evidence_list,
            )
            gap_items.append(gap_item)

            # Accumulate Readiness Points
            importance_weight = 3.0 if req.importance == "high" else (2.0 if req.importance == "medium" else 1.0)
            earned_points += match_factor * importance_weight
            max_points += 1.0 * importance_weight

        # 3b. Preserve declared skills from learner profile not explicitly in role benchmark
        for skill in profile.technical_skills:
            norm_skill_name = normalize_skill_name(skill.name).strip().lower()
            if norm_skill_name not in matched_learner_keys:
                matched_learner_keys.add(norm_skill_name)
                current_prof = skill.proficiency or "Intermediate"
                current_level = PROFICIENCY_LEVELS.get(current_prof.lower(), 2)
                gap_status = "strong" if (current_level >= 3 or skill.confidence >= 0.8) else "meets_requirement"
                
                gap_item = SkillGapItem(
                    skill_name=skill.name,
                    required_proficiency="Optional",
                    current_proficiency=current_prof,
                    gap_status=gap_status,
                    priority="low",
                    importance="low",
                    reason=f"{skill.name} is a verified declared skill in your learner profile.",
                    evidence=skill.evidence,
                )
                gap_items.append(gap_item)

        # 4. Compute Overall Readiness Score
        overall_readiness = min(100.0, round((earned_points / max_points) * 100, 1)) if max_points > 0 else 0.0

        # 5. Synthesize Executive Summary
        missing_count = sum(1 for g in gap_items if g.gap_status == "missing")
        improvement_count = sum(1 for g in gap_items if g.gap_status == "needs_improvement")
        met_count = sum(1 for g in gap_items if g.gap_status in ("meets_requirement", "strong"))

        summary = (
            f"Skill gap analysis for target role '{target_role}'. "
            f"Overall role readiness is {overall_readiness}%. "
            f"Learner meets {met_count} skill requirements, needs improvement in {improvement_count}, "
            f"and is missing {missing_count} required competencies."
        )

        result = SkillGapAnalysisResult(
            user_id=user_id,
            target_role=target_role,
            analyzed_at=datetime.utcnow().isoformat(),
            skills=gap_items,
            overall_readiness=overall_readiness,
            summary=summary,
        )

        # Emit observable execution trace
        self._last_trace = AgentTrace(
            trace_id=trace_id,
            agent_name=self.name,
            input_data={"user_id": user_id, "target_role": target_role},
            decision=f"Analyzed {len(gap_items)} skill benchmarks. Overall readiness: {overall_readiness}%.",
            tools_used=["role_requirement_service", "skill_normalizer", "readiness_calculator"],
            output_data={"overall_readiness": overall_readiness, "missing_skills_count": missing_count},
            status="success",
            created_at=start_time,
        )

        return result

    def _calculate_priority(self, gap_status: str, importance: str) -> str:
        """
        Calculates deterministic priority ('high', 'medium', 'low') based on gap status and role skill importance.
        """
        if gap_status in ("meets_requirement", "strong"):
            return "low"

        if importance == "high":
            return "high"
        elif importance == "medium":
            if gap_status in ("missing", "needs_improvement"):
                return "medium"
            return "low"
        else:
            return "low"

    def _generate_reason(
        self, skill_name: str, required_prof: str, current_prof: str, gap_status: str, target_role: str
    ) -> str:
        """Generates clear human-readable explanation for skill gap item."""
        if gap_status == "strong":
            return f"{skill_name} exceeds the {required_prof} proficiency requirement for {target_role}."
        elif gap_status == "meets_requirement":
            return f"{skill_name} satisfies the required {required_prof} proficiency for {target_role}."
        elif gap_status == "needs_improvement":
            return f"{skill_name} is required at {required_prof} level for {target_role}. Current learner level is {current_prof}."
        else:
            return f"{skill_name} is a required {required_prof} skill for {target_role}, but no evidence currently exists in the learner profile."
