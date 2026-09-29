"""
Teacher domain tests (sync, self-contained).

Run from the project root with:

    pytest tests/test_teacher.py --noconftest -v

--noconftest keeps any other tests/conftest.py (e.g. an old async one) from
interfering. Tables must already exist in the target database. Set
TEST_DATABASE_URL to point at a throwaway database; if it isn't set, whatever
DATABASE_URL / .env resolves to is used. Either way these tests never
create or drop tables: they create uniquely-named rows and delete exactly
those rows afterwards.
"""
import hashlib
import os
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

if os.environ.get("TEST_DATABASE_URL"):
    os.environ["DATABASE_URL"] = os.environ["TEST_DATABASE_URL"]
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-not-for-production")

import jwt  # noqa: E402
import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import delete, update  # noqa: E402

from backend.app.core.config import get_settings  # noqa: E402
from backend.app.core.database import SessionLocal  # noqa: E402
from backend.app.core.security import create_access_token, hash_password  # noqa: E402
from backend.app.main import app  # noqa: E402
from backend.app.models.student import ClassLevel, Student, StudentSession, StudentStatus  # noqa: E402
from backend.app.models.teacher import (  # noqa: E402
    Teacher,
    TeacherGuidance,
    TeacherStatus,
    TeacherStudentAssignment,
)
from backend.app.schemas.teacher import (  # noqa: E402
    AttemptDetail,
    AttemptSummary,
    StudentProgressReport,
    SubjectProgress,
    TopicProgress,
)
from backend.app.services import teacher_learning_adapter, teacher_service  # noqa: E402

TEACHER_PASSWORD = "dev-only-teacher-password"
_STUDENT_HASH = hash_password("dev-only-student-password")


# --------------------------------------------------------------------------
# Fixtures / helpers
# --------------------------------------------------------------------------

class _Factory:
    """Creates rows directly and deletes exactly those rows afterwards."""

    def __init__(self):
        self.teacher_ids: list[uuid.UUID] = []
        self.student_ids: list[uuid.UUID] = []

    def teacher(self, full_name="Test Teacher"):
        email = f"t_{uuid.uuid4().hex[:10]}@example.test"
        with SessionLocal() as db:
            t = teacher_service.create_teacher(
                db, email=email, full_name=full_name, password=TEACHER_PASSWORD
            )
            self.teacher_ids.append(t.id)
            return SimpleNamespace(id=t.id, email=email, password=TEACHER_PASSWORD)

    def student(self, class_level=ClassLevel.FORM_2):
        with SessionLocal() as db:
            s = Student(
                username=f"s_{uuid.uuid4().hex[:10]}",
                full_name="Test Student",
                password_hash=_STUDENT_HASH,
                class_level=class_level,
                status=StudentStatus.ACTIVE,
            )
            db.add(s)
            db.commit()
            db.refresh(s)
            self.student_ids.append(s.id)
            return SimpleNamespace(id=s.id)

    def assign(self, teacher, student):
        with SessionLocal() as db:
            teacher_service.assign_student_to_teacher(db, teacher.id, student.id)

    def student_token(self, student) -> str:
        """A perfectly valid STUDENT access token (real session row + shared token)."""
        with SessionLocal() as db:
            sess = StudentSession(
                student_id=student.id,
                device_label="pytest",
                refresh_token_hash=(uuid.uuid4().hex * 2)[:64],
                expires_at=datetime.now(timezone.utc) + timedelta(days=1),
            )
            db.add(sess)
            db.commit()
            db.refresh(sess)
            token, _ = create_access_token(student_id=str(student.id), session_id=str(sess.id))
            return token

    def cleanup(self):
        with SessionLocal() as db:
            db.execute(
                delete(TeacherGuidance).where(
                    TeacherGuidance.teacher_id.in_(self.teacher_ids)
                    | TeacherGuidance.student_id.in_(self.student_ids)
                )
            )
            db.execute(
                delete(TeacherStudentAssignment).where(
                    TeacherStudentAssignment.teacher_id.in_(self.teacher_ids)
                    | TeacherStudentAssignment.student_id.in_(self.student_ids)
                )
            )
            db.execute(delete(StudentSession).where(StudentSession.student_id.in_(self.student_ids)))
            db.execute(delete(Teacher).where(Teacher.id.in_(self.teacher_ids)))
            db.execute(delete(Student).where(Student.id.in_(self.student_ids)))
            db.commit()


