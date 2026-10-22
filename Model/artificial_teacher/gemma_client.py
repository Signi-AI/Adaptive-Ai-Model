"""Local Gemma client for the Artificial Teacher (talks to a local Ollama server).

Design rules
- Synchronous: the model server's routes are plain functions that FastAPI runs in a threadpool.
- Bounded concurrency: at most TEACHER_MAX_CONCURRENT requests are sent to the model at
  once. Extra callers wait up to TEACHER_QUEUE_TIMEOUT_SECONDS, then get ModelBusyError so
  the server can answer HTTP 503 instead of 40 students silently stacking up behind one CPU.
- Typed errors so the route can map every failure to a clear HTTP status.
- Offline: only ever talks to OLLAMA_BASE_URL (default http://127.0.0.1:11434).
"""
from __future__ import annotations

import os
import threading
from typing import Any

import httpx


class ModelError(Exception):
    """Base class for every model failure."""


class ModelUnavailableError(ModelError):
    """Ollama is not running, or the configured model has not been pulled."""


class ModelTimeoutError(ModelError):
    """The model did not answer within TEACHER_TIMEOUT_SECONDS."""


class ModelBusyError(ModelError):
    """Too many requests are already waiting for the model."""


class ModelResponseError(ModelError):
    """The model returned an error status or an empty reply."""


def _pick(value: Any, env_name: str, default: Any) -> Any:
    """Explicit argument wins, then environment variable, then default."""
    if value is not None:
        return value
    return os.getenv(env_name, default)


class GemmaClient:
    def __init__(
        self,
        *,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float | None = None,
        num_ctx: int | None = None,
        num_batch: int | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        max_concurrent: int | None = None,
        queue_timeout: float | None = None,
        keep_alive: str | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        self.base_url = str(_pick(base_url, "OLLAMA_BASE_URL", "http://127.0.0.1:11434")).rstrip("/")
        self.model = str(_pick(model, "TEACHER_MODEL", "gemma3:4b"))
        self.timeout = float(_pick(timeout, "TEACHER_TIMEOUT_SECONDS", 120))
        self.num_ctx = int(_pick(num_ctx, "TEACHER_NUM_CTX", 4096))
        self.num_batch = int(_pick(num_batch, "TEACHER_NUM_BATCH", 64))
        self.temperature = float(_pick(temperature, "TEACHER_TEMPERATURE", 0.4))
        self.max_tokens = int(_pick(max_tokens, "TEACHER_MAX_TOKENS", 400))
        self.queue_timeout = float(_pick(queue_timeout, "TEACHER_QUEUE_TIMEOUT_SECONDS", 60))
        self.keep_alive = str(_pick(keep_alive, "TEACHER_KEEP_ALIVE", "30m"))
        slots = int(_pick(max_concurrent, "TEACHER_MAX_CONCURRENT", 2))
        self._slots = threading.BoundedSemaphore(max(1, slots))
        # trust_env=False: never route localhost traffic through a school/office HTTP proxy.
        self._http = http_client or httpx.Client(trust_env=False)

    # ------------------------------------------------------------------ health
    def health(self) -> dict[str, Any]:
        """Is Ollama reachable, and is the configured model installed?"""
        try:
            resp = self._http.get(f"{self.base_url}/api/tags", timeout=5)
            resp.raise_for_status()
        except httpx.HTTPError as exc:
            return {"reachable": False, "model_installed": False, "installed_models": [], "detail": str(exc)}
        names = [m.get("name", "") for m in resp.json().get("models", [])]
        wanted = self.model if ":" in self.model else f"{self.model}:latest"
        return {
            "reachable": True,
            "model_installed": wanted in names,
            "installed_models": names,
            "detail": "ok",
        }

    # -------------------------------------------------------------------- chat
    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Send chat messages to the local model and return the reply text."""
        if not self._slots.acquire(timeout=self.queue_timeout):
            raise ModelBusyError("The teacher model is busy. Try again shortly.")
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "keep_alive": self.keep_alive,
                "options": {
                    "num_ctx": self.num_ctx,
                    "num_batch": self.num_batch,
                    "temperature": self.temperature if temperature is None else temperature,
                    "num_predict": self.max_tokens if max_tokens is None else max_tokens,
                },
            }
            try:
                resp = self._http.post(f"{self.base_url}/api/chat", json=payload, timeout=self.timeout)
            except httpx.TimeoutException as exc:
                raise ModelTimeoutError(f"Model did not answer within {self.timeout:.0f}s") from exc
            except httpx.HTTPError as exc:
                raise ModelUnavailableError(
                    f"Cannot reach Ollama at {self.base_url}. Is it running? ({exc})"
                ) from exc

            if resp.status_code == 404:
                raise ModelUnavailableError(
                    f"Model '{self.model}' is not installed. Run: ollama pull {self.model}"
                )
            if resp.status_code >= 400:
                raise ModelResponseError(f"Ollama returned HTTP {resp.status_code}: {resp.text[:200]}")

            text = ((resp.json().get("message") or {}).get("content") or "").strip()
            if not text:
                raise ModelResponseError("The model returned an empty reply.")
            return text
        finally:
            self._slots.release()
