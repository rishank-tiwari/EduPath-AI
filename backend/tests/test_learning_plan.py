"""
Unit & Integration Tests for EduPath Learning Planner & Learning Plan Foundation.
"""

import mongomock
import pytest
from fastapi.testclient import TestClient
from app.core.database import db_manager
from app.main import app
from app.schemas.learning_plan import LearningModule, LearningPlanResponse, LearningTask
from app.services.prerequisite_service import prerequisite_service
from app.services.profile_service import profile_service
from app.services.skill_gap_service import skill_gap_service

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


def test_learning_plan_schema_validation():
    """1. Test Learning Plan Pydantic model initialization and validation."""
    task = LearningTask(
        task_id="t1",
        title="Learn Statistics",
        description="Study statistics basics",
        task_type="learn",
        estimated_minutes=45,
        skill_name="Statistics",
        difficulty="Intermediate",
        status="not_started",
    )
    module = LearningModule(
        module_id="m1",
        title="Statistics Foundations",
        description="Master statistics",
        skill_name="Statistics",
        priority="high",
        week_number=1,
        estimated_hours=3.5,
        prerequisites=["Probability"],
        tasks=[task],
        status="not_started",
    )
    plan = LearningPlanResponse(
        plan_id="p1",
        user_id="test_user_schema",
        target_role="AI/ML Engineer",
        title="AI/ML Roadmap",
        summary="Test summary",
        total_estimated_hours=3.5,
        duration_weeks=1,
        modules=[module],
        version=1,
    )
    assert plan.plan_id == "p1"
    assert plan.version == 1
    assert len(plan.modules) == 1
    assert plan.modules[0].tasks[0].task_type == "learn"


def test_prerequisite_ordering_logic():
    """2. Test prerequisite topological sorting engine."""
    skills = ["Deep Learning", "Machine Learning", "Python", "Statistics"]
    ordered = prerequisite_service.order_by_prerequisites(skills)
    
    # Python and Statistics must come before Machine Learning
    assert ordered.index("Python") < ordered.index("Machine Learning")
    assert ordered.index("Statistics") < ordered.index("Machine Learning")
    # Machine Learning must come before Deep Learning
    assert ordered.index("Machine Learning") < ordered.index("Deep Learning")


def test_missing_learner_profile_returns_400():
    """3. Test generating plan without existing learner profile returns 400 Bad Request."""
    res = client.post("/api/v1/plans/generate?user_id=non_existent_plan_user")
    assert res.status_code == 400
    assert "Learner profile for user_id 'non_existent_plan_user' not found" in res.json()["detail"]


def test_missing_skill_gap_analysis_returns_400():
    """4. Test generating plan with profile but missing skill gap analysis returns 400 Bad Request."""
    # Create profile only
    profile_payload = {
        "user_id": "user_no_gap",
        "target_role": "AI/ML Engineer",
        "career_goal": "Become ML Engineer",
        "experience_level": "Entry-Level",
    }
    client.post("/api/v1/profile", json=profile_payload)

    res = client.post("/api/v1/plans/generate?user_id=user_no_gap")
    assert res.status_code == 400
    assert "Skill gap analysis for user_id 'user_no_gap' not found" in res.json()["detail"]


def test_full_plan_generation_flow_and_skipping_satisfied_skills():
    """5. Test end-to-end plan generation, prerequisite ordering, skipping satisfied skills, and tasks."""
    user_id = "test_planner_user_1"

    # 1. Save profile with Python Advanced, PyTorch Beginner, no ML/Statistics
    profile_payload = {
        "user_id": user_id,
        "target_role": "AI/ML Engineer",
        "career_goal": "Become ML Engineer",
        "experience_level": "Entry-Level",
        "technical_skills": [
            {
                "name": "Python",
                "proficiency": "Advanced",
                "confidence": 0.9,
                "evidence": [{"source_type": "project", "source_id": "p1", "description": "Built Python API"}]
            },
            {
                "name": "PyTorch",
                "proficiency": "Beginner",
                "confidence": 0.5,
                "evidence": [{"source_type": "project", "source_id": "p1", "description": "Built basic NN"}]
            }
        ]
    }
    client.post("/api/v1/profile", json=profile_payload)

    # 2. Run skill gap analysis
    res_gap = client.post(f"/api/v1/skill-gaps/analyze?user_id={user_id}")
    assert res_gap.status_code == 200

    # 3. Generate learning plan
    res_plan = client.post(f"/api/v1/plans/generate?user_id={user_id}")
    assert res_plan.status_code == 200
    plan = res_plan.json()

    assert plan["user_id"] == user_id
    assert plan["target_role"] == "AI/ML Engineer"
    assert plan["version"] == 1
    assert plan["total_estimated_hours"] > 0
    assert plan["duration_weeks"] >= 1
    assert len(plan["modules"]) > 0

    # Check that Python (satisfied/strong) is NOT created as an active study module
    module_skills = [m["skill_name"] for m in plan["modules"]]
    assert "Python" not in module_skills

    # Check task types generated inside modules
    first_mod_tasks = plan["modules"][0]["tasks"]
    task_types = set(t["task_type"] for t in first_mod_tasks)
    assert "learn" in task_types or "practice" in task_types or "project" in task_types or "review" in task_types


def test_get_plan_endpoints():
    """6. Test GET /api/v1/plans and GET /api/v1/plans/{plan_id} endpoints."""
    user_id = "test_planner_get_user"

    # Setup profile & gap analysis
    client.post("/api/v1/profile", json={
        "user_id": user_id,
        "target_role": "Backend Developer",
        "career_goal": "Master FastAPI",
    })
    client.post(f"/api/v1/skill-gaps/analyze?user_id={user_id}")
    res_gen = client.post(f"/api/v1/plans/generate?user_id={user_id}")
    gen_plan = res_gen.json()
    plan_id = gen_plan["plan_id"]

    # 1. GET /api/v1/plans?user_id=...
    res_get = client.get(f"/api/v1/plans?user_id={user_id}")
    assert res_get.status_code == 200
    assert res_get.json()["plan_id"] == plan_id

    # 2. GET /api/v1/plans/{plan_id}
    res_get_by_id = client.get(f"/api/v1/plans/{plan_id}")
    assert res_get_by_id.status_code == 200
    assert res_get_by_id.json()["user_id"] == user_id


def test_mongodb_failure_returns_503():
    """7. Test that when MongoDB is disconnected, plan endpoints raise HTTP 503 Service Unavailable."""
    db_manager.db = None
    db_manager.client = None

    res = client.get("/api/v1/plans?user_id=some_user")
    assert res.status_code == 503
    assert "Database service unavailable" in res.json()["detail"]

    res_post = client.post("/api/v1/plans/generate?user_id=some_user")
    assert res_post.status_code == 503
    assert "Database service unavailable" in res_post.json()["detail"]
