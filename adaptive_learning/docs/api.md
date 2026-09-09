# Service / API Documentation

All client-facing operations go through `AdaptiveLearningService`.

```python
from app.database.session import get_session
from app.services import AdaptiveLearningService

session = get_session()
service = AdaptiveLearningService(session)
```

## Student management

| Method | Description |
|--------|-------------|
| `create_student(name, grade_level=None, preferred_language="en")` | Create profile, return `Student` |
| `get_student(student_id)` | Load profile or `None` |
| `update_student(student)` | Persist profile changes |

## Progress & mastery

| Method | Description |
|--------|-------------|
| `get_student_progress(student_id)` | List of `Mastery` for all topics |
| `get_mastery(student_id, topic_id)` | Single `Mastery` or `None` |

## Core adaptive interaction

| Method | Description |
|--------|-------------|
| `submit_answer(student_id, question_id, given_answer, time_spent_seconds=None)` | Full cycle: validate → record → update mastery → analyse mistakes → feedback. Returns dict with result, feedback, mastery. |
| `get_next_question(student_id, topic_id=None)` | Adaptive question selection. If `topic_id` omitted, uses top recommendation. |
| `get_recommended_topic(student_id)` | Single highest-priority `Recommendation` |
| `get_recommendations(student_id, max_items=3)` | Ordered list of `Recommendation` |
| `diagnose_student(student_id)` | `DiagnosisReport` with weak topics + summary |
| `get_learning_path(student_id, max_length=8)` | Ordered `LearningPath` respecting prerequisites |

## Content helpers

| Method | Description |
|--------|-------------|
| `list_topics(subject=None)` | All topics or filtered by subject |
| `get_topic(topic_id)` | Single topic |
| `list_lessons(topic_id)` | Lessons ordered by `order_index` |
| `get_question(question_id)` | Single question |

## Return shapes (submit_answer)

```python
{
  "attempt_id": "...",
  "result": "correct" | "incorrect",
  "feedback": {
    "is_correct": bool,
    "message": str,
    "explanation": str,
    "concept_to_review": str | None,
    "mastery_after": float | None
  },
  "mastery": {
    "topic_id": str,
    "score": float,
    "attempts": int,
    "correct_count": int
  }
}
```

## Error handling

- Missing student / question → `ValueError` with a clear message.
- Database errors are not leaked to callers; the service layer catches and re-raises domain-level exceptions where appropriate.
- AI enrichment failures are swallowed; core feedback always succeeds.
