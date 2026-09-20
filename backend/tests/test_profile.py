"""
Unit & Integration Tests for EduPath Learner Profile & Profile Agent.
"""

import mongomock
import pytest
from fastapi.testclient import TestClient
from app.core.database import db_manager
from app.main import app
from app.schemas.learner_profile import (
    LearnerProfileCreate,
    SkillEvidence,
    TechnicalSkill,
)

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


def test_mongodb_failure_raises_503_and_does_not_persist_in_memory():
    """Verify that when MongoDB is disconnected, API returns 503 Service Unavailable instead of silently saving in memory."""
    # Force MongoDB disconnected state
    db_manager.db = None
    db_manager.client = None

    payload = {
        "user_id": "test_db_down_user",
        "target_role": "Backend Developer",
        "career_goal": "Master FastAPI",
    }

    # 1. POST /api/v1/profile fails with 503
    res_post = client.post("/api/v1/profile", json=payload)
    assert res_post.status_code == 503
    assert "Database service unavailable" in res_post.json()["detail"]

    # 2. GET /api/v1/profile fails with 503 (no in-memory cache return)
    res_get = client.get("/api/v1/profile?user_id=test_db_down_user")
    assert res_get.status_code == 503
    assert "Database service unavailable" in res_get.json()["detail"]


def test_learner_profile_schema_validation():
    """Verify evidence-backed technical skill schema initialization."""
    evidence = SkillEvidence(
        source_type="project",
        source_id="proj_101",
        description="Built PyTorch model engine",
    )
    skill = TechnicalSkill(
        name="PyTorch",
        proficiency="Intermediate",
        confidence=0.85,
        evidence=[evidence],
    )
    assert skill.name == "PyTorch"
    assert skill.confidence == 0.85
    assert len(skill.evidence) == 1
    assert skill.evidence[0].source_type == "project"


def test_health_check_endpoint():
    """1. Test GET /api/v1/health endpoint."""
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "database" in data


def test_create_and_get_learner_profile():
    """2. Test POST /api/v1/profile and 3. GET /api/v1/profile endpoints."""
    payload = {
        "user_id": "test_user_99",
        "target_role": "AI/ML Engineer",
        "career_goal": "Build production LLM applications",
        "experience_level": "Mid-Level",
        "education": [
            {
                "degree": "B.Tech",
                "field_of_study": "Computer Science Engineering",
                "institution": "Example University",
                "graduation_year": 2026,
            }
        ],
        "technical_skills": [
            {
                "name": "Python",
                "proficiency": "Advanced",
                "confidence": 0.90,
                "evidence": [
                    {
                        "source_type": "project",
                        "source_id": "proj_1",
                        "description": "Primary backend language",
                    }
                ],
            }
        ],
        "projects": [
            {
                "title": "EduPath Platform",
                "description": "Agentic career learning engine",
                "technologies_used": ["Python", "FastAPI"],
            }
        ],
    }

    # 2. Create Profile
    res_create = client.post("/api/v1/profile", json=payload)
    assert res_create.status_code == 201
    data_create = res_create.json()
    assert data_create["user_id"] == "test_user_99"
    assert data_create["target_role"] == "AI/ML Engineer"
    assert data_create["education"][0]["degree"] == "B.Tech"
    assert data_create["technical_skills"][0]["name"] == "Python"
    assert data_create["technical_skills"][0]["confidence"] == 0.90
    assert data_create["profile_completeness"] > 0

    # 3. Retrieve Profile
    res_get = client.get("/api/v1/profile?user_id=test_user_99")
    assert res_get.status_code == 200
    data_get = res_get.json()
    assert data_get["user_id"] == "test_user_99"
    assert data_get["career_goal"] == "Build production LLM applications"


