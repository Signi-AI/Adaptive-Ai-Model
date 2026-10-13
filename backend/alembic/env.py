from logging.config import fileConfig

from sqlalchemy import create_engine, pool

from logging.config import fileConfig
import os
import sys

# 🌟 Force Python to recognise the root directory path first
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, pool
from alembic import context
from app.core.config import get_settings

# 🌟 1. Load the models package FIRST. 
# This runs the clean __init__.py file we arranged, registering all models on the Base instance together.
import app.models  

# 🌟 2. NOW import Base safely. 
# Since app.models already ran, Python reads this from the local cache instead of re-running the configuration paths.
from app.core.database import Base 

# This is the Alembic Config object
config = context.config

target_metadata = Base.metadata


# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    settings = get_settings()
    url = settings.database_url

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """Helper method to execute context migrations."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    settings = get_settings()
    connectable = create_engine(settings.database_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        do_run_migrations(connection)

    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
