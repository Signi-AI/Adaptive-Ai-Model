# Offline Adaptive Learning Model

Production-quality **offline-first** adaptive learning engine for students.
The system adapts content difficulty, learning path, recommendations and
feedback based on each student’s mastery (0–100 %) — completely without
internet.

This repository contains the **intelligence / model layer**, not a full UI.
Any future mobile app, web app, PWA or local school server can consume the
`AdaptiveLearningService` API.

## Features

- Student profiles & local progress storage (SQLite)
- Topic graph with prerequisites
- Mastery tracking (0–100 %) with transparent deterministic algorithm
- Adaptive difficulty (Easy / Medium / Hard)
- Knowledge diagnosis & mistake analysis
- Personalised recommendations & learning paths
- Instant educational feedback
- Optional spaced-repetition interface (disabled by default)
- Optional AI/LLM provider interface (works without any model)
- Fully offline, no cloud dependency

## Architecture (summary)

```
Client (CLI / Mobile / Web / School Server)
        ↓
AdaptiveLearningService   ← public API
        ↓
Adaptive Engine  +  Content Engine  +  Feedback Engine
        ↓
Domain models
        ↓
Repositories (interfaces)
        ↓
SQLite (SQLAlchemy)
```

Optional AI layer plugs into Feedback only and is never required.

See `docs/` for full architecture, database schema and algorithm details.

## Quick start

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialise database + sample Mathematics content
python scripts/init_db.py --drop

# 4. Run the demo CLI journey
python main.py

# 5. Run tests
pytest tests/ -v
```

## Project layout

```
adaptive_learning/
├── app/
│   ├── domain/           # Pure educational entities
│   ├── database/         # SQLAlchemy models & session
│   ├── repositories/     # Persistence contracts + SQLite impl
│   ├── adaptive_engine/  # Mastery, difficulty, diagnosis, …
│   ├── content_engine/   # Lessons, questions, answer validation
│   ├── feedback/         # Instant feedback
│   ├── ai/               # Optional AIProvider
│   ├── services/         # AdaptiveLearningService façade
│   └── config/
├── data/
│   ├── database/         # SQLite file (created at runtime)
│   └── content/          # Seed JSON (Mathematics)
├── tests/
├── scripts/
├── docs/
├── main.py
└── requirements.txt
```

## Public service API (main methods)

```python
service = AdaptiveLearningService(session)

service.create_student(name, grade_level=None)
service.get_student(student_id)
service.get_student_progress(student_id)

service.submit_answer(student_id, question_id, given_answer)
service.get_next_question(student_id, topic_id=None)
service.get_recommended_topic(student_id)
service.get_recommendations(student_id)
service.diagnose_student(student_id)
service.get_learning_path(student_id)

service.list_topics(subject=None)
service.list_lessons(topic_id)
```

## Adaptive algorithms (brief)

**Mastery** – after every answer:
- Correct → gain proportional to difficulty, with diminishing returns at high mastery
- Incorrect → loss, increased by consecutive mistakes
- Always clamped to [0, 100]

**Difficulty** – base level from mastery bands, then adjusted by recent performance streak.

**Diagnosis** – ranks topics by low mastery + consecutive mistakes.

**Learning path** – topological order of topics still below goal, prioritising weak topics while respecting prerequisites.

## Offline guarantees

- No external API calls
- No cloud database
- No mandatory authentication server
- No required LLM
- All student data and content live on the device

## Extending

- Add another subject: drop a new JSON seed under `data/content/` and load it.
- Enable AI: implement `AIProvider` and pass it to `AdaptiveLearningService`.
- Spaced repetition: implement the interface in `adaptive_engine` (feature flag already present).
- Sync: add an optional adapter that reads the same SQLite file when connectivity appears.

## License

MIT (or as required by your organisation).
