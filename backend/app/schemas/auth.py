"""
Shared auth schemas. One login, one token shape, for every role -- this is
what replaced the separate LoginRequest-vs-teacher-form and
TokenResponse-vs-TeacherTokenResponse duplication.
"""
from datetime import datetime

from fastapi import Form
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str
    # Optional friendly label the frontend can send (e.g. from a device
    # picker in the UI) -- purely for the person's own session list, never
    # used to make a security decision.
    device_label: str | None = Field(default=None, max_length=255)

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...),
        device_label: str | None = Form(None),
    ) -> "LoginRequest":
        """
        Lets /auth/login accept OAuth2-style form data (what Swagger's
        Authorize dialog actually POSTs) while the route body still works
        with LoginRequest like a normal Pydantic model. Swagger also sends
        grant_type/scope/client_id/client_secret per the OAuth2 spec --
        those are simply ignored since they aren't declared as Form(...)
        parameters here.
        """
        return cls(username=username, password=password, device_label=device_label)


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: datetime
