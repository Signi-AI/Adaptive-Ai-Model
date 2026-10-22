"""Tests for the AI layer. None of these need Ollama or internet: the model is faked."""
import json
import sys
from pathlib import Path

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from artificial_teacher.gemma_client import (  # noqa: E402
    GemmaClient,
    ModelBusyError,
    ModelResponseError,
    ModelTimeoutError,
    ModelUnavailableError,
)
from artificial_teacher.prompt_builder import build_messages, build_system_prompt, resolve_action  # noqa: E402
from artificial_teacher.retrieval_service import RetrievalService, tokenize  # noqa: E402
from artificial_teacher.student_context import (  # noqa: E402
    AssessmentResult,
    StudentContext,
    Turn,
    default_teaching_language,
    mastery_band,
)
from artificial_teacher.service import (  # noqa: E402
    ArtificialTeacherService,
    TeachingRequest,
    leaks_answer,
)


# --------------------------------------------------------------------------- fixtures
def _chunk(cid, text, subject, level, topic, p=1):
    return {"id": cid, "text": text, "subject": subject, "class_level": level, "topic": topic,
            "language": "en", "source": "Test Book", "page_start": p, "page_end": p}


@pytest.fixture()
def chunks_file(tmp_path):
    rows = [
        _chunk("m1", "A linear equation has one unknown and no powers. Solve 2x + 4 = 10 by subtracting 4.", "Mathematics", "Form 2", "Linear Equations", 10),
        _chunk("m2", "To balance an equation do the same operation on both sides of the equals sign.", "Mathematics", "Form 2", "Linear Equations", 11),
        _chunk("m3", "A fraction shows part of a whole. The numerator is on top.", "Mathematics", "Form 2", "Fractions", 20),
        _chunk("m4", "Quadratic equations have a squared unknown and two roots.", "Mathematics", "Form 4", "Quadratics", 5),
        _chunk("b1", "Photosynthesis happens in chloroplasts using sunlight.", "Biology", "Form 2", "Plants", 3),
    ]
    p = tmp_path / "chunks.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return p


class FakeClient:
    model = "fake-gemma"

    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []

    def health(self):
        return {"reachable": True, "model_installed": True, "installed_models": [self.model], "detail": "ok"}

    def chat(self, messages, **_):
        self.calls.append(messages)
        return self.replies.pop(0) if len(self.replies) > 1 else self.replies[0]


def _student(**kw):
    base = dict(display_name="Asha Mwakyusa", class_level="Form 2", mastery=0.31, recent_performance="poor",
                weaknesses=["balancing"], recommended_action="REVISE")
    base.update(kw)
    return StudentContext(**base)


# --------------------------------------------------------------------------- retrieval
def test_topic_scope_beats_other_topics_and_levels(chunks_file):
    r = RetrievalService(chunks_file)
    hits = r.retrieve(subject="Mathematics", class_level="Form 2", topic="Linear Equations",
                      query="how do I balance both sides", k=3)
    assert {h.scope for h in hits} == {"topic"}
    assert hits[0].chunk.id == "m2"
    assert all(h.chunk.class_level == "Form 2" and h.chunk.topic == "Linear Equations" for h in hits)


def test_label_matching_ignores_case_and_spacing(chunks_file):
    r = RetrievalService(chunks_file)
    hits = r.retrieve(subject="mathematics", class_level="form  2", topic="linear equations", query="equation")
    assert hits and hits[0].scope == "topic"


def test_unknown_topic_falls_back_to_subject_and_never_crosses_class(chunks_file):
    r = RetrievalService(chunks_file)
    hits = r.retrieve(subject="Mathematics", class_level="Form 2", topic="Ratios", query="numerator fraction")
    assert hits and all(h.scope == "subject" for h in hits)
    assert all(h.chunk.class_level == "Form 2" for h in hits)


def test_subject_fallback_with_no_word_match_returns_nothing(chunks_file):
    r = RetrievalService(chunks_file)
    assert r.retrieve(subject="Mathematics", class_level="Form 2", topic="Ratios", query="zzzz qqqq") == []


def test_topic_scope_with_generic_query_returns_topic_opening(chunks_file):
    r = RetrievalService(chunks_file)
    hits = r.retrieve(subject="Mathematics", class_level="Form 2", topic="Linear Equations", query="zzzz", k=2)
    assert [h.chunk.id for h in hits][0] in {"m1", "m2"}


def test_unknown_subject_and_missing_file_are_safe(chunks_file, tmp_path):
    assert RetrievalService(chunks_file).retrieve(subject="Chemistry", class_level="Form 2", topic="x", query="y") == []
    empty = RetrievalService(tmp_path / "nope.jsonl")
    assert empty.chunk_count == 0
    assert empty.retrieve(subject="Mathematics", class_level="Form 2", topic="x", query="y") == []


