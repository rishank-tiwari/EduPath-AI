from app.main import app
from fastapi.testclient import TestClient

with TestClient(app) as client:
    userId = 'demo_user_1'
    print("=== STARTING PRACTICE -> PROGRESS -> ADAPTATION FLOW TEST ===")

    # 1. Generate Practice
    gen_res = client.post('/api/v1/practice/generate', json={
        'user_id': userId,
        'task_id': 'task_stats_1',
        'skill_name': 'Statistics',
        'difficulty': 'beginner'
    })
    print('1. Generate Practice Status:', gen_res.status_code)
    practice_data = gen_res.json()
    practice_id = practice_data.get('practice_id')
    questions = practice_data.get('questions', [])
    print(f'   Practice ID: {practice_id}, Questions count: {len(questions)}')

    # 2. Submit deliberately low score (0/2)
    answers_list = []
    for q in questions:
        q_id = q['question_id']
        correct = q.get('correct_answer', '')
        options = q.get('options', [])
        wrong = [opt for opt in options if opt != correct]
        answers_list.append({
            'question_id': q_id,
            'learner_answer': wrong[0] if wrong else 'Wrong Answer Choice'
        })

    sub_res = client.post(f'/api/v1/practice/{practice_id}/submit', json={
        'user_id': userId,
        'answers': answers_list
    })
    print('2. Submit Practice Status:', sub_res.status_code)
    result = sub_res.json()
    print(f"   Score: {result.get('score')}/{result.get('total_questions')} ({result.get('percentage')}%)")

    # 3. Check Progress
    prog_res = client.get(f'/api/v1/progress?user_id={userId}')
    print('3. Get Progress Status:', prog_res.status_code)
    print(f"   Progress data: {prog_res.json()}")

    # 4. Trigger Adaptation
    adapt_res = client.post('/api/v1/adaptation/analyze', json={
        'user_id': userId,
        'skill_name': 'Statistics'
    })
    print('4. Trigger Adaptation Status:', adapt_res.status_code)
    print(f"   Adaptation Decision: {adapt_res.json()}")

    # 5. Check Plan Update
    plan_res = client.get(f'/api/v1/plans?user_id={userId}')
    print('5. Get Plan Status:', plan_res.status_code)
    plan = plan_res.json()
    print(f"   Plan Version: v{plan.get('version')}")
    print(f"   New First Task: {plan['modules'][0]['tasks'][0]['title']}")
    print("=== END FLOW TEST ===")
