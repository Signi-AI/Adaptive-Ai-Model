"""HTTP contract tests for the standalone model server. The model is faked; no Ollama needed."""
import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from artificial_teacher.gemma_client import (  # noqa: E402
    ModelBusyError, ModelResponseError, ModelTimeoutError, ModelUnavailableError,
)
from artificial_teacher.retrieval_service import RetrievalService  # noqa: E402
from artificial_teacher.server import create_app  # noqa: E402
from artificial_teacher.service import ArtificialTeacherService  # noqa: E402
from artificial_teacher.settings import MODEL_ROOT, load_env, resolve_path  # noqa: E402

PAYLOAD = {
    "subject": "Mathematics",
    "topic": "Linear Equations",
    "student": {"display_name": "Asha", "class_level": "Form 2", "mastery": 0.42,
                "strengths": ["basic addition"], "weaknesses": ["equation manipulation"],
                "recent_performance": "poor", "recommended_action": "REVISE"},
    "message": "I don't understand this.",
}


class FakeClient:
    model = "fake-gemma"

    def __init__(self, reply="Let's go step by step. What is 2x + 4 = 10 asking us to find?", error=None):
        self.reply, self.error = reply, error

    def health(self):
        return {"reachable": True, "model_installed": True, "installed_models": ["fake-gemma"], "detail": "ok"}

    def chat(self, messages, **_):
        if self.error:
            raise self.error
        return self.reply


@pytest.fixture()
def chunks_file(tmp_path):
    p = tmp_path / "chunks.jsonl"
    p.write_text(json.dumps({"id": "c1", "text": "A linear equation has one unknown.", "subject": "Mathematics",
                             "class_level": "Form 2", "topic": "Linear Equations", "language": "en",
                             "source": "Test Book", "page_start": 4, "page_end": 4}) + "\n", encoding="utf-8")
    return p


def _make_client(chunks_file, **kw):
    """Build a TestClient as a context manager so the lifespan fires (Starlette >= 1.0)."""
    svc = ArtificialTeacherService(FakeClient(**kw), RetrievalService(chunks_file))
    return TestClient(create_app(svc))


def test_health(chunks_file):
    with _make_client(chunks_file) as c:
        body = c.get("/health").json()
    assert body == {"status": "ok", "model": "fake-gemma", "ollama_reachable": True,
                    "model_installed": True, "chunks_loaded": 1}


def test_teach_returns_contract(chunks_file):
    with _make_client(chunks_file) as c:
        r = c.post("/v1/teach", json=PAYLOAD)
    assert r.status_code == 200
    body = r.json()
    assert set(body) == {"response", "teaching_mode", "language", "grounded", "sources", "model", "latency_ms", "warnings"}
    assert body["teaching_mode"] == "REVISE" and body["language"] == "en" and body["grounded"] is True
    assert body["sources"][0]["source"] == "Test Book"
    for forbidden in ("mastery", "score", "student_id", "recommendation_id", "is_correct"):
        assert forbidden not in body


@pytest.mark.parametrize("error,status", [
    (ModelBusyError("busy"), 503), (ModelUnavailableError("down"), 503),
    (ModelTimeoutError("slow"), 504), (ModelResponseError("bad"), 502),
])
def test_model_errors_map_to_http_status(chunks_file, error, status):
    with _make_client(chunks_file, error=error) as c:
        r = c.post("/v1/teach", json=PAYLOAD)
    assert r.status_code == status and r.json()["detail"]
    if isinstance(error, ModelBusyError):
        assert r.headers["retry-after"] == "10"


def test_validation_errors(chunks_file):
    with _make_client(chunks_file) as c:
        assert c.post("/v1/teach", json={**PAYLOAD, "message": "  "}).status_code == 422       # empty message
        assert c.post("/v1/teach", json={"subject": "Mathematics"}).status_code == 422           # missing fields
        bad = {**PAYLOAD, "student": {**PAYLOAD["student"], "mastery": 1.5}}
        assert c.post("/v1/teach", json=bad).status_code == 422                                  # mastery out of range


def test_api_key_enforced_only_when_configured(chunks_file, monkeypatch):
    with _make_client(chunks_file) as c:
        monkeypatch.delenv("MODEL_API_KEY", raising=False)
        assert c.post("/v1/teach", json=PAYLOAD).status_code == 200
        monkeypatch.setenv("MODEL_API_KEY", "s3cret")
        assert c.post("/v1/teach", json=PAYLOAD).status_code == 401
        assert c.post("/v1/teach", json=PAYLOAD, headers={"X-Model-Key": "wrong"}).status_code == 401
        assert c.post("/v1/teach", json=PAYLOAD, headers={"X-Model-Key": "s3cret"}).status_code == 200


def test_resolve_path_is_relative_to_model_folder_not_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert resolve_path("data/raw") == MODEL_ROOT / "data/raw"
    assert resolve_path(str(tmp_path)) == tmp_path


def test_load_env_parses_file_and_real_env_wins(tmp_path, monkeypatch):
    f = tmp_path / ".env"
    f.write_text('\ufeff# comment\nTEACHER_MODEL="gemma3:1b"\nTEACHER_NUM_CTX=2048\nBROKEN LINE\n', encoding="utf-8")
    monkeypatch.delenv("TEACHER_MODEL", raising=False)
    monkeypatch.setenv("TEACHER_NUM_CTX", "9999")
    load_env(f)
    import os
    assert os.environ["TEACHER_MODEL"] == "gemma3:1b"      # BOM + quotes handled
    assert os.environ["TEACHER_NUM_CTX"] == "9999"          # already-set variable not overridden
    monkeypatch.delenv("TEACHER_MODEL", raising=False)
