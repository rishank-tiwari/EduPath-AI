"""
Unit & Integration Tests for EduPath Resource Agent, Practice Agent & Evaluation System.
"""

import mongomock
import pytest
from fastapi.testclient import TestClient
from app.core.database import db_manager
from app.main import app
from app.schemas.practice import PracticeQuestion, PracticeResultRecord, QuestionEvaluationResult
from app.schemas.resource import LearningResource, ResourceRecommendationResponse
from ai.agents.practice.practice_agent import PracticeAgent

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


def test_resource_schema_validation():
    """1. Test LearningResource Pydantic model initialization."""
    res = LearningResource(
        resource_id="r1",
        title="Python Basics Guide",
        description="Official Python docs",
        resource_type="documentation",
        url="https://docs.python.org/3/",
        skill_name="Python",
        difficulty="beginner",
        estimated_minutes=30,
        source="Python Software Foundation",
    )
    assert res.resource_id == "r1"
    assert res.skill_name == "Python"
    assert res.estimated_minutes == 30


def test_resource_recommendation_endpoint():
    """2. Test POST /api/v1/resources/recommend endpoint."""
    payload = {
        "task_id": "task_stat_101",
        "skill_name": "Statistics",
        "difficulty": "beginner",
        "user_id": "test_user_res",
    }
    res = client.post("/api/v1/resources/recommend", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["task_id"] == "task_stat_101"
    assert data["skill_name"] == "Statistics"
    assert len(data["resources"]) > 0
    assert data["resources"][0]["url"].startswith("http")


def test_missing_task_id_for_resource_recommendation():
    """3. Test resource recommendation without task_id returns 422/400."""
    payload = {
        "task_id": "",
        "skill_name": "Statistics",
    }
    res = client.post("/api/v1/resources/recommend", json=payload)
    assert res.status_code == 400
    assert "task_id is required" in res.json()["detail"]


def test_practice_schema_validation():
    """4. Test Practice schema initialization and evaluation record."""
    q_res = QuestionEvaluationResult(
        question_id="q1",
        question="What is Python?",
        correct=True,
        learner_answer="Language",
        correct_answer="Language",
        explanation="Python is a programming language.",
    )
    record = PracticeResultRecord(
        result_id="res_01",
        user_id="u1",
        practice_id="prac_01",
        task_id="t1",
        skill_name="Python",
        topic="Python Basics",
        difficulty="beginner",
        score=1,
        total_questions=1,
        percentage=100.0,
        question_results=[q_res],
    )
    assert record.score == 1
    assert record.percentage == 100.0
    assert record.question_results[0].correct is True


def test_practice_generation_endpoint():
    """5. Test POST /api/v1/practice/generate endpoint."""
    payload = {
        "user_id": "user_prac_01",
        "task_id": "task_stat_101",
        "skill_name": "Statistics",
        "difficulty": "beginner",
    }
    res = client.post("/api/v1/practice/generate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["user_id"] == "user_prac_01"
    assert data["skill_name"] == "Statistics"
    assert len(data["questions"]) > 0
    # Confirm correct answers are omitted from public session
    assert "correct_answer" not in data["questions"][0]


def test_practice_submission_and_scoring_evaluation():
    """6 & 7 & 8. Test practice submission, score calculation, percentage math, and detailed explanations."""
    user_id = "eval_user_01"

    # 1. Generate session
    gen_res = client.post("/api/v1/practice/generate", json={
        "user_id": user_id,
        "task_id": "task_prob_01",
        "skill_name": "Probability",
        "difficulty": "beginner",
    })
    session = gen_res.json()
    practice_id = session["practice_id"]
    q1_id = session["questions"][0]["question_id"]

    # 2. Submit correct answer for q1
    submit_payload = {
        "user_id": user_id,
        "answers": [
            {"question_id": q1_id, "learner_answer": "1/2"}
        ]
    }
    sub_res = client.post(f"/api/v1/practice/{practice_id}/submit", json=submit_payload)
    assert sub_res.status_code == 200
    result = sub_res.json()

    assert result["user_id"] == user_id
    assert result["practice_id"] == practice_id
    assert result["score"] >= 1
    assert result["percentage"] > 0.0
    assert len(result["question_results"]) == len(session["questions"])
    assert result["question_results"][0]["explanation"] != ""


def test_practice_history_endpoint():
    """9 & 10. Test GET /api/v1/practice/history endpoint."""
    user_id = "history_user_01"

    # Generate & submit practice
    gen_res = client.post("/api/v1/practice/generate", json={
        "user_id": user_id,
        "task_id": "task_ml_01",
        "skill_name": "Machine Learning",
    })
    practice_id = gen_res.json()["practice_id"]
    client.post(f"/api/v1/practice/{practice_id}/submit", json={
        "user_id": user_id,
        "answers": []
    })

    # Retrieve history
    hist_res = client.get(f"/api/v1/practice/history?user_id={user_id}")
    assert hist_res.status_code == 200
    history = hist_res.json()
    assert len(history) >= 1
    assert history[0]["user_id"] == user_id
    assert history[0]["skill_name"] == "Machine Learning"


def test_mongodb_failure_returns_503_for_resources_and_practice():
    """11. Test that DB offline state returns HTTP 503 Service Unavailable."""
    db_manager.db = None
    db_manager.client = None

    res_rec = client.post("/api/v1/resources/recommend", json={"task_id": "t1", "skill_name": "Python"})
    assert res_rec.status_code == 503

    res_prac = client.post("/api/v1/practice/generate", json={"user_id": "u1", "task_id": "t1", "skill_name": "Python"})
    assert res_prac.status_code == 503

    res_hist = client.get("/api/v1/practice/history?user_id=u1")
    assert res_hist.status_code == 503
