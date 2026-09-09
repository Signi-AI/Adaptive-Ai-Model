# Database Documentation

## Engine

SQLite via SQLAlchemy 2.x. Single file, zero configuration, fully offline.

Default location (configurable in `app/config/settings.py`):

```
data/database/adaptive_learning.db
```

## Tables

### students
Primary learner identity.
- `id` (PK, UUID string)
- `name`, `grade_level`, `preferred_language`
- `created_at`, `updated_at`
- `metadata_json` (optional free-form JSON)

### topics
Curriculum nodes.
- `id` (PK)
- `subject`, `name`, `description`, `order_index`
- `prerequisite_ids` (comma-separated list of topic IDs – simple DAG)
- Indexed on `subject`

### lessons
Instructional content belonging to a topic.
- FK → `topics.id`
- `title`, `content`, `difficulty`, `order_index`, `estimated_minutes`

### questions
Assessment items.
- FK → `topics.id`, optional FK → `lessons.id`
- `stem`, `options_json`, `correct_answer`, `explanation`
- `difficulty` (easy/medium/hard), `tags`
- Indexed on `topic_id`, `difficulty`

### mastery
Hot table – one row per (student, topic).
- Unique constraint on `(student_id, topic_id)`
- `score` (0.0–100.0), `attempts`, `correct_count`
- `last_attempt_at`, `updated_at`
- Indexed on both foreign keys

### answer_attempts
Atomic event log that drives all adaptation.
- FKs → students, questions, topics
- `given_answer`, `result`, `difficulty`, `time_spent_seconds`
- Indexed on student, topic, question, created_at

### mistakes
Aggregated mistake statistics.
- Unique on `(student_id, topic_id, concept_tag)`
- `total_mistakes`, `consecutive_mistakes`, `is_improving`
- Updated by MistakeAnalyzer after every attempt

### spaced_repetition
Optional schedule (only written when feature flag is on).
- Unique on `(student_id, question_id)`
- `ease_factor`, `interval_days`, `next_review_at`, `repetitions`
- Indexed on `next_review_at`

## Relationships

```
Student 1──* Mastery *──1 Topic
Student 1──* AnswerAttempt *──1 Question *──1 Topic
Topic 1──* Lesson
Topic 1──* Question
```

## Design decisions

- Prerequisite edges stored as a simple comma-separated string for the MVP.
  A future normalised junction table can be introduced without changing the domain model.
- Mastery is denormalised (one row per pair) for fast reads by the adaptive engine.
- No soft-delete; historical attempts are immutable.
