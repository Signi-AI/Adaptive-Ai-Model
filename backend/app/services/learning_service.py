"""Server-owned Artificial Teacher orchestration for a learning session."""
import uuid
import json
import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.model_client import ask_artificial_teacher
from app.models.chat_message import ChatMessage, ChatRole
from app.models.attempt import Attempt
from app.models.generated_question import GeneratedQuestion
from app.models.learning_session import LearningSession
from app.models.lesson import Lesson
from app.models.subject import Subject
from app.models.topic import Topic
from app.models.user import User
from app.services.adaptive_service import AdaptiveService
from app.services.mastery_service import MasteryService
from app.services import session_service
from app.services.recommendation_service import RecommendationService


def _model_class_level(value: object) -> str:
    """Turn the database enum (FORM_2) into the model contract's Form 2."""
    text = getattr(value, "value", str(value))
    return text.replace("_", " ").title()


def _curriculum_level_key(value: object | None) -> str:
    """Compare registration enums with friendly curriculum level labels."""
    text = str(getattr(value, "value", value) or "").lower()
    return re.sub(r"[^a-z0-9]", "", text).replace("standard", "std")


def _owned_session(db: Session, student_id: uuid.UUID, session_id: uuid.UUID) -> LearningSession:
    session = db.get(LearningSession, session_id)
    if session is None or session.student_id != student_id:
        raise LookupError("Learning session not found")
    return session


def start_session(
    db: Session,
    student_id: uuid.UUID,
    subject_id: uuid.UUID,
    topic_id: uuid.UUID,
    lesson_id: uuid.UUID | None = None,
) -> LearningSession:
    subject = db.get(Subject, subject_id)
    topic = db.get(Topic, topic_id)
    if subject is None or not subject.active:
        raise LookupError("Subject not found")
    if topic is None or not topic.active or topic.subject_id != subject.id:
        raise ValueError("Topic does not belong to the selected subject")
    student = db.get(User, student_id)
    if student is None or student.class_level is None:
        raise ValueError("Student class level is required before starting a learning session")
    level = subject.academic_level
    if level is None or _curriculum_level_key(student.class_level) not in {
        _curriculum_level_key(level.code), _curriculum_level_key(level.name),
    }:
        raise ValueError("This subject is not assigned to the student's registered class")
    if lesson_id is not None:
        lesson = db.get(Lesson, lesson_id)
        if lesson is None or lesson.topic_id != topic.id:
            raise ValueError("Lesson does not belong to the selected topic")
    return session_service.record_session(db, student_id, subject_id, topic_id, lesson_id)


def _teacher_payload(db: Session, student: User, session: LearningSession, message: str) -> dict:
    subject = db.get(Subject, session.subject_id)
    topic = db.get(Topic, session.topic_id)
    if subject is None or topic is None:
        raise LookupError("The curriculum for this learning session is no longer available")
    if student.class_level is None:
        raise ValueError("Student class level is required before starting a learning session")

    state = MasteryService.get_topic_learning_state(db, student.id, topic.id)
    all_state = MasteryService.get_student_learning_state(db, student.id)
    decision = AdaptiveService.decide_next_action(db, student.id, topic.id, str(session.id), persist=False)
    rows = db.execute(
        select(ChatMessage)
        .where(ChatMessage.student_id == student.id, ChatMessage.learning_session_id == session.id)
        .order_by(ChatMessage.created_at.desc())
        .limit(8)
    ).scalars().all()
    history = [
        {"role": "student" if row.role == ChatRole.STUDENT else "teacher", "content": row.content}
        for row in reversed(rows)
    ]
    return {
        "subject": subject.name,
        "topic": topic.name,
        "student": {
            "display_name": student.full_name[:50],
            "class_level": _model_class_level(student.class_level),
            "mastery": state.mastery_score,
            "strengths": [item.topic_name for item in all_state.strengths[:8]],
            "weaknesses": [item.topic_name for item in all_state.weaknesses[:8]],
            "recent_performance": (
                "unknown" if state.attempts == 0 else
                "poor" if state.recent_performance < 0.4 else
                "developing" if state.recent_performance < 0.65 else
                "good" if state.recent_performance < 0.85 else "excellent"
            ),
            "recommended_action": decision.action.value,
        },
        "message": message,
        "history": history,
    }


