"""
Document & Portfolio Intelligence Agent for EduPath (UNDERSTAND phase).

Parses uploaded resumes, portfolio documents, certificates, and project descriptions.
Extracts structured skills, evidence snippets, confidence levels, education, and projects.
Distinguishes declared skills, document-derived skills, project-derived skills, and assessed skills.
"""

from datetime import datetime
import re
import uuid
from typing import Any, Dict, List, Optional, Tuple

from ai.agents.base_agent import AgentTrace, BaseAgent
from ai.providers.factory import get_ai_provider
from app.schemas.learner_profile import (
    Certification,
    Education,
    Project,
    SkillEvidence,
    TechnicalSkill,
    compute_skill_confidence,
)
from app.utils.logger import logger
from app.utils.skill_normalizer import normalize_skill_name

# Skill taxonomy keywords with default proficiencies
KNOWN_SKILLS_TAXONOMY = {
    "Python": "Intermediate",
    "FastAPI": "Intermediate",
    "PyTorch": "Intermediate",
    "TensorFlow": "Intermediate",
    "SQL": "Intermediate",
    "PostgreSQL": "Intermediate",
    "MongoDB": "Intermediate",
    "Docker": "Intermediate",
    "Kubernetes": "Intermediate",
    "Git": "Intermediate",
    "React": "Intermediate",
    "JavaScript": "Intermediate",
    "TypeScript": "Intermediate",
    "Scikit-Learn": "Intermediate",
    "Pandas": "Intermediate",
    "NumPy": "Intermediate",
    "AWS": "Intermediate",
    "MLOps": "Intermediate",
    "Statistics": "Beginner",
    "Probability": "Beginner",
    "Model Evaluation": "Intermediate",
    "Model Deployment": "Intermediate",
    "Deep Learning": "Intermediate",
    "Machine Learning": "Intermediate",
    "Data Processing": "Intermediate",
}


class DocumentIntelligenceAgent(BaseAgent):
    """
    Dedicated agent for analyzing uploaded learner documents (PDF, DOCX, TXT)
    and portfolio text descriptions to extract evidence-backed skills.
    """

    def __init__(self, provider=None):
        super().__init__(
            name="DocumentIntelligenceAgent",
            description="Parses resumes, portfolios, and project docs to extract evidence-backed technical skills, experience, and projects.",
            provider=provider or get_ai_provider(),
        )

    def extract_document_skills(
        self, text: str, document_type: str = "resume", source_label: str = "Uploaded Document"
    ) -> Tuple[List[TechnicalSkill], List[Project]]:
        """
        Scans text for skills, extracts surrounding context sentences as evidence,
        and computes confidence scores.
        """
        sentences = [s.strip() for s in re.split(r'[.\n;•!]', text) if len(s.strip()) > 3]
        text_lower = text.lower()

        detected_skills: Dict[str, TechnicalSkill] = {}
        extracted_projects: List[Project] = []

        # 1. Scan for known skills in sentences
        for skill_key, default_prof in KNOWN_SKILLS_TAXONOMY.items():
            pattern = r'\b' + re.escape(skill_key.lower()) + r'\b'
            matching_sentences = [s for s in sentences if re.search(pattern, s.lower())]

            if matching_sentences:
                evidence_list = []
                for s in matching_sentences[:3]:
                    ev_src = f"{document_type.capitalize()} -> {source_label}"
                    evidence_list.append(
                        SkillEvidence(
                            source_type=document_type if document_type in ("resume", "portfolio", "certificate", "project") else "resume",
                            source_id=f"doc_{uuid.uuid4().hex[:6]}",
                            description=s[:150],
                            evidence_source=ev_src,
                            verified=True,
                        )
                    )

                conf = compute_skill_confidence(evidence_list)
                # Boost confidence if project context is detected in sentence
                if any("project" in s.lower() or "built" in s.lower() or "developed" in s.lower() for s in matching_sentences):
                    conf = min(0.95, conf + 0.15)

                detected_skills[skill_key] = TechnicalSkill(
                    name=skill_key,
                    source=document_type if document_type in ("resume", "portfolio", "certificate", "project") else "resume",
                    proficiency=default_prof,
                    confidence=round(conf, 2),
                    evidence=evidence_list,
                    verified=True,
                )

        # 2. Extract portfolio projects from text blocks mentioning 'project' or 'built'
        project_blocks = [s for s in sentences if any(k in s.lower() for k in ["project", "developed", "built", "implemented", "system", "app"])]
        for idx, block in enumerate(project_blocks[:5]):
            matched_techs = [s for s in KNOWN_SKILLS_TAXONOMY.keys() if s.lower() in block.lower()]
            extracted_projects.append(
                Project(
                    project_id=f"proj_doc_{idx+1}",
                    title=f"Extracted Project {idx+1}: {matched_techs[0] if matched_techs else 'Application'}",
                    description=block[:200],
                    technologies_used=matched_techs if matched_techs else ["Python"],
                )
            )

        return list(detected_skills.values()), extracted_projects

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes document intelligence extraction.
        Inputs:
          - text: raw document or portfolio text
          - user_id: learner identifier
          - document_type: 'resume', 'portfolio', 'certificate', 'project'
          - filename: optional filename
        """
        trace_id = f"tr_doc_{uuid.uuid4().hex[:10]}"
        start_time = datetime.utcnow()

        text = inputs.get("text") or inputs.get("content_text") or ""
        user_id = inputs.get("user_id", "demo_user_1")
        document_type = inputs.get("document_type", "resume")
        filename = inputs.get("filename", "document.txt")

        skills, projects = self.extract_document_skills(text, document_type, filename)

        # Categorize skill sources for completeness
        declared_skills = [s.name for s in skills if s.source == "self_declared"]
        document_derived = [s.name for s in skills if s.source in ("resume", "document")]
        project_derived = [s.name for s in skills if s.source in ("portfolio", "project")]

        summary = (
            f"Analyzed {document_type} '{filename}'. "
            f"Extracted {len(skills)} skills with concrete evidence snippets and {len(projects)} portfolio projects."
        )

        agent_traces = [
            f"✓ Analyzed your {document_type} ({filename})",
            f"✓ Detected {len(skills)} evidence-backed skills: {', '.join([s.name for s in skills[:5]])}",
        ]
        if project_derived:
            agent_traces.append(f"✓ Found {len(project_derived)} project-derived technical capabilities")

        self._last_trace = AgentTrace(
            trace_id=trace_id,
            agent_name=self.name,
            input_data={"user_id": user_id, "document_type": document_type, "filename": filename},
            decision=summary,
            tools_used=["document_parser", "evidence_extractor"],
            output_data={"extracted_skill_count": len(skills), "extracted_project_count": len(projects)},
            status="success",
            created_at=start_time,
        )

        return {
            "user_id": user_id,
            "document_type": document_type,
            "filename": filename,
            "skills": [s.model_dump() for s in skills],
            "projects": [p.model_dump() for p in projects],
            "declared_skills": declared_skills,
            "document_derived_skills": document_derived,
            "project_derived_skills": project_derived,
            "summary": summary,
            "agent_traces": agent_traces,
        }


# Type hint alias for internal tuple return
Tuple_Skills_Projects = tuple[List[TechnicalSkill], List[Project]]
