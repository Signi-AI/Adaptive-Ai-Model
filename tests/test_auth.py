"""
Covers the DoD's authentication checks: registration, login, JWT
validity, protected-route rejection, refresh rotation, and logout.
"""
import pytest

from tests.conftest import unique_username

pytestmark = pytest.mark.asyncio


async def _register(client, username=None, password="a-strong-password", class_level="FORM_2"):
    username = username or unique_username()
    resp = await client.post(
        "/auth/register",
        json={
            "username": username,
            "full_name": "Test Student",
            "password": password,
            "class_level": class_level,
        },
    )
    return username, resp


async def test_successful_registration(client):
    _, resp = await _register(client)
    assert resp.status_code == 201
    body = resp.json()
    assert "password" not in body
    assert "password_hash" not in body


async def test_duplicate_registration_rejected(client):
    username, first = await _register(client)
    assert first.status_code == 201

    _, second = await _register(client, username=username)
    assert second.status_code == 409


async def test_registration_rejects_short_password(client):
    _, resp = await _register(client, password="short")
    assert resp.status_code == 422


async def test_successful_login(client):
    username, reg = await _register(client, password="a-strong-password")
    assert reg.status_code == 201

    resp = await client.post(
        "/auth/login", json={"username": username, "password": "a-strong-password"}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["access_token"]
    assert body["refresh_token"]


async def test_login_incorrect_password(client):
    username, reg = await _register(client, password="a-strong-password")
    assert reg.status_code == 201

    resp = await client.post(
        "/auth/login", json={"username": username, "password": "wrong-password"}
    )
    assert resp.status_code == 401


async def test_login_unknown_account(client):
    resp = await client.post(
        "/auth/login", json={"username": "no-such-student", "password": "whatever123"}
    )
    assert resp.status_code == 401


async def test_protected_endpoint_without_authentication(client):
    resp = await client.get("/students/me")
    # 403 is FastAPI's HTTPBearer default when no Authorization header is
    # sent at all; 401 is what we raise once a token is present but bad.
    assert resp.status_code in (401, 403)


async def test_protected_endpoint_with_invalid_token(client):
    resp = await client.get("/students/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert resp.status_code == 401


async def test_authenticated_student_can_access_own_profile(client):
    username, reg = await _register(client, password="a-strong-password")
    login = await client.post(
        "/auth/login", json={"username": username, "password": "a-strong-password"}
    )
    token = login.json()["access_token"]

    resp = await client.get("/students/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["username"] == username


async def test_refresh_issues_new_tokens_and_rotates_old_one(client):
    username, reg = await _register(client, password="a-strong-password")
    login = await client.post(
        "/auth/login", json={"username": username, "password": "a-strong-password"}
    )
    old_refresh = login.json()["refresh_token"]

    refreshed = await client.post("/auth/refresh", json={"refresh_token": old_refresh})
    assert refreshed.status_code == 200
    assert refreshed.json()["refresh_token"] != old_refresh

    # The rotated-out token must not work a second time.
    replay = await client.post("/auth/refresh", json={"refresh_token": old_refresh})
    assert replay.status_code == 401


async def test_logout_revokes_session_immediately(client):
    username, reg = await _register(client, password="a-strong-password")
    login = await client.post(
        "/auth/login", json={"username": username, "password": "a-strong-password"}
    )
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    logout = await client.post("/auth/logout", headers=headers)
    assert logout.status_code == 204

    # Same access token, now dead — the "instant revoke on a shared lab
    # PC" property, not just waiting for the JWT to expire on its own.
    after = await client.get("/students/me", headers=headers)
    assert after.status_code == 401