def post_chat_message(
    db: Session, student: User, session_id: uuid.UUID, message: str
) -> tuple[ChatMessage, ChatMessage]:
    session = _owned_session(db, student.id, session_id)
    payload = _teacher_payload(db, student, session, message.strip())
    reply_text = ask_artificial_teacher(payload)["response"].strip()

    student_row = ChatMessage(
        student_id=student.id,
        learning_session_id=session.id,
        role=ChatRole.STUDENT,
        content=message.strip(),
    )
    db.add(student_row)
    db.flush()
    reply_row = ChatMessage(
        student_id=student.id,
        learning_session_id=session.id,
        role=ChatRole.AI_TEACHER,
        content=reply_text,
    )
    db.add(reply_row)

    db.commit()
    db.refresh(student_row)
    db.refresh(reply_row)
    return student_row, reply_row


def get_chat_history(db: Session, student_id: uuid.UUID, session_id: uuid.UUID) -> list[ChatMessage]:
    _owned_session(db, student_id, session_id)
    result = db.execute(
        select(ChatMessage)
        .where(ChatMessage.student_id == student_id, ChatMessage.learning_session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
    )
    return list(result.scalars().all())


def get_practice_question(
    db: Session, student_id: uuid.UUID, session_id: uuid.UUID
) -> GeneratedQuestion:
    """Return only a question prompt; its answer remains server-side."""
    session = _owned_session(db, student_id, session_id)
    question = db.execute(
        select(GeneratedQuestion)
        .where(
            GeneratedQuestion.subject_id == session.subject_id,
            GeneratedQuestion.topic_id == session.topic_id,
        )
        .order_by(GeneratedQuestion.created_at.desc())
        .limit(1)
    ).scalar_one_or_none()
    if question is None:
        raise LookupError("No practice question is configured for this topic yet")
    return question


def _answer_text(value: object) -> str:
    if isinstance(value, str):
        return value.strip()
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _normalise_answer(value: str) -> str:
    return " ".join(value.casefold().split())


def submit_attempt(
    db: Session,
    student_id: uuid.UUID,
    session_id: uuid.UUID,
    question_id: uuid.UUID,
    student_answer: str,
    client_submission_id: uuid.UUID,
) -> tuple[Attempt, object, object, list[object]]:
    """Evaluate an existing backend-generated question and atomically update learning state."""
    session = _owned_session(db, student_id, session_id)
    existing = db.execute(
        select(Attempt).where(
            Attempt.student_id == student_id,
            Attempt.client_submission_id == client_submission_id,
        )
    ).scalar_one_or_none()
    if existing is not None:
        state = MasteryService.get_topic_learning_state(db, student_id, existing.topic_id)
        decision = AdaptiveService.get_latest_decision(db, student_id, existing.topic_id)
        return existing, state, decision, []

    question = db.get(GeneratedQuestion, question_id)
    if question is None:
        raise LookupError("Question not found")
    if question.subject_id != session.subject_id or question.topic_id != session.topic_id:
        raise ValueError("Question does not belong to this learning session")

    expected = _answer_text(question.correct_answer)
    correct = _normalise_answer(student_answer) == _normalise_answer(expected)
    attempt = Attempt(
        student_id=student_id,
        client_submission_id=client_submission_id,
        subject_id=session.subject_id,
        topic_id=session.topic_id,
        lesson_id=question.lesson_id,
        learning_objective_id=question.learning_objective_id,
        question_id=question.id,
        session_id=session.id,
        question_text=question.generated_text,
        student_answer=student_answer.strip(),
        expected_answer=expected,
        is_correct=correct,
        score=1.0 if correct else 0.0,
        result="CORRECT" if correct else "INCORRECT",
        difficulty=3,
        ai_feedback="Correct. Keep building on this idea." if correct else "Not quite. Review the concept and try a guided example.",
    )
    try:
        db.add(attempt)
        db.flush()
        state = MasteryService.record_attempt(db, attempt.to_evidence(), commit=False)
        decision = AdaptiveService.decide_next_action(
            db, student_id, session.topic_id, str(session.id), commit=False
        )
        recommendations = RecommendationService.generate_from_decision(
            db, student_id, decision, commit=False
        )
        db.commit()
        db.refresh(attempt)
        return attempt, state, decision, recommendations
    except Exception:
        db.rollback()
        raise