@pytest.fixture()
def factory():
    f = _Factory()
    yield f
    f.cleanup()


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def _login(client, teacher) -> dict:
    r = client.post("/teachers/login", data={"username": teacher.email, "password": teacher.password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def _forge_teacher_token(teacher_id, *, expires_delta: timedelta, secret: str | None = None) -> str:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {
            "sub": str(teacher_id),
            "role": "TEACHER",
            "type": "access",
            "iat": now - timedelta(hours=3),
            "exp": now + expires_delta,
        },
        secret or settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


# --------------------------------------------------------------------------
# Authentication
# --------------------------------------------------------------------------

def test_teacher_login_succeeds_and_returns_working_token(client, factory):
    t = factory.teacher()
    headers = _login(client, t)
    r = client.get("/teachers/me", headers=headers)
    assert r.status_code == 200
    assert r.json()["email"] == t.email


def test_login_email_is_case_insensitive(client, factory):
    t = factory.teacher()
    r = client.post(
        "/teachers/login", data={"username": t.email.upper(), "password": t.password}
    )
    assert r.status_code == 200


def test_invalid_credentials_rejected(client, factory):
    t = factory.teacher()
    wrong_pw = client.post("/teachers/login", data={"username": t.email, "password": "nope-nope-nope"})
    unknown = client.post(
        "/teachers/login", data={"username": "nobody@example.test", "password": "whatever-123"}
    )
    assert wrong_pw.status_code == 401
    assert unknown.status_code == 401
    assert wrong_pw.json()["detail"] == unknown.json()["detail"]  # no account enumeration


def test_expired_jwt_rejected(client, factory):
    t = factory.teacher()
    expired = _forge_teacher_token(t.id, expires_delta=timedelta(hours=-1))
    r = client.get("/teachers/me", headers={"Authorization": f"Bearer {expired}"})
    assert r.status_code == 401


def test_wrongly_signed_jwt_rejected(client, factory):
    t = factory.teacher()
    forged = _forge_teacher_token(
        t.id, expires_delta=timedelta(hours=1), secret="not-the-real-secret-at-all-0123456789"
    )
    r = client.get("/teachers/me", headers={"Authorization": f"Bearer {forged}"})
    assert r.status_code == 401


def test_student_token_cannot_access_teacher_endpoints(client, factory):
    s = factory.student()
    token = factory.student_token(s)
    headers = {"Authorization": f"Bearer {token}"}
    # Sanity: the token really is valid for the student side.
    assert client.get("/students/me", headers=headers).status_code == 200
    # ...but it must not open any teacher endpoint.
    assert client.get("/teachers/me", headers=headers).status_code == 403
    assert client.get("/teachers/me/students", headers=headers).status_code == 403
    assert client.patch("/teachers/me", json={"full_name": "Hacker"}, headers=headers).status_code == 403


def test_teacher_token_cannot_access_student_endpoints(client, factory):
    t = factory.teacher()
    r = client.get("/students/me", headers=_login(client, t))
    assert r.status_code == 401


def test_unauthenticated_requests_rejected(client):
    assert client.get("/teachers/me").status_code == 401
    assert client.get("/teachers/me/students").status_code == 401
    assert client.post(f"/teachers/me/students/{uuid.uuid4()}/guidance", json={"guidance_text": "x"}).status_code == 401


def test_deactivated_teacher_token_stops_working(client, factory):
    t = factory.teacher()
    headers = _login(client, t)
    assert client.get("/teachers/me", headers=headers).status_code == 200
    with SessionLocal() as db:
        db.execute(update(Teacher).where(Teacher.id == t.id).values(status=TeacherStatus.DEACTIVATED))
        db.commit()
    assert client.get("/teachers/me", headers=headers).status_code == 401


# --------------------------------------------------------------------------
# Profile
# --------------------------------------------------------------------------

def test_teacher_can_get_own_profile_without_sensitive_fields(client, factory):
    t = factory.teacher(full_name="Amina Teacher")
    r = client.get("/teachers/me", headers=_login(client, t))
    assert r.status_code == 200
    body = r.json()
    assert body["full_name"] == "Amina Teacher"
    assert "password_hash" not in body and "password" not in body


def test_teacher_can_update_own_profile(client, factory):
    t = factory.teacher()
    headers = _login(client, t)
    r = client.patch(
        "/teachers/me",
        json={"full_name": "  New Name  ", "phone_number": "+255 700 000 000", "specialization": "Physics"},
        headers=headers,
    )
    assert r.status_code == 200
    body = r.json()
    assert body["full_name"] == "New Name"
    assert body["phone_number"] == "+255 700 000 000"
    assert body["specialization"] == "Physics"

    cleared = client.patch("/teachers/me", json={"phone_number": None}, headers=headers)
    assert cleared.status_code == 200 and cleared.json()["phone_number"] is None
    assert cleared.json()["specialization"] == "Physics"  # untouched field stays


def test_profile_update_validation(client, factory):
    t = factory.teacher()
    headers = _login(client, t)
    assert client.patch("/teachers/me", json={"full_name": None}, headers=headers).status_code == 422
    assert client.patch("/teachers/me", json={"phone_number": "abc"}, headers=headers).status_code == 422


def test_teacher_cannot_modify_another_teachers_profile(client, factory):
    a = factory.teacher(full_name="Teacher A")
    b = factory.teacher(full_name="Teacher B")
    r = client.patch(
        "/teachers/me",
        json={
            "full_name": "Renamed A",
            "id": str(b.id),
            "email": b.email,
            "status": "DEACTIVATED",
        },
        headers=_login(client, a),
    )
    assert r.status_code == 200
    assert r.json()["id"] == str(a.id)
    assert r.json()["email"] == a.email
    assert r.json()["status"] == "ACTIVE"
    assert r.json()["full_name"] == "Renamed A"

    rb = client.get("/teachers/me", headers=_login(client, b))
    assert rb.json()["full_name"] == "Teacher B"


# --------------------------------------------------------------------------
# Student access / authorization
# --------------------------------------------------------------------------

def test_teacher_lists_only_assigned_students(client, factory):
    t, other = factory.teacher(), factory.teacher()
    s1, s2, s3 = factory.student(), factory.student(), factory.student()
    factory.assign(t, s1)
    factory.assign(t, s2)
    factory.assign(other, s3)

    r = client.get("/teachers/me/students", headers=_login(client, t))
    assert r.status_code == 200
    ids = {row["student_id"] for row in r.json()}
    assert ids == {str(s1.id), str(s2.id)}
    row = r.json()[0]
    assert set(row) >= {"student_id", "full_name", "class_level", "overall_progress", "last_activity_at"}
    assert "password_hash" not in row and "username" not in row


def test_teacher_can_view_assigned_student(client, factory):
    t, s = factory.teacher(), factory.student(ClassLevel.FORM_3)
    factory.assign(t, s)
    r = client.get(f"/teachers/me/students/{s.id}", headers=_login(client, t))
    assert r.status_code == 200
    body = r.json()
    assert body["profile"]["id"] == str(s.id)
    assert body["profile"]["class_level"] == "FORM_3"
    assert "password_hash" not in body["profile"]
    assert body["progress"]["learning_data_available"] is False
    assert body["recent_attempts"] == []
    assert body["recent_guidance"] == []


def test_teacher_cannot_view_unassigned_student(client, factory):
    t, s = factory.teacher(), factory.student()
    r = client.get(f"/teachers/me/students/{s.id}", headers=_login(client, t))
    assert r.status_code == 404


def test_teacher_cannot_access_another_teachers_student_on_any_route(client, factory):
    a, b = factory.teacher(), factory.teacher()
    s = factory.student()
    factory.assign(b, s)
    headers = _login(client, a)
    base = f"/teachers/me/students/{s.id}"
    assert client.get(base, headers=headers).status_code == 404
    assert client.get(f"{base}/progress", headers=headers).status_code == 404
    assert client.get(f"{base}/attempts", headers=headers).status_code == 404
    assert client.get(f"{base}/attempts/{uuid.uuid4()}", headers=headers).status_code == 404
    assert client.get(f"{base}/guidance", headers=headers).status_code == 404
    assert client.post(f"{base}/guidance", json={"guidance_text": "hi"}, headers=headers).status_code == 404


def test_unknown_and_malformed_student_ids_handled(client, factory):
    t = factory.teacher()
    headers = _login(client, t)
    unknown = client.get(f"/teachers/me/students/{uuid.uuid4()}/progress", headers=headers)
    assert unknown.status_code == 404
    malformed = client.get("/teachers/me/students/not-a-uuid/progress", headers=headers)
    assert malformed.status_code == 422


def test_ended_assignment_no_longer_grants_access(client, factory):
    t, s = factory.teacher(), factory.student()
    factory.assign(t, s)
    headers = _login(client, t)
    assert client.get(f"/teachers/me/students/{s.id}", headers=headers).status_code == 200
    with SessionLocal() as db:
        teacher_service.end_assignment(db, t.id, s.id)
    assert client.get(f"/teachers/me/students/{s.id}", headers=headers).status_code == 404
    assert client.get("/teachers/me/students", headers=headers).json() == []


# --------------------------------------------------------------------------
# Progress (consumes the Learning domain through the adapter)
# --------------------------------------------------------------------------

def test_progress_for_assigned_student_default_is_honest_empty(client, factory):
    t, s = factory.teacher(), factory.student()
    factory.assign(t, s)
    r = client.get(f"/teachers/me/students/{s.id}/progress", headers=_login(client, t))
    assert r.status_code == 200
    body = r.json()
    assert body["student_id"] == str(s.id)
    assert body["learning_data_available"] is False
    assert body["subjects"] == []


def test_progress_returns_learning_domain_data(client, factory, monkeypatch):
    t, s = factory.teacher(), factory.student()
    factory.assign(t, s)

    def fake_progress(db, student_id):
        return StudentProgressReport(
            student_id=student_id,
            learning_data_available=True,
            overall_progress=0.62,
            subjects=[
                SubjectProgress(
                    subject="Mathematics",
                    mastery=0.62,
                    topics=[
                        TopicProgress(
                            topic="Linear Equations",
                            attempts_count=10,
                            correct_count=7,
                            incorrect_count=3,
                            mastery=0.7,
                        )
                    ],
                )
            ],
            strengths=["Linear Equations"],
            weaknesses=["Fractions"],
            recommendations=["Review fractions before continuing"],
        )

    monkeypatch.setattr(teacher_learning_adapter, "get_student_progress", fake_progress)
    headers = _login(client, t)

    body = client.get(f"/teachers/me/students/{s.id}/progress", headers=headers).json()
    assert body["overall_progress"] == 0.62
    assert body["subjects"][0]["topics"][0]["correct_count"] == 7
    assert body["strengths"] == ["Linear Equations"]
    assert body["weaknesses"] == ["Fractions"]

    overview = client.get(f"/teachers/me/students/{s.id}", headers=headers).json()
    assert overview["progress"]["recommendations"] == ["Review fractions before continuing"]

    listing = client.get("/teachers/me/students", headers=headers).json()
    assert listing[0]["overall_progress"] == 0.62


# --------------------------------------------------------------------------
# Attempts
# --------------------------------------------------------------------------

def _install_fake_attempts(monkeypatch, student_id):
    attempt_id = uuid.uuid4()
    when = datetime(2026, 9, 27, 10, 0, tzinfo=timezone.utc)
    summary = AttemptSummary(
        id=attempt_id, subject="Mathematics", topic="Fractions", result="INCORRECT", score=0.0, attempted_at=when
    )
    detail = AttemptDetail(
        **summary.model_dump(),
        question="What is 1/2 + 1/4?",
        student_answer="2/6",
        expected_answer="3/4",
        ai_feedback="You added the denominators instead of finding a common one.",
    )
    monkeypatch.setattr(
        teacher_learning_adapter,
        "list_student_attempts",
        lambda db, sid, *, limit, offset: [summary] if sid == student_id else [],
    )
    monkeypatch.setattr(
        teacher_learning_adapter,
        "get_student_attempt",
        lambda db, sid, aid: detail if (sid == student_id and aid == attempt_id) else None,
    )
    return attempt_id


def test_attempts_default_is_empty_and_unknown_attempt_404(client, factory):
    t, s = factory.teacher(), factory.student()
    factory.assign(t, s)
    headers = _login(client, t)
    assert client.get(f"/teachers/me/students/{s.id}/attempts", headers=headers).json() == []
    assert client.get(f"/teachers/me/students/{s.id}/attempts/{uuid.uuid4()}", headers=headers).status_code == 404


def test_teacher_can_view_attempts_and_a_specific_attempt(client, factory, monkeypatch):
    t, s = factory.teacher(), factory.student()
    factory.assign(t, s)
    attempt_id = _install_fake_attempts(monkeypatch, s.id)
    headers = _login(client, t)

    listing = client.get(f"/teachers/me/students/{s.id}/attempts", headers=headers)
    assert listing.status_code == 200
    assert listing.json()[0]["id"] == str(attempt_id)

    one = client.get(f"/teachers/me/students/{s.id}/attempts/{attempt_id}", headers=headers)
    assert one.status_code == 200
    body = one.json()
    assert body["student_answer"] == "2/6"
    assert body["expected_answer"] == "3/4"
    assert "common one" in body["ai_feedback"]  # AI feedback present, and labelled as such

    assert client.get(f"/teachers/me/students/{s.id}/attempts?limit=0", headers=headers).status_code == 422


def test_unauthorized_attempt_access_rejected(client, factory, monkeypatch):
    owner_teacher, intruder = factory.teacher(), factory.teacher()
    s = factory.student()
    factory.assign(owner_teacher, s)
    attempt_id = _install_fake_attempts(monkeypatch, s.id)
    r = client.get(f"/teachers/me/students/{s.id}/attempts/{attempt_id}", headers=_login(client, intruder))
    assert r.status_code == 404


# --------------------------------------------------------------------------
# Guidance
# --------------------------------------------------------------------------

def test_teacher_can_create_guidance_for_assigned_student(client, factory):
    t, s = factory.teacher(), factory.student()
    factory.assign(t, s)
    r = client.post(
        f"/teachers/me/students/{s.id}/guidance",
        json={"guidance_text": "  Review multiplication of fractions before continuing.  ", "subject": "Mathematics", "topic": "Fractions"},
        headers=_login(client, t),
    )
    assert r.status_code == 201
    body = r.json()
    assert body["teacher_id"] == str(t.id)
    assert body["student_id"] == str(s.id)
    assert body["guidance_text"] == "Review multiplication of fractions before continuing."
    assert body["subject"] == "Mathematics"
    assert body["is_read"] is False
    assert body["source"] == "HUMAN_TEACHER"  # never confusable with AI feedback


def test_guidance_teacher_id_comes_from_token_not_body(client, factory):
    t, victim = factory.teacher(), factory.teacher()
    s = factory.student()
    factory.assign(t, s)
    r = client.post(
        f"/teachers/me/students/{s.id}/guidance",
        json={"guidance_text": "Try again.", "teacher_id": str(victim.id), "student_id": str(uuid.uuid4())},
        headers=_login(client, t),
    )
    assert r.status_code == 201
    assert r.json()["teacher_id"] == str(t.id)
    assert r.json()["student_id"] == str(s.id)


def test_teacher_can_retrieve_previous_guidance_newest_first(client, factory):
    t, s = factory.teacher(), factory.student()
    factory.assign(t, s)
    headers = _login(client, t)
    for text in ("first note", "second note", "third note"):
        assert client.post(f"/teachers/me/students/{s.id}/guidance", json={"guidance_text": text}, headers=headers).status_code == 201
    r = client.get(f"/teachers/me/students/{s.id}/guidance", headers=headers)
    assert r.status_code == 200
    assert [g["guidance_text"] for g in r.json()] == ["third note", "second note", "first note"]

    overview = client.get(f"/teachers/me/students/{s.id}", headers=headers).json()
    assert len(overview["recent_guidance"]) == 3


def test_teacher_only_sees_own_guidance_for_a_shared_student(client, factory):
    a, b = factory.teacher(), factory.teacher()
    s = factory.student()
    factory.assign(a, s)
    factory.assign(b, s)
    ha, hb = _login(client, a), _login(client, b)
    client.post(f"/teachers/me/students/{s.id}/guidance", json={"guidance_text": "from A"}, headers=ha)
    client.post(f"/teachers/me/students/{s.id}/guidance", json={"guidance_text": "from B"}, headers=hb)
    assert [g["guidance_text"] for g in client.get(f"/teachers/me/students/{s.id}/guidance", headers=ha).json()] == ["from A"]
    assert [g["guidance_text"] for g in client.get(f"/teachers/me/students/{s.id}/guidance", headers=hb).json()] == ["from B"]


def test_cannot_create_guidance_for_unassigned_student(client, factory):
    t, s = factory.teacher(), factory.student()
    r = client.post(f"/teachers/me/students/{s.id}/guidance", json={"guidance_text": "hello"}, headers=_login(client, t))
    assert r.status_code == 404
    with SessionLocal() as db:
        assert db.query(TeacherGuidance).filter(TeacherGuidance.student_id == s.id).count() == 0


def test_guidance_validation(client, factory):
    t, s = factory.teacher(), factory.student()
    factory.assign(t, s)
    headers = _login(client, t)
    url = f"/teachers/me/students/{s.id}/guidance"
    assert client.post(url, json={"guidance_text": "   "}, headers=headers).status_code == 422
    assert client.post(url, json={}, headers=headers).status_code == 422
    assert client.post(url, json={"guidance_text": "x" * 4001}, headers=headers).status_code == 422
    assert client.post(url, json={"guidance_text": "ok", "attempt_id": "nope"}, headers=headers).status_code == 422


def test_guidance_linked_to_valid_attempt_and_invalid_attempt_rejected(client, factory, monkeypatch):
    t, s = factory.teacher(), factory.student()
    factory.assign(t, s)
    attempt_id = _install_fake_attempts(monkeypatch, s.id)
    headers = _login(client, t)
    url = f"/teachers/me/students/{s.id}/guidance"

    ok = client.post(url, json={"guidance_text": "Check the common denominator.", "attempt_id": str(attempt_id)}, headers=headers)
    assert ok.status_code == 201
    assert ok.json()["attempt_id"] == str(attempt_id)
    assert ok.json()["subject"] == "Mathematics"  # defaulted from the attempt
    assert ok.json()["topic"] == "Fractions"

    bad = client.post(url, json={"guidance_text": "x", "attempt_id": str(uuid.uuid4())}, headers=headers)
    assert bad.status_code == 404
