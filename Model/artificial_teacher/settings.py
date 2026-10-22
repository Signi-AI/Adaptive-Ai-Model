"""Paths and .env loading for the standalone model folder.

Why this exists: relative paths must not depend on where you happen to start the program, and
the model folder keeps its OWN .env (it is a separate component from the backend).
"""
from __future__ import annotations

import os
from pathlib import Path

MODEL_ROOT = Path(__file__).resolve().parents[1]


def resolve_path(value: str | Path) -> Path:
    """Relative paths are relative to the model folder, never to the current directory."""
    p = Path(value)
    return p if p.is_absolute() else MODEL_ROOT / p


def load_env(env_file: Path | None = None) -> None:
    """Load KEY=VALUE lines from model/.env. Real environment variables win. No inline comments."""
    path = env_file or (MODEL_ROOT / ".env")
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8-sig").splitlines():  # utf-8-sig: Windows Notepad adds a BOM
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value
