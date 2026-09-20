# Practice Agent Documentation (Task 1.4)

## Purpose
The **Practice Agent** (`ACT` phase) synthesizes contextual practice activities (`mcq`, `short_answer`), evaluates learner answer submissions deterministically, computes scores and percentages, and provides clear explanations.

It answers:
> *"How can the learner test what they just learned, and how well did they perform?"*

---

## Inputs & Outputs

### Practice Generation Inputs
- `user_id`: Learner identifier.
- `task_id`: Associated learning task ID.
- `skill_name`: Target skill name (e.g., `"Statistics"`, `"Probability"`, `"Machine Learning"`).
- `difficulty`: Target difficulty level.

### Practice Generation Outputs
A public `PracticeSession` object containing:
- `practice_id`: Unique session ID.
- `questions`: List of `PracticeQuestionPublic` items (omitting correct answers and explanations for security).

### Submission Evaluation Inputs
- `practice_id`: Unique practice session ID.
- `user_id`: Learner identifier.
- `answers`: List of submitted `LearnerAnswerItem` items.

### Submission Evaluation Outputs
A structured `PracticeResultRecord` containing:
- `result_id`: Unique result ID.
- `score`: Number of correctly answered questions.
- `total_questions`: Total questions evaluated.
- `percentage`: Percentage score (`0.0%` to `100.0%`).
- `question_results`: Detailed list containing `correct`, `learner_answer`, `correct_answer`, and `explanation`.

---

## Storage & API Integration
- **MongoDB Collections**: `practice_sessions` and `practice_results` with index on `user_id`.
- **Endpoints**:
  - `POST /api/v1/practice/generate`: Generates new practice session.
  - `POST /api/v1/practice/{practice_id}/submit`: Evaluates answers and returns score/explanations.
  - `GET /api/v1/practice/history`: Retrieves previous practice evaluation records.
