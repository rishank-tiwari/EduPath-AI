# Progress Agent Documentation (Task 1.5)

## Purpose
The **Progress Agent** (`MEASURE` phase) analyzes historical practice result records, tracks learner skill trajectory, calculates performance status, evaluates chronological trends, and detects weak topics.

It answers:
> *"How is this learner performing across skills and topics?"*

---

## Inputs & Outputs

### Inputs
- `user_id`: Learner identifier.
- `skill_name`: Target skill name.
- `topic`: Learning topic name.
- `practice_results`: Chronological list of stored practice evaluation records.

### Outputs
A structured `ProgressSummary` model containing:
- `progress_id`: Unique progress summary ID.
- `total_attempts`: Count of completed practice sessions.
- `total_questions` & `correct_answers`: Aggregated question metrics.
- `average_score`: Mean percentage score across attempts.
- `latest_score`: Most recent practice score.
- `performance_status`: Categorized performance level (`strong`, `on_track`, `needs_review`, `struggling`).
- `trend`: Directional trajectory (`improving`, `stable`, `declining`, `insufficient_data`).

---

## Performance Thresholds & Trend Rules

### Configurable Performance Status Thresholds
- $\ge 90.0\% \rightarrow$ **`strong`**
- $70.0\% - 89.9\% \rightarrow$ **`on_track`**
- $50.0\% - 69.9\% \rightarrow$ **`needs_review`**
- $< 50.0\% \rightarrow$ **`struggling`**

### Trend Analysis Rules
- $< 2$ attempts $\rightarrow$ **`insufficient_data`**
- Latest score $>$ Previous score by $> +5.0\% \rightarrow$ **`improving`**
- Latest score $<$ Previous score by $> -5.0\% \rightarrow$ **`declining`**
- Score change within $[-5.0\%, +5.0\%] \rightarrow$ **`stable`**

---

## Storage & API Integration
- **MongoDB Collections**: `progress` (for summaries) and `progress_events` (for event logs) with indexes on `user_id`, `skill_name`, and `topic`.
- **Endpoints**:
  - `POST /api/v1/progress/record`: Records a progress event.
  - `GET /api/v1/progress`: Returns progress summaries for a learner.
  - `GET /api/v1/progress/skills`: Returns progress grouped by skill.
  - `GET /api/v1/progress/history`: Retrieves event logs history.
