"""
Project Idea Generation Agent for EduPath (PRACTICE phase).

Generates practical, targeted portfolio project recommendations based on target role,
identified skill gaps, current skill level, and completed learning activities.
"""

from datetime import datetime
import uuid
from typing import Any, Dict, List, Optional

from ai.agents.base_agent import BaseAgent
from ai.providers.factory import get_ai_provider
from app.utils.logger import logger


class ProjectAgent(BaseAgent):
    """
    Generates personalized portfolio project ideas to help learners close specific skill gaps.
    """

    def __init__(self, provider=None):
        super().__init__(
            name="ProjectAgent",
            description="Generates targeted portfolio project ideas and technical specifications matching learner skill gaps and target role.",
            provider=provider or get_ai_provider(),
        )

    def generate_project_ideas(
        self,
        target_role: str,
        skill_gaps: List[str],
        experience_level: str = "Entry-Level",
        completed_skills: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Generates structured project proposals tailored to target role and skill gaps.
        """
        completed = completed_skills or []
        gaps = [g.strip() for g in skill_gaps if g.strip()]
        if not gaps:
            gaps = ["Statistics", "Model Evaluation", "MLOps"]

        projects = []

        # Project 1: Model Evaluation & Statistics Dashboard
        if any(s in ["Statistics", "Probability", "Model Evaluation", "Machine Learning"] for s in gaps):
            projects.append(
                {
                    "project_id": f"proj_gen_{uuid.uuid4().hex[:8]}",
                    "title": "ML Model Evaluation & Statistics Dashboard",
                    "objective": "Build a comprehensive model evaluation suite that calculates precision, recall, ROC-AUC, and confidence intervals across classification models.",
                    "skills_practiced": ["Statistics", "Model Evaluation", "Python", "Data Processing"],
                    "difficulty": "Intermediate",
                    "estimated_duration": "4 - 6 hours",
                    "prerequisites": ["Python", "Pandas", "Scikit-Learn Basics"],
                    "expected_outcome": "An interactive web dashboard evaluating binary ML classifiers with statistical significance tests.",
                    "suggested_tech_stack": ["Python", "FastAPI", "Scikit-Learn", "Streamlit"],
                    "optional_challenge": "Add automated drift detection using Kolmogorov-Smirnov statistical tests.",
                }
            )

        # Project 2: MLOps Pipeline & Model Registry
        if any(s in ["MLOps", "Model Deployment", "Docker", "Data Processing"] for s in gaps):
            projects.append(
                {
                    "project_id": f"proj_gen_{uuid.uuid4().hex[:8]}",
                    "title": "Production MLOps Pipeline & FastAPI Serving Engine",
                    "objective": "Design an automated model training, packaging, and serving API with versioning and continuous health checks.",
                    "skills_practiced": ["MLOps", "Model Deployment", "Docker", "FastAPI"],
                    "difficulty": "Intermediate",
                    "estimated_duration": "6 - 8 hours",
                    "prerequisites": ["Python", "Docker Basics", "REST APIs"],
                    "expected_outcome": "Containerized FastAPI microservice serving real-time model inference with latency monitoring.",
                    "suggested_tech_stack": ["Python", "FastAPI", "Docker", "Prometheus"],
                    "optional_challenge": "Implement zero-downtime rolling updates using Docker Compose or Kubernetes.",
                }
            )

        # Project 3: Deep Learning / NLP Feature Extractor
        if any(s in ["Deep Learning", "PyTorch", "Data Processing", "TensorFlow"] for s in gaps) or "Senior" in experience_level:
            projects.append(
                {
                    "project_id": f"proj_gen_{uuid.uuid4().hex[:8]}",
                    "title": "Neural Feature Extraction & Embedding Engine",
                    "objective": "Train a custom PyTorch autoencoder or fine-tune an embedding model to vectorize unstructured documents.",
                    "skills_practiced": ["Deep Learning", "PyTorch", "Data Processing"],
                    "difficulty": "Advanced" if "Senior" in experience_level else "Intermediate",
                    "estimated_duration": "8 hours",
                    "prerequisites": ["Python", "PyTorch Tensors"],
                    "expected_outcome": "End-to-end vector search indexing module backed by PyTorch embeddings.",
                    "suggested_tech_stack": ["PyTorch", "Python", "NumPy", "FAISS"],
                    "optional_challenge": "Benchmark GPU inference speed vs CPU vector search throughput.",
                }
            )

        # Project 4: Generic fallback portfolio project matching target role
        if not projects:
            projects.append(
                {
                    "project_id": f"proj_gen_{uuid.uuid4().hex[:8]}",
                    "title": f"End-to-End {target_role} Benchmark Suite",
                    "objective": f"Develop a production-grade benchmark application for {target_role} addressing key operational workflows.",
                    "skills_practiced": gaps[:3],
                    "difficulty": "Intermediate",
                    "estimated_duration": "5 hours",
                    "prerequisites": ["Python", "Git"],
                    "expected_outcome": "Fully tested repository demonstrating hands-on proficiency in target skills.",
                    "suggested_tech_stack": ["Python", "Git", "pytest"],
                    "optional_challenge": "Deploy application to cloud staging environment with automated CI/CD.",
                }
            )

        return projects

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Base agent execution handler."""
        target_role = inputs.get("target_role", "AI/ML Engineer")
        skill_gaps = inputs.get("skill_gaps", ["Statistics", "Model Evaluation"])
        experience_level = inputs.get("experience_level", "Entry-Level")
        completed_skills = inputs.get("completed_skills", [])

        projects = self.generate_project_ideas(
            target_role=target_role,
            skill_gaps=skill_gaps,
            experience_level=experience_level,
            completed_skills=completed_skills,
        )

        return {
            "target_role": target_role,
            "skill_gaps": skill_gaps,
            "projects": projects,
        }
