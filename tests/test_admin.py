"""
Tests for the Admin & Role Management domain: role storage, admin
authentication/authorization, user listing, the generic role-change
endpoint, and every privilege-escalation rule in section 15/23 of the
issue. Sync, self-contained, real database.

Run from the project root:

    pytest tests/test_admin.py --noconftest -v

Set TEST_DATABASE_URL to point at a throwaway database; if unset, whatever
DATABASE_URL resolves to is used. These tests never create/drop tables --
they create uniquely-named rows and delete exactly those afterwards. Roles
must already exist (role_service.ensure_core_roles_exist) -- the client
fixture below guarantees this by booting the app through its lifespan.
"""
import os
import sys
import uuid
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

if os.environ.get("TEST_DATABASE_URL"):
    os.environ["DATABASE_URL"] = os.environ["TEST_DATABASE_URL"]
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-not-for-production")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import delete  # noqa: E402

from backend.app.core.database import SessionLocal  # noqa: E402
from backend.app.main import app  # noqa: E402
from backend.app.models.chat_message import ChatMessage  # noqa: E402
from backend.app.models.role import UserRole  # noqa: E402
from backend.app.models.teacher import TeacherGuidance, TeacherStudentAssignment  # noqa: E402
from backend.app.models.user import User, UserSession  # noqa: E402
from backend.app.services import admin_service, role_service, user_service  # noqa: E402

PASSWORD = "a-strong-password"


class _Factory:
    def __init__(self):
        self.user_ids: list[uuid.UUID] = []

    def student(self) -> SimpleNamespace:
        from backend.app.models.user import ClassLevel
        from backend.app.schemas.student import RegisterRequest

        username = f"s_{uuid.uuid4().hex[:10]}"
        with SessionLocal() as db:
            user = user_service.register_student(
                db,
                RegisterRequest(username=username, full_name="Test Student", password=PASSWORD, class_level=ClassLevel.FORM_2),
            )
            self.user_ids.append(user.id)
            return SimpleNamespace(id=user.id, username=username)

    def teacher(self) -> SimpleNamespace:
        username = f"t_{uuid.uuid4().hex[:10]}"
        with SessionLocal() as db:
            user = user_service.create_teacher_user(db, username=username, full_name="Test Teacher", password=PASSWORD)
            self.user_ids.append(user.id)
            return SimpleNamespace(id=user.id, username=username)

    def admin(self) -> SimpleNamespace:
        username = f"a_{uuid.uuid4().hex[:10]}"
        with SessionLocal() as db:
            role = role_service.get_role_by_name(db, UserRole.ADMIN)
            from backend.app.core.security import hash_password

            user = User(username=username, full_name="Test Admin", password_hash=hash_password(PASSWORD), role_id=role.id)
            db.add(user)
            db.commit()
            db.refresh(user)
            self.user_ids.append(user.id)
            return SimpleNamespace(id=user.id, username=username)

    def cleanup(self):
        with SessionLocal() as db:
            db.execute(
                delete(TeacherGuidance).where(
                    TeacherGuidance.teacher_id.in_(self.user_ids) | TeacherGuidance.student_id.in_(self.user_ids)
                )
            )
            db.execute(
                delete(TeacherStudentAssignment).where(
                    TeacherStudentAssignment.teacher_id.in_(self.user_ids)
                    | TeacherStudentAssignment.student_id.in_(self.user_ids)
                )
            )
            db.execute(delete(ChatMessage).where(ChatMessage.student_id.in_(self.user_ids)))
            db.execute(delete(UserSession).where(UserSession.user_id.in_(self.user_ids)))
            db.execute(delete(User).where(User.id.in_(self.user_ids)))
            db.commit()


@pytest.fixture()
def factory():
    f = _Factory()
    yield f
    f.cleanup()


@pytest.fixture(scope="module")
def client():
    # Context-manager form triggers the lifespan startup event, which seeds
    # the three core roles -- required before any user can be created.
    with TestClient(app) as c:
        yield c


def _login(client, username: str, password: str = PASSWORD) -> dict:
    r = client.post("/auth/login", data={"username": username, "password": password})
    assert r.status_code == 200, r.text
    return r.json()


def _headers(token_response: dict) -> dict:
    return {"Authorization": f"Bearer {token_response['access_token']}"}


# --------------------------------------------------------------------------
# Role tests
# --------------------------------------------------------------------------

def test_core_roles_exist_and_are_exactly_three(client):
    # `client` is unused directly -- it's here to force the app's lifespan
    # (which seeds the three roles) to have already run, rather than
    # relying on incidental test execution order.
    with SessionLocal() as db:
        roles = {r.name for r in role_service.list_roles(db)}
    assert roles == {"ADMIN", "TEACHER", "STUDENT"}


