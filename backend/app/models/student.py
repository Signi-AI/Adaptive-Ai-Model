"""
models/student.py

Student identity and profile data ONLY.

Login credentials (username, password hash, PIN — whatever the future
Authentication issue lands on) deliberately do NOT live on this table.
Keeping "who is this student" separate from "how do they prove it's
them" means Authentication can add its own table/columns later without
a migration that reshapes this one — and it matches the DB-backed
session design already agreed on for this project (a sessions table
keyed by student_id, not credentials baked into Student itself).
"""

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Free-text for now (e.g. "Form 2", "Standard 5") rather than an
    # enum or a class_levels lookup table. Tanzania's exact
    # Standard/Form taxonomy isn't defined anywhere in the project
    # docs yet, and this issue explicitly says not to over-build in
    # Week 1. Tightening this into a real enum/lookup table is a
    # sensible follow-up once curriculum content is actually being
    # seeded and the valid class list is nailed down.
    class_level: Mapped[str] = mapped_column(String(50), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