def test_bad_lines_are_skipped(tmp_path):
    p = tmp_path / "c.jsonl"
    p.write_text('not json\n' + json.dumps(_chunk("ok", "valid text here", "Mathematics", "Form 2", "T")) + "\n")
    assert RetrievalService(p).chunk_count == 1


def test_tokenizer_handles_kiswahili_and_digits():
    assert tokenize("Tafuta thamani ya x: 2x + 4 = 10") == ["tafuta", "thamani", "ya", "2x", "4", "10"]


# --------------------------------------------------------------------------- context / prompt
def test_mastery_band_and_override():
    assert mastery_band(None) == "unknown" and mastery_band(0.1) == "low"
    assert mastery_band(0.5) == "medium" and mastery_band(0.9) == "high"
    assert _student(mastery=0.1, mastery_label="high").band == "high"


def test_language_defaults():
    assert default_teaching_language("Form 2", "Mathematics") == "en"
    assert default_teaching_language("Std 5", "Mathematics") == "sw"
    assert default_teaching_language("Std 5", "English") == "en"
    assert default_teaching_language("Form 1", "Kiswahili") == "sw"


def test_resolve_action_aliases_and_unknown():
    assert resolve_action("review", "low") == ("REVISE", True)
    assert resolve_action("PROGRESS", "high") == ("ADVANCE", True)
    assert resolve_action("DANCE", "low") == ("CONTINUE", False)
    assert resolve_action(None, "unknown") == ("INTRODUCE", True)


def _prompt(student, **kw):
    return build_system_prompt(subject="Mathematics", topic="Linear Equations", student=student,
                               language=kw.get("language", "en"), hits=kw.get("hits", []),
                               assessment=kw.get("assessment"))


def test_weak_and_strong_get_different_instructions_and_no_mastery_number():
    weak, _, _ = _prompt(_student(mastery=0.31))
    strong, _, _ = _prompt(_student(mastery=0.92, recommended_action="ADVANCE"))
    assert weak != strong
    assert "Low understanding" in weak and "REVISE" in weak
    assert "High understanding" in strong and "challenging" in strong
    assert "0.31" not in weak and "0.92" not in strong
    assert "Asha" in weak and "Mwakyusa" not in weak  # first name only


def test_swahili_rule_and_ungrounded_notice():
    p, _, _ = _prompt(_student(), language="sw")
    assert "Kiswahili" in p and "No curriculum excerpt was found" in p


def test_assessment_block_hides_answer_unless_revealed():
    a = AssessmentResult(question="Solve 2x+4=10", student_answer="x=2.5", is_correct=False, verified_answer="x = 3")
    p, _, _ = _prompt(_student(), assessment=a)
    assert "INCORRECT" in p and "do NOT state it" in p and "REVEAL ANSWER: NO" in p
    a2 = a.model_copy(update={"reveal_answer": True})
    p2, _, _ = _prompt(_student(), assessment=a2)
    assert "REVEAL ANSWER: YES" in p2 and "do NOT state it" not in p2


def test_messages_alternate_and_end_with_user():
    hist = [Turn(role="teacher", content="Hi"), Turn(role="student", content="a"), Turn(role="student", content="b"),
            Turn(role="teacher", content="ok")]
    msgs = build_messages(system_prompt="S", history=hist, user_message="new")
    roles = [m["role"] for m in msgs]
    assert roles[0] == "system" and roles[1] == "user" and roles[-1] == "user"
    assert all(roles[i] != roles[i + 1] for i in range(1, len(roles) - 1))


# --------------------------------------------------------------------------- leak guard
@pytest.mark.parametrize("text,answer,expected", [
    ("So x = 3 is the answer", "x = 3", True),
    ("so x=3", "x = 3", True),
    ("Subtract 4. That is step 3 of the method.", "3", False),
    ("The answer is 3.", "3", True),
    ("Then 6 / 2 = 3", "3", True),
    ("The result is 30", "3", False),
    ("What do you get when you subtract 4 from both sides?", "x = 3", False),
    ("Jibu ni 3", "3", True),
    ("x = 2.5 is not right", "2.5", True),
])
def test_leaks_answer(text, answer, expected):
    assert leaks_answer(text, answer) is expected


# --------------------------------------------------------------------------- service
def _service(chunks_file, replies):
    client = FakeClient(replies)
    return ArtificialTeacherService(client, RetrievalService(chunks_file)), client


def test_service_grounded_response_and_sources(chunks_file):
    svc, client = _service(chunks_file, ["Let us balance it. What do you subtract first?"])
    res = svc.respond(TeachingRequest(subject="Mathematics", topic="Linear Equations", student=_student(),
                                      message="I do not understand"))
    assert res.grounded and res.sources and res.teaching_mode == "REVISE" and res.language == "en"
    assert res.model == "fake-gemma" and res.warnings == []
    assert "Test Book" in client.calls[0][0]["content"]