def test_role_seeding_is_idempotent():
    with SessionLocal() as db:
        role_service.ensure_core_roles_exist(db)
        role_service.ensure_core_roles_exist(db)
        roles = role_service.list_roles(db)
    names = [r.name for r in roles]
    assert sorted(names) == ["ADMIN", "STUDENT", "TEACHER"]  # no duplicates


def test_get_role_by_name_resolves_each_role(client):
    with SessionLocal() as db:
        for role_enum in (UserRole.ADMIN, UserRole.TEACHER, UserRole.STUDENT):
            role = role_service.get_role_by_name(db, role_enum)
            assert role.name == role_enum.value


def test_get_admin_roles_endpoint_lists_three_with_descriptions(client, factory):
    a = factory.admin()
    r = client.get("/admin/roles", headers=_headers(_login(client, a.username)))
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 3
    assert all(row["description"] for row in body)
    assert all(row["is_active"] is True for row in body)


# --------------------------------------------------------------------------
# Admin authentication / authorization
# --------------------------------------------------------------------------

def test_admin_authenticates_through_the_same_login_as_everyone(client, factory):
    a = factory.admin()
    r = client.post("/auth/login", data={"username": a.username, "password": PASSWORD})
    assert r.status_code == 200
    schemes = client.get("/openapi.json").json()["components"]["securitySchemes"]
    assert set(schemes) == {"OAuth2PasswordBearer"}  # still one scheme -- admin didn't add a second


def test_unauthenticated_cannot_access_admin_routes(client):
    assert client.get("/admin/users").status_code == 401
    assert client.get("/admin/roles").status_code == 401


def test_student_cannot_access_admin_routes(client, factory):
    s = factory.student()
    headers = _headers(_login(client, s.username))
    assert client.get("/admin/users", headers=headers).status_code == 403
    assert client.patch(f"/admin/users/{s.id}/role", json={"role": "ADMIN"}, headers=headers).status_code == 403


def test_teacher_cannot_access_admin_routes(client, factory):
    t = factory.teacher()
    headers = _headers(_login(client, t.username))
    assert client.get("/admin/users", headers=headers).status_code == 403


def test_admin_can_access_admin_routes(client, factory):
    a = factory.admin()
    r = client.get("/admin/users", headers=_headers(_login(client, a.username)))
    assert r.status_code == 200


# --------------------------------------------------------------------------
# Admin user management
# --------------------------------------------------------------------------

def test_admin_can_list_and_view_users_without_sensitive_fields(client, factory):
    a = factory.admin()
    s = factory.student()
    headers = _headers(_login(client, a.username))

    listing = client.get("/admin/users", headers=headers)
    assert listing.status_code == 200
    ids = {row["id"] for row in listing.json()}
    assert str(s.id) in ids
    assert all("password_hash" not in row and "password" not in row for row in listing.json())

    single = client.get(f"/admin/users/{s.id}", headers=headers)
    assert single.status_code == 200
    assert single.json()["role"] == "STUDENT"
    assert "password_hash" not in single.json()


def test_admin_list_can_filter_by_role(client, factory):
    a = factory.admin()
    t = factory.teacher()
    headers = _headers(_login(client, a.username))
    r = client.get("/admin/users", params={"role": "TEACHER"}, headers=headers)
    assert r.status_code == 200
    assert all(row["role"] == "TEACHER" for row in r.json())
    assert str(t.id) in {row["id"] for row in r.json()}


def test_admin_viewing_unknown_user_gets_404(client, factory):
    a = factory.admin()
    r = client.get(f"/admin/users/{uuid.uuid4()}", headers=_headers(_login(client, a.username)))
    assert r.status_code == 404


# --------------------------------------------------------------------------
# Assigning roles (the generic PATCH endpoint)
# --------------------------------------------------------------------------

def test_admin_can_assign_each_role_via_the_generic_endpoint(client, factory):
    a = factory.admin()
    s, t = factory.student(), factory.teacher()
    headers = _headers(_login(client, a.username))

    r1 = client.patch(f"/admin/users/{s.id}/role", json={"role": "TEACHER"}, headers=headers)
    assert r1.status_code == 200 and r1.json()["role"] == "TEACHER"

    r2 = client.patch(f"/admin/users/{t.id}/role", json={"role": "STUDENT"}, headers=headers)
    assert r2.status_code == 200 and r2.json()["role"] == "STUDENT"

    r3 = client.patch(f"/admin/users/{s.id}/role", json={"role": "ADMIN"}, headers=headers)
    assert r3.status_code == 200 and r3.json()["role"] == "ADMIN"


