# TOALM V2 Local Integration Runbook

The frontend communicates only with FastAPI. FastAPI owns authentication,
authorization, session ownership, attempts, mastery, adaptive decisions and
recommendations. It calls the Artificial Teacher model process over loopback;
the browser never sends model context or model credentials.

## Configuration

Copy `backend/.env.example` to `backend/.env`, set the PostgreSQL URL and use a
long random JWT secret. Copy the Model component's `.env.example` to
`Model/.env`. `TEACHER_MODEL_URL` must match the model server address, and the
optional model API keys must match. Copy `frontend/.env.example` to
`frontend/.env` when the backend is not on `127.0.0.1:8000`.

The model server requires Ollama and the configured Gemma artifact already
downloaded. Add textbooks and run the Model ingestion step before expecting
grounded curriculum replies. The regular learning flow does not use a remote
AI provider.

## Start locally

1. Create and activate a Python environment in `backend`, then run
   `pip install -r requirements.txt`.
2. Start PostgreSQL, then from `backend` run `alembic upgrade head`.
3. Seed the required roles and curriculum using the existing project seed
   process. For a local first run, use `python -m app.scripts.seed_starter_curriculum`
   from `backend`; it adds the class levels and starter subjects/topics required
   by the current learner UI. Each `academic_levels.code` or `academic_levels.name` must match
   the registration class (for example `FORM_2`, `Form 2`, `STD_4`, or
   `Standard 4`). Subjects, topics, and generated practice questions must
   exist before the learning screen can start a session and record progress.
4. In a separate terminal, activate `Model/.venv`, ensure Ollama is running,
   and run `uvicorn artificial_teacher.server:app --host 127.0.0.1 --port 8100`.
   Check `http://127.0.0.1:8100/health`; it must report `status: ok`.
5. From `backend`, run `uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`.
6. From `frontend`, run `npm install` once and then `npm run dev`.

## Frontend API contract

- `POST /auth/register` creates a student account; `POST /auth/login` accepts
  form fields `username` and `password` and returns access and refresh tokens.
- `GET /students/me` reads the signed-in student's database profile. Every
  protected request verifies both the JWT and its live, non-revoked database
  session before it is served.
- `GET /students/me/curriculum` resolves subjects from the class saved at
  registration. The browser must use this endpoint rather than allowing the
  learner to pick an education level. `GET /topics/subject/{subject_id}` loads
  the topics for one of those subjects.
- `POST /learning/sessions` starts an owned learning session.
- `POST /learning/session/message` accepts only `session_id` and `message`.
  FastAPI builds the curriculum, history, mastery and adaptive context before
  requesting `POST /v1/teach` from the local model server.
- `POST /learning/attempts` evaluates an existing backend-generated question,
  persists the attempt, then updates mastery, adaptive decision and
  recommendations in one transaction. A retry uses the same
  `client_submission_id`.
- `GET /learning/sessions/{session_id}/question` returns an existing generated
  practice prompt for that session's topic without exposing the verified answer.
- `GET /progress?academic_level_id=...` and `GET /recommendations` show
  persisted learning state. The frontend gets the curriculum level ID from
  `/students/me/curriculum`, so progress is scoped to the registered class.
- `PATCH /students/me` accepts a display name and class level. Existing profile
  controls can use it when a learner changes their education level; subsequent
  curriculum and progress requests resolve the new class automatically.

Expected model failures are returned safely: unavailable/busy model `503`,
slow model `504`, malformed model output `502`, and expired API credentials
trigger a frontend refresh attempt followed by a sign-in prompt if it fails.

## Database migration added by this integration

`c2f9a6e5b4d1_link_chat_messages_to_learning_sessions` scopes chat history to
the learning session and adds idempotency support for answer submissions. Run
the migration before deploying the new frontend.
