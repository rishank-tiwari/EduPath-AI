"""
Automated unit & integration tests verifying:
1. 10-question General Practice sessions vs 5-question Module Practice sessions.
2. Persistence of Module Completion status in MongoDB LearningPlan.
3. Prevention of duplicate practice session generation for completed modules.
4. Compatibility with Progress update and Adaptation pipeline.
"""

import asyncio
import mongomock
import pytest
from fastapi.testclient import TestClient
from app.core.database import db_manager
from app.main import app
from app.api.routes.practice import PracticeGenerateRequest
from app.services.practice_service import PracticeService
from app.services.learning_plan_service import learning_plan_service

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


# --- REQUIREMENT 1: 10-QUESTION GENERAL PRACTICE ---

def test_general_practice_generates_exactly_10_questions():
    """Verify general practice mode generates exactly 10 questions."""
    practice_service = PracticeService()
    session = practice_service.generate_practice(
        user_id="test_user_gen",
        task_id="task_gen_10",
        skill_name="Statistics",
        difficulty="beginner",
        practice_mode="general"
    )
    assert session.practice_mode == "general"
    assert len(session.questions) == 10


def test_general_practice_questions_match_requested_skill_relevance():
    """Verify ALL 10 questions generated for Machine Learning match Machine Learning topic strictly."""
    practice_service = PracticeService()
    session = practice_service.generate_practice(
        user_id="test_user_relevance",
        task_id="task_ml_10",
        skill_name="Machine Learning",
        difficulty="beginner",
        practice_mode="general"
    )
    assert session.practice_mode == "general"
    assert len(session.questions) == 10
    
    # Verify every question has skill_name and topic metadata attached
    for q in session.questions:
        assert q.skill_name == "Machine Learning"
        assert q.topic is not None
        # Verify no question prompt contains unrelated skills (like statistics or probability or sql)
        q_text = q.question.lower()
        assert "probability of rolling" not in q_text
        assert "measure of central tendency" not in q_text
        assert "sql join" not in q_text


def test_general_practice_submission_handles_10_answers():
    """Verify submitting 10 answers for general practice evaluates correctly."""
    user_id = "test_user_gen_sub"
    gen_res = client.post("/api/v1/practice/generate", json={
        "user_id": user_id,
        "task_id": "task_gen_10",
        "skill_name": "Statistics",
        "difficulty": "beginner",
        "practice_mode": "general"
    })
    assert gen_res.status_code == 200
    data = gen_res.json()
    assert data["practice_mode"] == "general"
    assert len(data["questions"]) == 10

    # Submit 10 answers
    answers = [{"question_id": q["question_id"], "learner_answer": "Mean"} for q in data["questions"]]
    sub_res = client.post(f"/api/v1/practice/{data['practice_id']}/submit", json={
        "user_id": user_id,
        "answers": answers
    })
    assert sub_res.status_code == 200
    res_data = sub_res.json()
    assert res_data["total_questions"] == 10
    assert 0 <= res_data["score"] <= 10


# --- REQUIREMENT 2: 5-QUESTION MODULE PRACTICE ---

def test_module_practice_generates_exactly_5_questions():
    """Verify module practice mode generates exactly 5 questions."""
    practice_service = PracticeService()
    session = practice_service.generate_practice(
        user_id="test_user_mod",
        task_id="task_mod_01",
        skill_name="Probability",
        difficulty="beginner",
        practice_mode="module",
        module_id="mod_w1_prob"
    )
    assert session.practice_mode == "module"
    assert session.module_id == "mod_w1_prob"
    assert len(session.questions) == 5


# --- REQUIREMENT 3: MODULE COMPLETION & REPEATED QUESTION PREVENTION ---

def test_module_completion_persistence_and_repeated_question_prevention():
    """
    Verify complete flow:
    1. Generate module plan.
    2. Start 5-question module practice.
    3. Submit answers.
    4. Module status becomes 'completed' in MongoDB LearningPlan.
    5. Attempting to generate practice for same completed module raises 409 Conflict.
    """
    user_id = "test_module_complete_user"

    # 1. Setup profile, gap analysis, and learning plan
    client.post("/api/v1/profile", json={
        "user_id": user_id,
        "target_role": "AI/ML Engineer",
        "career_goal": "Master deep learning",
        "technical_skills": [{"name": "Python", "proficiency": "Intermediate"}]
    })
    client.post(f"/api/v1/skill-gaps/analyze?user_id={user_id}")
    plan_res = client.post(f"/api/v1/plans/generate?user_id={user_id}")
    assert plan_res.status_code == 200
    plan = plan_res.json()
    first_mod = plan["modules"][0]
    mod_id = first_mod["module_id"]
    task_id = first_mod["tasks"][0]["task_id"]
    skill_name = first_mod["skill_name"]

    # 2. Generate 5-question module practice session
    gen_res = client.post("/api/v1/practice/generate", json={
        "user_id": user_id,
        "task_id": task_id,
        "module_id": mod_id,
        "skill_name": skill_name,
        "difficulty": "beginner",
        "practice_mode": "module"
    })
    assert gen_res.status_code == 200
    session_data = gen_res.json()
    assert len(session_data["questions"]) == 5

    # 3. Submit practice answers
    answers = [{"question_id": q["question_id"], "learner_answer": "Sample Answer"} for q in session_data["questions"]]
    sub_res = client.post(f"/api/v1/practice/{session_data['practice_id']}/submit", json={
        "user_id": user_id,
        "answers": answers
    })
    assert sub_res.status_code == 200

    # 4. Verify module status updated to 'completed' in MongoDB LearningPlan
    latest_plan = learning_plan_service.get_plan(user_id)
    target_mod = next(m for m in latest_plan.modules if m.module_id == mod_id)
    assert target_mod.status == "completed"
    assert target_mod.completion_status == "completed"
    assert target_mod.completed_at is not None
    assert target_mod.latest_score is not None

    # 5. Attempting to generate another practice for same completed module fails with 409 Conflict
    dup_gen = client.post("/api/v1/practice/generate", json={
        "user_id": user_id,
        "task_id": task_id,
        "module_id": mod_id,
        "skill_name": skill_name,
        "difficulty": "beginner",
        "practice_mode": "module"
    })
    assert dup_gen.status_code == 409
    assert "already completed" in dup_gen.json()["detail"].lower()