def test_assigning_the_same_role_is_rejected(client, factory):
    a = factory.admin()
    s = factory.student()
    r = client.patch(f"/admin/users/{s.id}/role", json={"role": "STUDENT"}, headers=_headers(_login(client, a.username)))
    assert r.status_code == 409


def test_role_change_erases_data_from_the_old_role(client, factory):
    a = factory.admin()
    s = factory.student()
    headers = _headers(_login(client, a.username))
    student_headers = _headers(_login(client, s.username))
    client.post("/learning/session/message", json={"message": "hi"}, headers=student_headers)

    with SessionLocal() as db:
        assert db.query(ChatMessage).filter(ChatMessage.student_id == s.id).count() == 2

    r = client.patch(f"/admin/users/{s.id}/role", json={"role": "TEACHER"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["role"] == "TEACHER"

    with SessionLocal() as db:
        assert db.query(ChatMessage).filter(ChatMessage.student_id == s.id).count() == 0
        refreshed = db.get(User, s.id)
        assert refreshed.class_level is None
        assert refreshed.phone_number is None  # blank start in the new role too


def test_invalid_role_value_rejected(client, factory):
    a = factory.admin()
    s = factory.student()
    r = client.patch(f"/admin/users/{s.id}/role", json={"role": "SUPERUSER"}, headers=_headers(_login(client, a.username)))
    assert r.status_code == 422


def test_changing_role_for_unknown_user_is_404(client, factory):
    a = factory.admin()
    r = client.patch(f"/admin/users/{uuid.uuid4()}/role", json={"role": "TEACHER"}, headers=_headers(_login(client, a.username)))
    assert r.status_code == 404


# --------------------------------------------------------------------------
# Privilege escalation
# --------------------------------------------------------------------------

def test_registration_ignores_a_client_supplied_admin_role(client, factory):
    username = f"escalate_{uuid.uuid4().hex[:8]}"
    r = client.post(
        "/auth/register",
        json={"username": username, "full_name": "Attacker", "password": PASSWORD, "class_level": "FORM_1", "role": "ADMIN"},
    )
    assert r.status_code == 201
    assert r.json()["role"] == "STUDENT"  # the extra "role" field is simply ignored
    factory.user_ids.append(uuid.UUID(r.json()["id"]))


def test_non_admin_cannot_change_another_users_role(client, factory):
    t = factory.teacher()
    victim = factory.student()
    headers = _headers(_login(client, t.username))
    r = client.patch(f"/admin/users/{victim.id}/role", json={"role": "ADMIN"}, headers=headers)
    assert r.status_code == 403
    with SessionLocal() as db:
        assert db.get(User, victim.id).role.name == "STUDENT"  # unchanged


def test_student_cannot_promote_self(client, factory):
    s = factory.student()
    headers = _headers(_login(client, s.username))
    r = client.patch(f"/admin/users/{s.id}/role", json={"role": "ADMIN"}, headers=headers)
    assert r.status_code == 403


# --------------------------------------------------------------------------
# Final-admin protection
# --------------------------------------------------------------------------

def test_cannot_demote_the_last_active_admin(client, factory):
    # Use a dedicated, isolated admin so other admins created by earlier
    # tests in this module can't accidentally make this one "not the last."
    with SessionLocal() as db:
        db.execute(delete(User))  # start from a genuinely empty slate for this one
        db.commit()
    a = factory.admin()
    headers = _headers(_login(client, a.username))
    r = client.patch(f"/admin/users/{a.id}/role", json={"role": "TEACHER"}, headers=headers)
    assert r.status_code == 409
    with SessionLocal() as db:
        assert db.get(User, a.id).role.name == "ADMIN"  # unchanged


def test_can_demote_an_admin_when_another_active_admin_remains(client, factory):
    a1, a2 = factory.admin(), factory.admin()
    headers = _headers(_login(client, a1.username))
    r = client.patch(f"/admin/users/{a2.id}/role", json={"role": "TEACHER"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["role"] == "TEACHER"


def test_count_active_admins_excludes_the_given_user(client, factory):
    a = factory.admin()
    with SessionLocal() as db:
        assert admin_service.count_active_admins(db, excluding=a.id) == 0
        assert admin_service.count_active_admins(db) >= 1


# --------------------------------------------------------------------------
# Authentication integration -- role changes respected on next login
# --------------------------------------------------------------------------

def test_role_changes_are_respected_by_the_next_login(client, factory):
    a = factory.admin()
    s = factory.student()
    admin_headers = _headers(_login(client, a.username))

    client.patch(f"/admin/users/{s.id}/role", json={"role": "ADMIN"}, headers=admin_headers)

    new_tokens = _login(client, s.username)
    new_headers = _headers(new_tokens)
    assert client.get("/admin/users", headers=new_headers).status_code == 200
    assert client.get("/students/me", headers=new_headers).status_code == 403
