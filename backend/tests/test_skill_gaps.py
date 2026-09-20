"""
Unit & Integration Tests for EduPath Skill Gap Agent & Skill Gap Intelligence Foundation.
"""

import mongomock
import pytest
from fastapi.testclient import TestClient
from app.core.database import db_manager
from app.main import app
from app.schemas.learner_profile import SkillEvidence, TechnicalSkill
from app.schemas.skill_gap import SkillGapItem, SkillGapResponse
from app.services.profile_service import profile_service
from app.services.role_service import role_service
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


def test_skill_gap_schema_validation():
    """1. Test Skill Gap Pydantic model initialization and validation."""
    evidence = SkillEvidence(source_type="project", source_id="p1", description="Built FastAPI API")
    item = SkillGapItem(
        skill_name="Python",
        required_proficiency="Intermediate",
        current_proficiency="Advanced",
        gap_status="strong",
        priority="low",
        importance="high",
        reason="Python exceeds requirement",
        evidence=[evidence],
    )
    assert item.skill_name == "Python"
    assert item.gap_status == "strong"
    assert item.priority == "low"
    assert len(item.evidence) == 1


def test_role_requirements_ai_ml_engineer():
    """2. Test AI/ML Engineer benchmark role requirements loading."""
    req = role_service.get_role_requirements("AI/ML Engineer")
    assert req.role_name == "AI/ML Engineer"
    skill_names = [s.name for s in req.required_skills]
    assert "Python" in skill_names
    assert "Machine Learning" in skill_names
    assert "Statistics" in skill_names
    assert "Deep Learning" in skill_names


def test_skill_normalization():
    """3. Test Skill Normalization Engine alias resolutions."""
    assert normalize_skill_name("Python Programming") == "Python"
    assert normalize_skill_name("python3") == "Python"
    assert normalize_skill_name("ML") == "Machine Learning"
    assert normalize_skill_name("PyTorch") == "Deep Learning"
    assert normalize_skill_name("Stats") == "Statistics"
    assert normalize_skill_name("Custom Novel Skill") == "Custom Novel Skill"


def test_skill_gap_analysis_flow_and_classifications():
    """4-9. Test gap classifications, priority formulas, evidence preservation, and readiness scoring."""
    # Seed learner profile in Task 1.1 Profile Service
    profile_payload = {
        "user_id": "test_gap_user_1",
        "target_role": "AI/ML Engineer",
        "career_goal": "Become ML Engineer",
        "technical_skills": [
            {
                "name": "Python",
                "proficiency": "Advanced",
                "confidence": 0.90,
                "evidence": [{"source_type": "project", "source_id": "p1", "description": "Backend engine"}],
            },
            {
                "name": "Machine Learning",
                "proficiency": "Intermediate",
                "confidence": 0.70,
                "evidence": [{"source_type": "project", "source_id": "p2", "description": "Trained models"}],
            },
            {
                "name": "Statistics",
                "proficiency": "Beginner",
                "confidence": 0.40,
                "evidence": [],
            },
        ],
    }
    profile_service.save_profile(profile_payload)

    # Execute Skill Gap API Analysis
    response = client.post("/api/v1/skill-gaps/analyze?user_id=test_gap_user_1")
    assert response.status_code == 200
    data = response.json()

    assert data["user_id"] == "test_gap_user_1"
    assert data["target_role"] == "AI/ML Engineer"
    assert data["overall_readiness"] > 0.0

    skills = {item["skill_name"]: item for item in data["skills"]}

    # 4. Test Strong classification
    assert skills["Python"]["gap_status"] == "strong"
    assert skills["Python"]["priority"] == "low"
    # 9. Test Evidence preservation
    assert len(skills["Python"]["evidence"]) == 1
    assert skills["Python"]["evidence"][0]["source_id"] == "p1"

    # 5. Test Meets Requirement classification
    assert skills["Machine Learning"]["gap_status"] == "meets_requirement"
    assert skills["Machine Learning"]["priority"] == "low"

    # 6. Test Needs Improvement classification
    assert skills["Statistics"]["gap_status"] == "needs_improvement"
    assert skills["Statistics"]["priority"] == "high"  # High importance + needs_improvement

    # 7. Test Missing classification
    assert skills["Deep Learning"]["gap_status"] == "missing"
    assert len(skills["Deep Learning"]["evidence"]) == 0


def test_missing_learner_profile_returns_400():
    """10. Test error handling when learner profile does not exist."""
    res = client.post("/api/v1/skill-gaps/analyze?user_id=non_existent_user_99")
    assert res.status_code == 400
    assert "Learner profile is required before skill-gap analysis" in res.json()["detail"]


def test_missing_target_role_returns_400():
    """11. Test error handling when learner profile lacks a target_role."""
    profile_payload = {
        "user_id": "no_role_user",
        "target_role": "   ",  # Blank role
        "career_goal": "Goal",
    }
    profile_service.save_profile(profile_payload)

    res = client.post("/api/v1/skill-gaps/analyze?user_id=no_role_user")
    assert res.status_code == 400
    assert "does not have a valid target_role specified" in res.json()["detail"]


def test_skill_gap_api_and_retrieval():
    """12-14. Test POST analyze, GET list, and GET single skill item API endpoints."""
    # Seed profile
    profile_service.save_profile({
        "user_id": "test_api_gap_user",
        "target_role": "AI/ML Engineer",
        "career_goal": "Build Agentic AI",
    })

    # 12. POST analyze
    res_post = client.post("/api/v1/skill-gaps/analyze?user_id=test_api_gap_user")
    assert res_post.status_code == 200
    post_data = res_post.json()
    assert post_data["user_id"] == "test_api_gap_user"

    # 13. GET skill gaps list
    res_get = client.get("/api/v1/skill-gaps?user_id=test_api_gap_user")
    assert res_get.status_code == 200
    get_data = res_get.json()
    assert get_data["user_id"] == "test_api_gap_user"
    assert len(get_data["skills"]) >= 4

    # 14. GET single skill item
    res_single = client.get("/api/v1/skill-gaps/Python?user_id=test_api_gap_user")
    assert res_single.status_code == 200
    single_data = res_single.json()
    assert single_data["skill_name"] == "Python"


def test_skill_gap_mongodb_unavailable_returns_503():
    """15. Test that when MongoDB is disconnected, API returns 503 Service Unavailable."""
    # Force MongoDB disconnected state
    db_manager.db = None
    db_manager.client = None

    res_post = client.post("/api/v1/skill-gaps/analyze?user_id=any_user")
    assert res_post.status_code == 503
    assert "Database service unavailable" in res_post.json()["detail"]

    res_get = client.get("/api/v1/skill-gaps?user_id=any_user")
    assert res_get.status_code == 503
    assert "Database service unavailable" in res_get.json()["detail"]