def test_service_ungrounded_warning_and_unknown_action(chunks_file):
    svc, _ = _service(chunks_file, ["Ok?"])
    res = svc.respond(TeachingRequest(subject="Chemistry", topic="Acids", message="help",
                                      student=_student(recommended_action="DANCE")))
    assert not res.grounded
    assert "no_curriculum_excerpts" in res.warnings
    assert any(w.startswith("unknown_recommended_action") for w in res.warnings)


def test_service_retries_once_when_answer_leaks(chunks_file):
    a = AssessmentResult(question="Solve 2x+4=10", student_answer="x=2.5", is_correct=False, verified_answer="x = 3")
    svc, client = _service(chunks_file, ["The answer is x = 3.", "What do you get after subtracting 4 from both sides?"])
    res = svc.respond(TeachingRequest(subject="Mathematics", topic="Linear Equations", student=_student(), assessment=a))
    assert len(client.calls) == 2 and "x = 3" not in res.response and res.warnings == []
    assert "previous draft stated the final answer" in client.calls[1][-1]["content"]


def test_service_flags_persistent_leak(chunks_file):
    a = AssessmentResult(question="q", student_answer="a", is_correct=False, verified_answer="x = 3")
    svc, client = _service(chunks_file, ["x = 3"])
    res = svc.respond(TeachingRequest(subject="Mathematics", topic="Linear Equations", student=_student(), assessment=a))
    assert len(client.calls) == 2 and "possible_answer_leak" in res.warnings


def test_service_no_retry_when_reveal_allowed(chunks_file):
    a = AssessmentResult(question="q", student_answer="a", is_correct=False, verified_answer="x = 3", reveal_answer=True)
    svc, client = _service(chunks_file, ["x = 3"])
    svc.respond(TeachingRequest(subject="Mathematics", topic="Linear Equations", student=_student(), assessment=a))
    assert len(client.calls) == 1


def test_service_empty_message_is_rejected_but_assessment_only_is_fine(chunks_file):
    svc, _ = _service(chunks_file, ["Good. Try this?"])
    with pytest.raises(ValueError):
        svc.respond(TeachingRequest(subject="Mathematics", topic="Linear Equations", student=_student(), message="  "))
    a = AssessmentResult(question="q", student_answer="x = 3", is_correct=True)
    res = svc.respond(TeachingRequest(subject="Mathematics", topic="Linear Equations", student=_student(), assessment=a))
    assert res.response


# --------------------------------------------------------------------------- client
def _client(handler, **kw):
    return GemmaClient(base_url="http://test", model="gemma3:4b",
                       http_client=httpx.Client(transport=httpx.MockTransport(handler)), **kw)


def test_client_success_and_payload():
    seen = {}

    def handler(req):
        seen.update(json.loads(req.content))
        return httpx.Response(200, json={"message": {"role": "assistant", "content": "  Hello  "}})

    assert _client(handler).chat([{"role": "user", "content": "hi"}]) == "Hello"
    assert seen["model"] == "gemma3:4b" and seen["stream"] is False and "num_ctx" in seen["options"]


def test_client_errors():
    def refuse(req):
        raise httpx.ConnectError("refused")

    def slow(req):
        raise httpx.ReadTimeout("slow")

    with pytest.raises(ModelUnavailableError, match="Cannot reach Ollama"):
        _client(refuse).chat([])
    with pytest.raises(ModelTimeoutError):
        _client(slow).chat([])
    with pytest.raises(ModelUnavailableError, match="ollama pull gemma3:4b"):
        _client(lambda r: httpx.Response(404, json={"error": "not found"})).chat([])
    with pytest.raises(ModelResponseError):
        _client(lambda r: httpx.Response(500, text="boom")).chat([])
    with pytest.raises(ModelResponseError, match="empty"):
        _client(lambda r: httpx.Response(200, json={"message": {"content": "  "}})).chat([])


def test_client_busy_when_all_slots_taken():
    c = _client(lambda r: httpx.Response(200, json={"message": {"content": "x"}}), max_concurrent=1, queue_timeout=0.05)
    assert c._slots.acquire(timeout=0.1)
    with pytest.raises(ModelBusyError):
        c.chat([])
    c._slots.release()
    assert c.chat([]) == "x"


def test_client_health():
    ok = _client(lambda r: httpx.Response(200, json={"models": [{"name": "gemma3:4b"}]})).health()
    assert ok["reachable"] and ok["model_installed"]
    missing = _client(lambda r: httpx.Response(200, json={"models": [{"name": "llama3:8b"}]})).health()
    assert missing["reachable"] and not missing["model_installed"]

    def down(req):
        raise httpx.ConnectError("refused")

    assert _client(down).health()["reachable"] is False
