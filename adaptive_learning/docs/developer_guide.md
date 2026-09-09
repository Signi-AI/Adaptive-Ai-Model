# Developer Guide

## Principles

1. The adaptive engine must stay independent of UI, concrete DB, and any LLM.
2. Prefer small, focused classes with a single responsibility.
3. Business rules live in the adaptive engine or domain; repositories are thin.
4. Feature flags (`settings.enable_spaced_repetition`, `settings.enable_ai`) keep optional subsystems out of the hot path.

## Adding a new subject

1. Create `data/content/<subject>_seed.json` following the Mathematics schema.
2. Extend `scripts/init_db.py` (or write a small loader) to import it.
3. No code changes required in the adaptive engine.

## Adding a new adaptive algorithm

1. Place pure logic under `app/adaptive_engine/`.
2. Depend only on domain models and repository *interfaces*.
3. Wire it inside `AdaptiveLearningService.__init__`.
4. Add unit tests that need no database.

## Enabling spaced repetition

```python
from app.adaptive_engine.spaced_repetition import SimpleSM2Service
from app.config import settings

settings.enable_spaced_repetition = True
# Then inject SimpleSM2Service (or a repository-backed version)
# into the service constructor / factory.
```

## Enabling a local LLM

```python
from app.ai.base import AIProvider

class MyLlamaProvider(AIProvider):
    def is_available(self) -> bool: ...
    def enrich_feedback(...): ...

service = AdaptiveLearningService(session, ai_provider=MyLlamaProvider())
```

The adaptive engine never sees the concrete provider.

## Testing strategy

- **Unit** (`tests/unit/`): pure calculators (Mastery, Difficulty) – no DB.
- **Integration** (`tests/integration/`): full service + in-memory SQLite.
- Run: `pytest tests/ -v --cov=app`

## Common pitfalls

- Do not import SQLAlchemy models from the adaptive engine or domain.
- Do not put adaptive formulas inside repositories or the service layer.
- Always clamp mastery after every calculation.
- When adding a new repository method, also add it to the abstract base.

## Future sync

Implement `app.sync.base.SyncAdapter` and inject a concrete instance only when the deployment has network access. The default `NullSyncAdapter` keeps everything offline.
