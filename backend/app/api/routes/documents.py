"""
API Routes for Document & Portfolio Intelligence System.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from ai.agents.profile.document_agent import DocumentIntelligenceAgent
from ai.agents.skill_gap.skill_gap_agent import SkillGapAgent
from app.repositories.profile_repository import profile_repository
from app.repositories.skill_gap_repository import skill_gap_repository
from app.schemas.learner_profile import DocumentUploadRequest, TechnicalSkill
from app.services.document_processor import get_document_processor
from app.services.role_service import role_service
from app.utils.logger import logger

router = APIRouter(prefix="/documents", tags=["Document Intelligence"])


@router.post("/upload", status_code=status.HTTP_200_OK)
async def upload_document(
    file: UploadFile = File(...),
    user_id: str = Form("demo_user_1"),
    document_type: str = Form("resume"),
) -> Dict[str, Any]:
    """
    POST /api/v1/documents/upload
    Uploads a document (PDF, DOCX, TXT), extracts text, runs DocumentIntelligenceAgent,
    updates LearnerProfile technical skills + evidence, and re-calculates skill gap analysis.
    """
    filename = file.filename or "document.txt"
    ext = filename.lower().split(".")[-1] if "." in filename else ""

    if ext not in ("pdf", "docx", "doc", "txt", "md", "json"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Please upload a PDF, DOCX, or TXT file.",
        )

    content_bytes = await file.read()
    if not content_bytes or len(content_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is empty. Please select a valid document.",
        )

    processor = get_document_processor()
    try:
        raw_text = await processor.extract_text(content_bytes, filename)
    except Exception as e:
        logger.error(f"Failed to extract document text for {filename}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="We couldn't read this file. Please try another PDF or DOCX.",
        )

    if ext == "pdf" and not raw_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This PDF does not contain selectable text yet. Please upload a text-based PDF or DOCX file.",
        )

    if not raw_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="We couldn't read this file. Please try another PDF or DOCX.",
        )

    agent = DocumentIntelligenceAgent()
    result = await agent.execute({
        "text": raw_text,
        "user_id": user_id,
        "document_type": document_type,
        "filename": filename,
    })

    # Save/merge into LearnerProfile
    await _merge_skills_into_profile(user_id, result["skills"], result["projects"])

    return result


@router.post("/analyze", status_code=status.HTTP_200_OK)
async def analyze_document_text(payload: DocumentUploadRequest) -> Dict[str, Any]:
    """
    POST /api/v1/documents/analyze
    Analyzes raw text content or project descriptions, extracts skills & evidence,
    updates LearnerProfile, and re-runs Skill Gap Agent.
    """
    if not payload.content_text or not payload.content_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text content is required for analysis.",
        )

    agent = DocumentIntelligenceAgent()
    result = await agent.execute({
        "text": payload.content_text,
        "user_id": payload.user_id,
        "document_type": payload.document_type,
        "filename": payload.filename or "portfolio.txt",
    })

    await _merge_skills_into_profile(payload.user_id, result["skills"], result["projects"])

    return result


async def _merge_skills_into_profile(user_id: str, new_skills: List[Dict[str, Any]], new_projects: List[Dict[str, Any]]):
    """Helper to merge newly extracted skills and projects into learner profile & recalculate skill gaps."""
    profile = profile_repository.get_by_user_id(user_id) or {
        "user_id": user_id,
        "target_role": "AI/ML Engineer",
        "career_goal": "Build production LLM and agentic AI applications",
        "experience_level": "Entry-Level",
        "technical_skills": [],
        "projects": [],
    }

    existing_skills_map = {}
    for sk in profile.get("technical_skills", []):
        if isinstance(sk, dict) and sk.get("name"):
            existing_skills_map[sk["name"].lower()] = sk

    for sk_dict in new_skills:
        name_lower = sk_dict["name"].lower()
        if name_lower in existing_skills_map:
            # Merge evidence
            existing_ev = existing_skills_map[name_lower].get("evidence", [])
            existing_ev.extend(sk_dict.get("evidence", []))
            existing_skills_map[name_lower]["evidence"] = existing_ev
            existing_skills_map[name_lower]["confidence"] = max(
                existing_skills_map[name_lower].get("confidence", 0.5), sk_dict.get("confidence", 0.7)
            )
            existing_skills_map[name_lower]["verified"] = True
            existing_skills_map[name_lower]["source"] = sk_dict.get("source", "resume")
        else:
            existing_skills_map[name_lower] = sk_dict

    merged_skills = list(existing_skills_map.values())
    profile["technical_skills"] = merged_skills

    # Merge projects
    existing_proj_titles = {p.get("title", "").lower() for p in profile.get("projects", []) if isinstance(p, dict)}
    for proj in new_projects:
        if proj.get("title", "").lower() not in existing_proj_titles:
            profile["projects"].append(proj)

    profile_repository.save_profile(profile)

    # Trigger SkillGapAgent recalculation
    try:
        role_req = role_service.get_role_requirements(profile.get("target_role", "AI/ML Engineer"))
        if role_req:
            skill_gap_agent = SkillGapAgent()
            gap_analysis = skill_gap_agent.analyze_skill_gaps(
                user_id=user_id,
                target_role=profile.get("target_role", "AI/ML Engineer"),
                learner_skills=merged_skills,
                role_requirements=role_req,
            )
            skill_gap_repository.save_skill_gap(gap_analysis.model_dump())

            try:
                from app.services.learning_plan_service import learning_plan_service
                await learning_plan_service.generate_plan(user_id)
            except Exception as plan_err:
                logger.warning(f"Plan re-generation after document upload failed: {plan_err}")
    except Exception as e:
        logger.warning(f"SkillGap re-analysis after document upload failed: {e}")
