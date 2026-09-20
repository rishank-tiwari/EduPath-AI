"""
Pydantic Schemas for EduPath Learner Profile & Evidence System.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator


def compute_skill_confidence(evidence: List["SkillEvidence"]) -> float:
    """
    Computes a deterministic evidence-backed confidence score between 0.40 and 0.95.

    Formula:
    - Base self-declared skill ('manual' or 'self_declared'): 0.40
    - Resume evidence ('resume'): +0.25 per item
    - Portfolio / Project evidence ('portfolio' or 'project'): +0.30 per project
    - Certification evidence ('certificate'): +0.25 per cert
    - Assessment evidence ('assessment'): +0.35 per assessment
    - Capped at maximum 0.95.
    """
    if not evidence:
        return 0.40

    score = 0.40
    for ev in evidence:
        stype = (ev.source_type or "").lower()
        if stype in ("portfolio", "project"):
            score += 0.30
        elif stype == "certificate":
            score += 0.25
        elif stype == "assessment":
            score += 0.35
        elif stype in ("resume", "document"):
            score += 0.25
        elif stype in ("manual", "self_declared"):
            score += 0.05

    return min(0.95, round(score, 2))


class SkillEvidence(BaseModel):
    """Evidence backing a technical skill's existence and proficiency."""

    source_type: str = Field(
        ...,
        description="Type of evidence source: 'resume', 'portfolio', 'project', 'certificate', 'assessment', 'self_declared', or 'manual'",
    )
    source_id: Optional[str] = Field(None, description="Identifier of the source project/cert/document/submission")
    description: str = Field("", description="Contextual description of how the skill was demonstrated")
    evidence_source: Optional[str] = Field(None, description="Detailed source breakdown (e.g. 'Resume -> Project X')")
    verified: bool = Field(True, description="Whether this evidence snippet has been verified")


class TechnicalSkill(BaseModel):
    """Structured technical skill with evidence-backed confidence scoring."""

    name: str = Field(..., description="Normalized skill name (e.g., 'Python', 'PyTorch', 'FastAPI')")
    source: str = Field(
        "self_declared",
        description="Skill provenance: 'self_declared', 'resume', 'portfolio', 'certificate', 'project', or 'assessment'",
    )
    proficiency: str = Field(
        "Intermediate",
        description="Declared or inferred proficiency: 'Beginner', 'Intermediate', 'Advanced', 'Expert'",
    )
    confidence: float = Field(
        0.50,
        ge=0.0,
        le=1.0,
        description="Evidence-backed confidence score between 0.0 (unverified) and 1.0 (strongly verified)",
    )
    evidence: List[SkillEvidence] = Field(
        default_factory=list,
        description="List of concrete evidence items backing this skill",
    )
    verified: bool = Field(True, description="Whether skill is evidence-backed")

    @model_validator(mode="after")
    def calculate_confidence_if_default(self) -> "TechnicalSkill":
        """Calculates deterministic confidence if evidence is present and default confidence was passed."""
        if self.evidence and (self.confidence == 0.40 or self.confidence == 0.50):
            self.confidence = compute_skill_confidence(self.evidence)
        return self


class Education(BaseModel):
    """Educational qualification item."""

    degree: str = Field(..., description="Degree or diploma name (e.g., 'Bachelor of Science')")
    field_of_study: str = Field(..., description="Major or specialization (e.g., 'Computer Science')")
    institution: str = Field(..., description="University or educational institution name")
    graduation_year: Optional[int] = Field(None, description="Year of graduation or completion")


class Project(BaseModel):
    """Project portfolio item demonstrating practical capability."""

    project_id: Optional[str] = Field(None, description="Unique project ID")
    title: str = Field(..., description="Project title")
    description: str = Field(..., description="Detailed description of the project and responsibilities")
    technologies_used: List[str] = Field(default_factory=list, description="List of technologies and frameworks used")
    repository_url: Optional[str] = Field(None, description="GitHub or code repository URL")
    demo_url: Optional[str] = Field(None, description="Live deployment or video demo URL")


class Certification(BaseModel):
    """Professional certification or course completion record."""

    cert_id: Optional[str] = Field(None, description="Unique certification ID")
    name: str = Field(..., description="Certification name (e.g., 'AWS Certified ML Specialty')")
    issuing_organization: str = Field(..., description="Organization issuing the certificate")
    issue_date: Optional[str] = Field(None, description="Issue date string (YYYY-MM)")
    credential_id: Optional[str] = Field(None, description="Verification or credential ID")


class DocumentUploadRequest(BaseModel):
    """Payload for analyzing text/portfolio input directly."""

    user_id: str = Field(..., description="Unique learner ID")
    document_type: str = Field("resume", description="Type: 'resume', 'portfolio', 'certificate', 'project'")
    content_text: str = Field(..., description="Raw document text or project description")
    filename: Optional[str] = Field("document.txt", description="Uploaded filename")


class LearnerProfileBase(BaseModel):
    """Base fields for Learner Profile."""

    user_id: str = Field(..., description="Unique identifier of the learner")
    target_role: str = Field(..., description="Target career role (e.g., 'AI/ML Engineer')")
    career_goal: str = Field(..., description="Specific long-term or short-term career objective")
    experience_level: str = Field(
        "Entry-Level",
        description="Career stage: 'Student', 'Entry-Level', 'Mid-Level', 'Senior', 'Lead'",
    )
    education: List[Education] = Field(default_factory=list)
    technical_skills: List[TechnicalSkill] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    certifications: List[Certification] = Field(default_factory=list)
    profile_summary: Optional[str] = Field(None, description="AI-generated or user-provided bio summary")
    profile_completeness: float = Field(
        0.0,
        ge=0.0,
        le=100.0,
        description="Calculated profile completeness percentage (0.0 to 100.0%)",
    )


class LearnerProfileCreate(LearnerProfileBase):
    """Payload schema for creating or updating a learner profile."""

    pass


class LearnerProfileResponse(LearnerProfileBase):
    """Response schema for returning a stored learner profile."""

    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    model_config = ConfigDict(from_attributes=True)
