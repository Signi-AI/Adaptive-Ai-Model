"""Thin, validated client for the local Artificial Teacher service."""
from __future__ import annotations

from typing import Any

import httpx

from app.core.config import get_settings


class TeacherModelError(RuntimeError):
    def __init__(self, detail: str, status_code: int) -> None:
        super().__init__(detail)
        self.status_code = status_code


def _detail(response: httpx.Response) -> str:
    try:
        value = response.json().get("detail")
        if isinstance(value, str) and value.strip():
            return value.strip()
    except (ValueError, AttributeError):
        pass
    return "The Artificial Teacher is temporarily unavailable. Please try again."


def ask_artificial_teacher(payload: dict[str, Any]) -> dict[str, Any]:
    """Call the loopback model server without accepting model context from a browser."""
    settings = get_settings()
    headers = {"X-Model-Key": settings.teacher_model_api_key} if settings.teacher_model_api_key else {}
    try:
        with httpx.Client(trust_env=False, timeout=settings.teacher_model_timeout_seconds) as client:
            response = client.post(
                f"{settings.teacher_model_url.rstrip('/')}/v1/teach",
                json=payload,
                headers=headers,
            )
    except httpx.TimeoutException as error:
        raise TeacherModelError("The Artificial Teacher took too long to respond. Please try again.", 504) from error
    except httpx.HTTPError as error:
        raise TeacherModelError("The Artificial Teacher is unavailable. Check that the local model service is running.", 503) from error

    if response.status_code in (502, 503, 504):
        raise TeacherModelError(_detail(response), response.status_code)
    if response.status_code == 401:
        raise TeacherModelError("The Artificial Teacher service is not configured correctly.", 503)
    if response.status_code >= 400:
        raise TeacherModelError("The Artificial Teacher rejected this request.", 502)

    try:
        data = response.json()
    except ValueError as error:
        raise TeacherModelError("The Artificial Teacher returned an invalid response.", 502) from error
    if not isinstance(data, dict) or not isinstance(data.get("response"), str) or not data["response"].strip():
        raise TeacherModelError("The Artificial Teacher returned an invalid response.", 502)
    return data