def test_update_and_get_learner_profile():
    """4. Test Update profile and 5. GET profile again."""
    initial_payload = {
        "user_id": "test_user_update",
        "target_role": "Frontend Engineer",
        "career_goal": "Learn React and Tailwind",
    }
    client.post("/api/v1/profile", json=initial_payload)

    updated_payload = {
        "user_id": "test_user_update",
        "target_role": "Full Stack AI Engineer",
        "career_goal": "Build Agentic AI Web Apps",
        "experience_level": "Senior",
        "technical_skills": [
            {
                "name": "React",
                "proficiency": "Advanced",
                "evidence": [{"source_type": "project", "source_id": "proj_react", "description": "Built UI"}],
            }
        ],
    }

    # 4. Update Profile
    res_update = client.post("/api/v1/profile", json=updated_payload)
    assert res_update.status_code == 201
    data_update = res_update.json()
    assert data_update["target_role"] == "Full Stack AI Engineer"
    assert data_update["technical_skills"][0]["confidence"] >= 0.65  # Deterministic base + project evidence

    # 5. GET profile again
    res_get_updated = client.get("/api/v1/profile?user_id=test_user_update")
    assert res_get_updated.status_code == 200
    data_get_updated = res_get_updated.json()
    assert data_get_updated["target_role"] == "Full Stack AI Engineer"
    assert data_get_updated["experience_level"] == "Senior"


def test_profile_agent_analyze_endpoint():
    """6. Test POST /api/v1/profile/analyze Profile Agent execution."""
    analyze_input = {
        "user_id": "test_agent_user_1",
        "target_role": "AI/ML Engineer",
        "career_goal": "Master LLM agent orchestration",
        "declared_skills": ["Python", "PyTorch"],
        "declared_projects": [
            {
                "title": "RAG Search Engine",
                "description": "Built vector search with PyTorch embeddings",
                "technologies_used": ["Python", "PyTorch", "FastAPI"],
            }
        ],
        "declared_education": [
            {
                "degree": "M.S.",
                "field_of_study": "Artificial Intelligence",
                "institution": "Tech Institute",
                "graduation_year": 2025,
            }
        ],
    }

    response = client.post("/api/v1/profile/analyze", json=analyze_input)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_agent_user_1"
    assert data["profile_completeness"] > 0
    assert len(data["technical_skills"]) >= 2
    assert data["education"][0]["degree"] == "M.S."

    # Check evidence association and deterministic confidence boosting
    pytorch_skill = next((s for s in data["technical_skills"] if s["name"] == "PyTorch"), None)
    assert pytorch_skill is not None
    assert pytorch_skill["confidence"] > 0.40  # Project evidence boosted confidence
    assert len(pytorch_skill["evidence"]) >= 1


def test_invalid_profile_inputs():
    """7. Verify validation error handling for invalid/missing mandatory fields."""
    # Missing required user_id, target_role, career_goal
    res1 = client.post("/api/v1/profile", json={"experience_level": "Senior"})
    assert res1.status_code == 422

    # Education is not a list
    res2 = client.post(
        "/api/v1/profile",
        json={
            "user_id": "u1",
            "target_role": "Role",
            "career_goal": "Goal",
            "education": "B.Tech CS",  # Invalid type
        },
    )
    assert res2.status_code == 422

    # Project item missing required title
    res3 = client.post(
        "/api/v1/profile",
        json={
            "user_id": "u2",
            "target_role": "Role",
            "career_goal": "Goal",
            "projects": [{"description": "Missing title"}],
        },
    )
    assert res3.status_code == 422


def test_minimal_valid_profile_request():
    """8. Verify profile creation with missing optional fields (valid minimal request)."""
    minimal_payload = {
        "user_id": "minimal_user",
        "target_role": "Data Scientist",
        "career_goal": "Analyze datasets",
    }
    response = client.post("/api/v1/profile", json=minimal_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == "minimal_user"
    assert data["education"] == []
    assert data["technical_skills"] == []
    assert data["projects"] == []
    assert data["profile_completeness"] == 40.0  # 20 target_role + 20 career_goal
