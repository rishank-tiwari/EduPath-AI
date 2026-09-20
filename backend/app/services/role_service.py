"""
Role Requirement Service for EduPath.

Provides a clean abstraction for career role skill benchmarks and target requirements.
"""

from typing import Dict, List, Optional
from app.schemas.role_requirement import RoleRequirement, RoleSkillRequirement


class RoleRequirementService:
    """Service providing benchmark skill requirements for target career roles."""

    def __init__(self):
        self._role_database: Dict[str, RoleRequirement] = {}
        self._initialize_foundational_roles()

    def _initialize_foundational_roles(self):
        """Initializes foundational role datasets (AI/ML Engineer, Backend Developer, Frontend Developer, Data Scientist)."""
        ai_ml_engineer = RoleRequirement(
            role_name="AI/ML Engineer",
            description="Designs, builds, evaluates, and deploys machine learning models and intelligent agent systems.",
            required_skills=[
                RoleSkillRequirement(name="Python", required_proficiency="Intermediate", importance="high"),
                RoleSkillRequirement(name="Machine Learning", required_proficiency="Intermediate", importance="high", prerequisites=["Python"]),
                RoleSkillRequirement(name="Statistics", required_proficiency="Intermediate", importance="high"),
                RoleSkillRequirement(name="Probability", required_proficiency="Intermediate", importance="medium", prerequisites=["Statistics"]),
                RoleSkillRequirement(name="Data Processing", required_proficiency="Intermediate", importance="medium", prerequisites=["Python"]),
                RoleSkillRequirement(name="Deep Learning", required_proficiency="Intermediate", importance="medium", prerequisites=["Machine Learning", "Python"]),
                RoleSkillRequirement(name="SQL", required_proficiency="Intermediate", importance="medium"),
                RoleSkillRequirement(name="Model Evaluation", required_proficiency="Intermediate", importance="high", prerequisites=["Machine Learning"]),
                RoleSkillRequirement(name="MLOps", required_proficiency="Beginner", importance="medium", prerequisites=["Python"]),
                RoleSkillRequirement(name="Model Deployment", required_proficiency="Beginner", importance="medium", prerequisites=["Python"]),
                RoleSkillRequirement(name="Git", required_proficiency="Beginner", importance="low"),
            ],
        )

        backend_developer = RoleRequirement(
            role_name="Backend Developer",
            description="Builds scalable server-side applications, REST APIs, databases, and microservices.",
            required_skills=[
                RoleSkillRequirement(name="Python", required_proficiency="Intermediate", importance="high"),
                RoleSkillRequirement(name="SQL", required_proficiency="Intermediate", importance="high"),
                RoleSkillRequirement(name="FastAPI", required_proficiency="Intermediate", importance="medium", prerequisites=["Python"]),
                RoleSkillRequirement(name="JavaScript", required_proficiency="Beginner", importance="medium"),
                RoleSkillRequirement(name="Git", required_proficiency="Intermediate", importance="high"),
                RoleSkillRequirement(name="REST APIs", required_proficiency="Intermediate", importance="high"),
                RoleSkillRequirement(name="Database Design", required_proficiency="Intermediate", importance="high", prerequisites=["SQL"]),
            ],
        )

        frontend_developer = RoleRequirement(
            role_name="Frontend Developer",
            description="Creates interactive user interfaces, web applications, and responsive design systems.",
            required_skills=[
                RoleSkillRequirement(name="JavaScript", required_proficiency="Intermediate", importance="high"),
                RoleSkillRequirement(name="React", required_proficiency="Intermediate", importance="high", prerequisites=["JavaScript"]),
                RoleSkillRequirement(name="HTML/CSS", required_proficiency="Intermediate", importance="high"),
                RoleSkillRequirement(name="Git", required_proficiency="Intermediate", importance="medium"),
                RoleSkillRequirement(name="REST APIs", required_proficiency="Beginner", importance="medium"),
            ],
        )

        data_scientist = RoleRequirement(
            role_name="Data Scientist",
            description="Extracts insights from structured/unstructured data using statistics and machine learning.",
            required_skills=[
                RoleSkillRequirement(name="Python", required_proficiency="Intermediate", importance="high"),
                RoleSkillRequirement(name="SQL", required_proficiency="Intermediate", importance="high"),
                RoleSkillRequirement(name="Statistics", required_proficiency="Intermediate", importance="high"),
                RoleSkillRequirement(name="Machine Learning", required_proficiency="Intermediate", importance="high", prerequisites=["Python", "Statistics"]),
                RoleSkillRequirement(name="Data Processing", required_proficiency="Intermediate", importance="high", prerequisites=["Python"]),
                RoleSkillRequirement(name="Git", required_proficiency="Beginner", importance="low"),
            ],
        )

        # Register roles
        for role in [ai_ml_engineer, backend_developer, frontend_developer, data_scientist]:
            key = role.role_name.strip().lower()
            self._role_database[key] = role

        # Aliases
        self._role_database["aiml engineer"] = ai_ml_engineer
        self._role_database["machine learning engineer"] = ai_ml_engineer
        self._role_database["backend dev"] = backend_developer
        self._role_database["frontend dev"] = frontend_developer

    def get_role_requirements(self, role_name: str) -> RoleRequirement:
        """
        Retrieves benchmark requirements for a given target role name.
        If role is not specifically configured, returns a fallback default role schema.
        """
        norm_key = (role_name or "").strip().lower()
        if norm_key in self._role_database:
            return self._role_database[norm_key]

        # General Fallback for unconfigured role names
        return RoleRequirement(
            role_name=role_name or "Software Engineer",
            description=f"Standard technical requirements benchmark for {role_name}.",
            required_skills=[
                RoleSkillRequirement(name="Python", required_proficiency="Intermediate", importance="high"),
                RoleSkillRequirement(name="SQL", required_proficiency="Intermediate", importance="high"),
                RoleSkillRequirement(name="JavaScript", required_proficiency="Beginner", importance="medium"),
                RoleSkillRequirement(name="Git", required_proficiency="Beginner", importance="medium"),
                RoleSkillRequirement(name="Machine Learning", required_proficiency="Intermediate", importance="medium"),
                RoleSkillRequirement(name="Statistics", required_proficiency="Intermediate", importance="medium"),
            ],
        )

    def register_role(self, role: RoleRequirement):
        """Allows dynamic registration of new target role benchmarks."""
        key = role.role_name.strip().lower()
        self._role_database[key] = role


role_service = RoleRequirementService()