# --- ADAPTIVE PIPELINE INTEGRATION TEST ---

def test_low_score_module_practice_triggers_adaptation():
    """Verify low score on module practice still integrates with progress and adaptation pipeline."""
    user_id = "test_adaptive_module_user"

    client.post("/api/v1/profile", json={
        "user_id": user_id,
        "target_role": "AI/ML Engineer",
        "career_goal": "Master deep learning",
        "technical_skills": [{"name": "Python", "proficiency": "Intermediate"}]
    })
    client.post(f"/api/v1/skill-gaps/analyze?user_id={user_id}")
    client.post(f"/api/v1/plans/generate?user_id={user_id}")

    # Generate & submit low-score practice
    gen_res = client.post("/api/v1/practice/generate", json={
        "user_id": user_id,
        "task_id": "task_stat_01",
        "module_id": "mod_w1_stats",
        "skill_name": "Statistics",
        "difficulty": "beginner",
        "practice_mode": "module"
    })
    session_data = gen_res.json()
    answers = [{"question_id": q["question_id"], "learner_answer": "Wrong Answer"} for q in session_data["questions"]]
    client.post(f"/api/v1/practice/{session_data['practice_id']}/submit", json={
        "user_id": user_id,
        "answers": answers
    })

    # Trigger adaptation
    adapt_res = client.post("/api/v1/adaptation/analyze", json={
        "user_id": user_id,
        "skill_name": "Statistics",
        "topic": "Probability Basics"
    })
    assert adapt_res.status_code == 200
    adapt_data = adapt_res.json()
    assert adapt_data["action"] in ("review", "add_practice")
    assert adapt_data["new_plan_version"] >= 2


def test_view_result_fetches_stored_result_by_id():
    """Verify GET /api/v1/practice/results/{identifier} retrieves stored practice result by practice_id or result_id."""
    user_id = "test_view_result_user"

    client.post("/api/v1/profile", json={
        "user_id": user_id,
        "target_role": "Data Scientist",
        "career_goal": "Learn ML",
        "technical_skills": [{"name": "Python", "proficiency": "Intermediate"}]
    })
    client.post(f"/api/v1/skill-gaps/analyze?user_id={user_id}")
    plan_res = client.post(f"/api/v1/plans/generate?user_id={user_id}")
    first_mod = plan_res.json()["modules"][0]

    gen_res = client.post("/api/v1/practice/generate", json={
        "user_id": user_id,
        "task_id": first_mod["tasks"][0]["task_id"],
        "module_id": first_mod["module_id"],
        "skill_name": first_mod["skill_name"],
        "difficulty": "beginner",
        "practice_mode": "module"
    })
    session_data = gen_res.json()
    practice_id = session_data["practice_id"]

    sub_res = client.post(f"/api/v1/practice/{practice_id}/submit", json={
        "user_id": user_id,
        "answers": [{"question_id": q["question_id"], "learner_answer": "Sample"} for q in session_data["questions"]]
    })
    assert sub_res.status_code == 200
    stored_result_id = sub_res.json()["result_id"]

    # Retrieve by practice_id
    res_by_prac = client.get(f"/api/v1/practice/results/{practice_id}")
    assert res_by_prac.status_code == 200
    assert res_by_prac.json()["practice_id"] == practice_id
    assert res_by_prac.json()["result_id"] == stored_result_id

    # Retrieve by result_id
    res_by_res = client.get(f"/api/v1/practice/results/{stored_result_id}")
    assert res_by_res.status_code == 200
    assert res_by_res.json()["result_id"] == stored_result_id


def test_invalid_result_id_returns_404():
    """Verify requesting a non-existent result ID returns 404 Not Found."""
    res = client.get("/api/v1/practice/results/non_existent_id_99999")
    assert res.status_code == 404
    assert "not found" in res.json()["detail"].lower()
