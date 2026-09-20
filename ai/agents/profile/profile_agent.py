"""
Profile Agent Implementation for EduPath (UNDERSTAND phase).

Receives learner background data, normalizes skill evidence, estimates evidence-backed confidence,
and generates structured Pydantic profile schemas for downstream agents.
"""

from datetime import datetime
import uuid
from typing import Any, Dict, List, Optional
from ai.agents.base_agent import AgentTrace, BaseAgent
from ai.providers.factory import get_ai_provider
from ai.schemas.profile_schema import ProfileAnalysisInput, ProfileAnalysisResult
from app.schemas.learner_profile import (
    Certification,
    Education,
    Project,
    SkillEvidence,
    TechnicalSkill,
)


class ProfileAgent(BaseAgent):
    """
    Profile Agent (UNDERSTAND Phase).
    Converts learner inputs, project evidence, and resume data into a structured, evidence-backed LearnerProfile.
    """

    def __init__(self, provider=None):
        super().__init__(
            name="ProfileAgent",
            description="Analyzes learner background, extracts technical skills, associates evidence, and computes profile completeness.",
            provider=provider or get_ai_provider(),
        )

    async def execute(self, inputs: Dict[str, Any]) -> ProfileAnalysisResult:
        """
        Executes Profile Agent analysis.
        Inputs may be raw dictionary or ProfileAnalysisInput payload.
        """
        trace_id = f"tr_{uuid.uuid4().hex[:10]}"
        start_time = datetime.utcnow()

        # Parse input payload
        if isinstance(inputs, ProfileAnalysisInput):
            analysis_input = inputs
        else:
            analysis_input = ProfileAnalysisInput(**inputs)

        # Build evidence-backed technical skills
        technical_skills = self._process_skills(
            declared_skills=analysis_input.declared_skills,
            declared_projects=analysis_input.declared_projects,
            raw_background=analysis_input.raw_background,
        )

        # Process projects
        projects = [
            Project(
                project_id=p.get("project_id") or f"proj_{uuid.uuid4().hex[:6]}",
                title=p.get("title", "Untitled Project"),
                description=p.get("description", ""),
                technologies_used=p.get("technologies_used", []),
                repository_url=p.get("repository_url"),
                demo_url=p.get("demo_url"),
            )
            for p in analysis_input.declared_projects
        ]

        # Process certifications
        certifications = [
            Certification(
                cert_id=c.get("cert_id") or f"cert_{uuid.uuid4().hex[:6]}",
                name=c.get("name", "Certification"),
                issuing_organization=c.get("issuing_organization", "Unknown"),
                issue_date=c.get("issue_date"),
                credential_id=c.get("credential_id"),
            )
            for c in analysis_input.declared_certifications
        ]

        # Process education
        education = [
            Education(
                degree=e.get("degree", "Degree"),
                field_of_study=e.get("field_of_study", "Field"),
                institution=e.get("institution", "Institution"),
                graduation_year=e.get("graduation_year"),
            )
            for e in analysis_input.declared_education
        ]

        # Infer experience level
        experience_level = self._infer_experience_level(projects, education, analysis_input.raw_background)

        # Synthesize profile summary
        profile_summary = (
            f"Learner targeting {analysis_input.target_role}. "
            f"Demonstrated background across {len(technical_skills)} technical skills "
            f"and {len(projects)} portfolio projects. Experience level: {experience_level}."
        )

        # Calculate profile completeness score
        completeness = self._calculate_completeness(
            target_role=analysis_input.target_role,
            career_goal=analysis_input.career_goal,
            skills=technical_skills,
            projects=projects,
            certifications=certifications,
            education=education,
            raw_background=analysis_input.raw_background,
        )

        # Assemble structured result model
        result = ProfileAnalysisResult(
            user_id=analysis_input.user_id,
            target_role=analysis_input.target_role,
            career_goal=analysis_input.career_goal,
            inferred_experience_level=experience_level,
            profile_summary=profile_summary,
            technical_skills=technical_skills,
            soft_skills=["Problem Solving", "Continuous Learning", "Technical Communication"],
            projects=projects,
            certifications=certifications,
            education=education,
            profile_completeness=completeness,
        )

        # Emit observable execution trace
        self._last_trace = AgentTrace(
            trace_id=trace_id,
            agent_name=self.name,
            input_data={"user_id": analysis_input.user_id, "target_role": analysis_input.target_role},
            decision=f"Normalized {len(technical_skills)} skills with evidence confidence scoring.",
            tools_used=["skill_evidence_analyzer", "completeness_calculator"],
            output_data={"profile_completeness": completeness, "experience_level": experience_level},
            status="success",
            created_at=start_time,
        )

        return result

    def _process_skills(
        self, declared_skills: List[str], declared_projects: List[Dict[str, Any]], raw_background: Optional[str]
    ) -> List[TechnicalSkill]:
        """Maps declared skills to concrete project evidence and computes evidence-backed confidence scores."""
        skill_map: Dict[str, TechnicalSkill] = {}

        # 1. Process explicit declared skills
        for s in declared_skills:
            norm_name = s.strip()
            if norm_name and norm_name not in skill_map:
                skill_map[norm_name] = TechnicalSkill(
                    name=norm_name,
                    proficiency="Intermediate",
                    confidence=0.50,  # Base confidence for unverified declared skill
                    evidence=[
                        SkillEvidence(
                            source_type="manual",
                            description="User self-declared skill in profile settings",
                        )
                    ],
                )

        # 2. Extract technologies from declared projects as evidence
        for p in declared_projects:
            proj_title = p.get("title", "Project")
            proj_id = p.get("project_id", "proj")
            for tech in p.get("technologies_used", []):
                norm_tech = tech.strip()
                if not norm_tech:
                    continue

                evidence_item = SkillEvidence(
                    source_type="project",
                    source_id=proj_id,
                    description=f"Demonstrated tech usage in project '{proj_title}'",
                )

                if norm_tech in skill_map:
                    skill_map[norm_tech].evidence.append(evidence_item)
                    # Boost confidence based on evidence count
                    ev_count = len(skill_map[norm_tech].evidence)
                    skill_map[norm_tech].confidence = min(0.95, 0.50 + (ev_count * 0.20))
                else:
                    skill_map[norm_tech] = TechnicalSkill(
                        name=norm_tech,
                        proficiency="Intermediate",
                        confidence=0.70,  # Project-backed skill starts higher
                        evidence=[evidence_item],
                    )

        return list(skill_map.values())

    def _infer_experience_level(
        self, projects: List[Project], education: List[Education], raw_background: Optional[str]
    ) -> str:
        """Infers candidate career stage from projects and background context."""
        project_count = len(projects)
        if project_count >= 5:
            return "Senior"
        elif project_count >= 2:
            return "Mid-Level"
        elif project_count == 1:
            return "Entry-Level"
        return "Student"

    def _calculate_completeness(
        self,
        target_role: str,
        career_goal: str,
        skills: List[TechnicalSkill],
        projects: List[Project],
        certifications: List[Certification],
        education: List[Education],
        raw_background: Optional[str],
    ) -> float:
        """Calculates quantitative profile completeness score (0.0 to 100.0%)."""
        score = 0.0

        if target_role and target_role.strip():
            score += 20.0
        if career_goal and career_goal.strip():
            score += 20.0
        if skills:
            score += min(25.0, len(skills) * 5.0)
        if projects:
            score += min(20.0, len(projects) * 10.0)
        if education:
            score += 10.0
        if certifications:
            score += 5.0

        return min(100.0, round(score, 1))
