"""
Automated unit & integration tests verifying Bug 1 (Skill Gap Data Flow & Skill Preservation)
and Bug 2 (Practice Evaluation & Adaptive Flow Integration).
"""

import asyncio
import mongomock
import pytest
from fastapi.testclient import TestClient
from app.core.database import db_manager
from app.main import app
from app.schemas.learner_profile import LearnerProfileCreate, TechnicalSkill, SkillEvidence
from app.services.profile_service import ProfileService
from app.services.skill_gap_service import SkillGapService
from app.utils.skill_normalizer import normalize_skill_name

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_mongodb():
    """Provides isolated mongomock MongoDB instance for each test."""
    mock_client = mongomock.MongoClient()
    db_manager.client = mock_client
    db_manager.db = mock_client["edupath_test"]
    yield
    db_manager.client = None
    db_manager.db = None


# --- BUG 1 TESTS ---

def test_bug1_multiple_skills_preservation_and_skill_gap_analysis():
    """Verify that selecting Python, JavaScript, SQL, PyTorch, and Git preserves all skills in profile and skill gap analysis."""
    user_id = "test_learner_bug1"
    target_role = "Backend Developer"

    selected_skills = ["Python", "JavaScript", "SQL", "PyTorch", "Git"]
    tech_skills = [
        TechnicalSkill(
            name=s,
            proficiency="Advanced" if s == "Python" else "Intermediate",
            confidence=0.9 if s == "Python" else 0.6,
            evidence=[SkillEvidence(source_type="project", description=f"Project with {s}")]
        )
        for s in selected_skills
    ]

    create_payload = LearnerProfileCreate(
        user_id=user_id,
        target_role=target_role,
        career_goal="Build high scale backend services",
        experience_level="Entry-Level",
        technical_skills=tech_skills
    )

    # 1. Save Profile
    saved_profile = ProfileService().save_profile(create_payload)
    assert saved_profile.user_id == user_id
    assert len(saved_profile.technical_skills) == 5

    # 2. Run Skill Gap Analysis
    skill_gap_service = SkillGapService()
    gap_response = asyncio.run(skill_gap_service.analyze_and_save_gaps(user_id))

    assert gap_response is not None
    analyzed_skill_names = [s.skill_name for s in gap_response.skills]

    # Verify all selected skills (or canonical normalized names) are present in analysis
    for original_skill in selected_skills:
        assert any(
            original_skill.lower() in name.lower() or normalize_skill_name(original_skill).lower() in name.lower()
            for name in analyzed_skill_names
        ), f"Selected skill '{original_skill}' missing from skill gap analysis!"


def test_bug1_skill_normalizer_does_not_discard_unrelated_skills():
    """Verify skill normalizer preserves standard skills without mapping everything to Python."""
    assert normalize_skill_name("Python") == "Python"
    assert normalize_skill_name("JavaScript") == "JavaScript"
    assert normalize_skill_name("SQL") == "SQL"
    assert normalize_skill_name("Git") == "Git"
    assert normalize_skill_name("PyTorch") == "Deep Learning"


def test_bug1_manual_onboarding_scenario_backend_developer():
    """Simulate manual test scenario: Backend Developer profile with 5 skills."""
    response = client.post("/api/v1/profile", json={
        "user_id": "test_backend_dev",
        "target_role": "Backend Developer",
        "career_goal": "Build robust web services",
        "technical_skills": [
            {"name": "Python", "proficiency": "Advanced"},
            {"name": "JavaScript", "proficiency": "Intermediate"},
            {"name": "SQL", "proficiency": "Intermediate"},
            {"name": "PyTorch", "proficiency": "Intermediate"},
            {"name": "Git", "proficiency": "Intermediate"},
        ]
    })
    assert response.status_code in (200, 201)

    gap_res = client.post(f"/api/v1/skill-gaps/analyze?user_id=test_backend_dev")
    assert gap_res.status_code == 200
    gap_data = gap_res.json()

    skill_names = [s["skill_name"] for s in gap_data["skills"]]
    assert "Python" in skill_names
    assert "SQL" in skill_names
    assert "JavaScript" in skill_names
    assert "Git" in skill_names
    assert any("Deep Learning" in s or "PyTorch" in s for s in skill_names)


# --- BUG 2 TESTS ---

def test_bug2_practice_generation_and_evaluation_flow():
    """Verify practice generation, answer evaluation, progress update, and adaptation trigger."""
    user_id = "test_practice_learner"

    # Setup profile & plan
    client.post("/api/v1/profile", json={
        "user_id": user_id,
        "target_role": "AI/ML Engineer",
        "career_goal": "Deploy production models",
        "technical_skills": [{"name": "Python", "proficiency": "Intermediate"}]
    })
    client.post(f"/api/v1/skill-gaps/analyze?user_id={user_id}")
    client.post(f"/api/v1/plans/generate?user_id={user_id}")

    # Generate practice session
    gen_res = client.post("/api/v1/practice/generate", json={
        "user_id": user_id,
        "task_id": "task_stat_01",
        "skill_name": "Statistics",
        "difficulty": "beginner"
    })
    assert gen_res.status_code == 200
    practice_data = gen_res.json()
    practice_id = practice_data["practice_id"]
    questions = practice_data["questions"]
    assert len(questions) > 0

    # Submit practice answers (deliberately incorrect to test adaptive flow)
    answers = [{"question_id": q["question_id"], "learner_answer": "Wrong answer"} for q in questions]
    sub_res = client.post(f"/api/v1/practice/{practice_id}/submit", json={
        "practice_id": practice_id,
        "user_id": user_id,
        "answers": answers
    })
    assert sub_res.status_code == 200
    result_data = sub_res.json()
    assert result_data["total_questions"] == len(questions)
    assert result_data["score"] == 0
    assert result_data["percentage"] == 0.0

    # Trigger adaptation and verify learning path update
    adapt_res = client.post("/api/v1/adaptation/analyze", json={
        "user_id": user_id,
        "skill_name": "Statistics",
        "topic": "Probability Basics"
    })
    assert adapt_res.status_code == 200
    adapt_data = adapt_res.json()
    assert adapt_data["action"] in ("review", "add_practice")
    assert adapt_data["new_plan_version"] >= 2
