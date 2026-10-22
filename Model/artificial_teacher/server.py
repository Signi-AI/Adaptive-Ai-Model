"""Standalone Artificial Teacher model server. The backend talks to THIS over HTTP.

Start (from the model folder, ONE worker only, the concurrency limit lives in this process):
    uvicorn artificial_teacher.server:app --host 127.0.0.1 --port 8100

Keep it on 127.0.0.1. Only your backend should reach it. Set MODEL_API_KEY in model/.env if there is
any chance another machine can reach the port; the backend then sends it as the X-Model-Key header.
"""
from __future__ import annotations

import logging
import os
import secrets
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException, Request

from artificial_teacher.gemma_client import (
    GemmaClient,
    ModelBusyError,
    ModelError,
    ModelTimeoutError,
    ModelUnavailableError,
)
from artificial_teacher.retrieval_service import RetrievalService
from artificial_teacher.service import ArtificialTeacherService, TeachingRequest, TeachingResponse
from artificial_teacher.settings import load_env

log = logging.getLogger("artificial_teacher.server")


def _require_key(x_model_key: str | None = Header(default=None)) -> None:
    expected = os.getenv("MODEL_API_KEY", "")
    if expected and not secrets.compare_digest(x_model_key or "", expected):
        raise HTTPException(status_code=401, detail="Missing or invalid X-Model-Key header.")


def create_app(service: ArtificialTeacherService | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if getattr(app.state, "service", None) is None:
            load_env()  # must happen before GemmaClient/RetrievalService read their settings
            app.state.service = ArtificialTeacherService(GemmaClient(), RetrievalService())
            log.info("Teacher ready: model=%s chunks=%d", app.state.service.model_name, app.state.service.chunks_loaded)
        yield

    app = FastAPI(title="TOALM Artificial Teacher Model", version="1.0.0", lifespan=lifespan)
    app.state.service = service

    @app.get("/health")
    def health(request: Request) -> dict:
        h = request.app.state.service.health()
        ok = h["reachable"] and h["model_installed"]
        return {
            "status": "ok" if ok else "degraded",
            "model": h["model"],
            "ollama_reachable": h["reachable"],
            "model_installed": h["model_installed"],
            "chunks_loaded": h["chunks_loaded"],
        }

    @app.post("/v1/teach", response_model=TeachingResponse, dependencies=[Depends(_require_key)])
    def teach(req: TeachingRequest, request: Request) -> TeachingResponse:
        try:
            return request.app.state.service.respond(req)
        except ModelBusyError as exc:
            raise HTTPException(503, str(exc), headers={"Retry-After": "10"})
        except ModelUnavailableError as exc:
            raise HTTPException(503, str(exc))
        except ModelTimeoutError as exc:
            raise HTTPException(504, str(exc))
        except ModelError as exc:
            raise HTTPException(502, str(exc))
        except ValueError as exc:
            raise HTTPException(422, str(exc))

    return app


app = create_app()
