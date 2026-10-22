# INFERENCE.md — how the backend calls the Artificial Teacher model

## Start
From the `model` folder, venv active:
`uvicorn artificial_teacher.server:app --host 127.0.0.1 --port 8100`   (ONE worker)

Requires Ollama running with the model from `.env` pulled (default `gemma3:4b`). Fully offline after setup.

## Endpoints
| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | `status` is `ok` or `degraded`, plus `model`, `ollama_reachable`, `model_installed`, `chunks_loaded` |
| POST | `/v1/teach` | One teaching reply |

If `MODEL_API_KEY` is set in `model/.env`, `/v1/teach` requires the header `X-Model-Key: <same value>`.

## Request (`POST /v1/teach`)
```json
{
  "subject": "Mathematics",
  "topic": "Linear Equations",
  "student": {
    "display_name": "Asha",
    "class_level": "Form 2",
    "mastery": 0.42,
    "mastery_label": null,
    "strengths": ["basic addition"],
    "weaknesses": ["equation manipulation"],
    "recent_performance": "poor",
    "recommended_action": "REVISE"
  },
  "message": "I don't understand this.",
  "history": [{"role": "teacher", "content": "..."}, {"role": "student", "content": "..."}],
  "assessment": null,
  "teaching_language": null
}
```
- `subject`, `topic`, `student.class_level` must match the names used in `data/manifest.json` (case and extra spaces are ignored).
- `recent_performance`: `unknown | poor | developing | good | excellent`. `mastery`: 0 to 1 or null.
- `recommended_action`: `INTRODUCE, REVISE (alias REVIEW), REMEDIATE, PRACTICE, CONTINUE, ADVANCE (alias PROGRESS)`. Unknown values do not crash; the response carries a warning.
- `history`: only the last 8 turns are used. `message` may be empty only when `assessment` is given.
- `assessment` (backend-verified, the model never re-judges it):
```json
{"question": "Solve 2x + 4 = 10", "student_answer": "x = 2.5", "is_correct": false,
 "verified_answer": "x = 3", "verified_solution_steps": ["2x = 6", "x = 3"], "reveal_answer": false}
```
- `teaching_language`: `en`, `sw`, or null for the default (Std = sw, Form = en, subject Kiswahili = sw, English = en).
- Never send student ids, emails, or other personal data. The model does not need them.

## Response (200)
```json
{
  "response": "Let's go step by step. ...",
  "teaching_mode": "REVISE",
  "language": "en",
  "grounded": true,
  "sources": [{"chunk_id": "d21dd767c56f", "source": "Test Mathematics Form 2", "topic": "Linear Equations",
               "page_start": 1, "page_end": 2, "scope": "topic"}],
  "model": "gemma3:4b",
  "latency_ms": 5400,
  "warnings": []
}
```
`warnings` can contain `no_curriculum_excerpts`, `unknown_recommended_action:<value>`, `possible_answer_leak`. Log them.
The response never contains mastery, score, correctness, student id, or recommendation id. Those stay in the backend.

## Errors (JSON body `{"detail": "..."}`)
| Status | Meaning | What the backend should do |
|---|---|---|
| 401 | Missing/wrong `X-Model-Key` | Fix configuration |
| 422 | Bad request (missing field, mastery outside 0-1, empty message) | Fix the request |
| 502 | Model returned an error or an empty reply | Retry once, then show a friendly message |
| 503 | Model busy (header `Retry-After: 10`) or Ollama/model not available | Ask the student to wait and retry |
| 504 | Model took longer than `TEACHER_TIMEOUT_SECONDS` | Retry or show a friendly message |

## Backend client example
```python
import httpx

MODEL_URL = "http://127.0.0.1:8100"
MODEL_KEY = ""   # same as MODEL_API_KEY in model/.env, empty if unused
_http = httpx.Client(trust_env=False, timeout=200)   # must exceed TEACHER_QUEUE_TIMEOUT + TEACHER_TIMEOUT

def ask_teacher(payload: dict) -> dict:
    headers = {"X-Model-Key": MODEL_KEY} if MODEL_KEY else {}
    r = _http.post(f"{MODEL_URL}/v1/teach", json=payload, headers=headers)
    if r.status_code in (502, 503, 504):
        raise RuntimeError(r.json().get("detail", "Teacher unavailable"))
    r.raise_for_status()
    return r.json()
```
Build `payload` on the server from the database (student, progress, last assessment). Never accept `student`,
`assessment` or `recommended_action` from the browser.

## What stays in the backend, what lives here
- Backend: students, authentication, subjects/topics, attempts, mastery, recommendations, question generation and
  answer verification, building the request above, storing results.
- Model folder: the textbooks, retrieval, the prompt, the Gemma call, the teaching reply.
So the backend no longer needs its own `data/content`, `retrieval_service.py`, `prompt_builder.py` or
`ingest_content.py`. It keeps only a thin HTTP client and the code that builds the request from the database.

## Performance and capacity
`TEACHER_MAX_CONCURRENT` (default 2) is how many requests are sent to the model at once; the rest wait up to
`TEACHER_QUEUE_TIMEOUT_SECONDS`, then get 503. One model on one machine serves students one after another, so
measure latency on the real hardware with the real number of students before promising anything.
