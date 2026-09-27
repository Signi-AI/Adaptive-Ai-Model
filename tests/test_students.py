"""
Covers the DoD's profile and session-management checks, including the
ID-manipulation attack the issue explicitly calls out.
"""
import pytest

from tests.conftest import unique_username

pytestmark = pytest.mark.asyncio


async def _register_and_login(client, class_level="FORM_2"):
    username = unique_username()
    password = "a-strong-password"
    await client.post(
        "/auth/register",
        json={
            "username": username,
            "full_name": "Test Student",
            "password": password,
            "class_level": class_level,
        },
    )
    login = await client.post("/auth/login", json={"username": username, "password": password})
    token = login.json()["access_token"]
    return username, {"Authorization": f"Bearer {token}"}


async def test_update_own_profile(client):
    _, headers = await _register_and_login(client, class_level="FORM_1")

    resp = await client.patch(
        "/students/me",
        json={"full_name": "Updated Name", "class_level": "FORM_2"},
        headers=headers,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["full_name"] == "Updated Name"
    assert body["class_level"] == "FORM_2"


async def test_session_created_on_login_and_listed(client):
    _, headers = await _register_and_login(client)

    resp = await client.get("/students/me/sessions", headers=headers)
    assert resp.status_code == 200
    sessions = resp.json()
    assert len(sessions) == 1
    assert sessions[0]["is_current"] is True
    assert sessions[0]["revoked"] is False


async def test_student_can_revoke_own_session(client):
    _, headers = await _register_and_login(client)

    sessions = (await client.get("/students/me/sessions", headers=headers)).json()
    session_id = sessions[0]["id"]

    resp = await client.delete(f"/students/me/sessions/{session_id}", headers=headers)
    assert resp.status_code == 204


async def test_student_cannot_revoke_another_students_session(client):
    _, headers_a = await _register_and_login(client)
    _, headers_b = await _register_and_login(client)

    sessions_b = (await client.get("/students/me/sessions", headers=headers_b)).json()
    session_b_id = sessions_b[0]["id"]

    # Student A tries to revoke Student B's session by guessing/reading its ID.
    resp = await client.delete(f"/students/me/sessions/{session_b_id}", headers=headers_a)
    assert resp.status_code == 404  # not 403 — existence isn't confirmed either

    # And it's still alive for B.
    still_there = (await client.get("/students/me/sessions", headers=headers_b)).json()
    assert still_there[0]["revoked"] is False
