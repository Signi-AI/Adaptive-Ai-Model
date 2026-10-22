"""Create the minimum local curriculum needed to run the existing learner UI.

This is deliberately idempotent: it only adds missing class levels, subjects,
and one starting topic per subject.  Replace/extend these starter records with
the school's approved curriculum before deployment.

Run from ``backend``:
    python -m app.scripts.seed_starter_curriculum
"""
from __future__ import annotations

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.academic_level import AcademicLevel
from app.models.subject import Subject
from app.models.topic import Topic


LEVELS = [*(f"STD_{number}" for number in range(1, 8)), *(f"FORM_{number}" for number in range(1, 7))]
SUBJECT_TOPICS = {
    "Mathematics": ["Algebra", "Geometry", "Statistics"],
    "Science": ["Matter", "Energy", "Living things"],
    "English": ["Grammar", "Writing", "Reading"],
    "Kiswahili": ["Sarufi", "Insha", "Methali"],
    "History": ["Early societies", "Colonial period", "Independence"],
    "Geography": ["Maps", "Weather", "Landforms"],
}


def _label(code: str) -> str:
    return code.replace("STD_", "Standard ").replace("FORM_", "Form ")


def main() -> None:
    with SessionLocal() as db:
        levels: dict[str, AcademicLevel] = {}
        for code in LEVELS:
            level = db.execute(select(AcademicLevel).where(AcademicLevel.code == code)).scalar_one_or_none()
            if level is None:
                level = AcademicLevel(name=_label(code), code=code, active=True)
                db.add(level)
                db.flush()
                print(f"added level: {code}")
            levels[code] = level

        for code, level in levels.items():
            for subject_name, topic_names in SUBJECT_TOPICS.items():
                subject = db.execute(
                    select(Subject).where(
                        Subject.academic_level_id == level.id,
                        Subject.name == subject_name,
                    )
                ).scalar_one_or_none()
                if subject is None:
                    subject = Subject(
                        name=subject_name,
                        code=f"{code}_{subject_name[:3].upper()}",
                        description=f"{subject_name} for {_label(code)}.",
                        academic_level_id=level.id,
                        active=True,
                    )
                    db.add(subject)
                    db.flush()
                    print(f"added subject: {code} / {subject_name}")

                for sequence, topic_name in enumerate(topic_names, start=1):
                    topic = db.execute(
                        select(Topic).where(Topic.subject_id == subject.id, Topic.name == topic_name)
                    ).scalar_one_or_none()
                    if topic is None:
                        db.add(Topic(
                            academic_level_id=level.id,
                            subject_id=subject.id,
                            name=topic_name,
                            description=f"Introduction to {topic_name}.",
                            sequence=sequence,
                            active=True,
                        ))

        db.commit()
    print("Starter curriculum is ready.")


if __name__ == "__main__":
    main()
