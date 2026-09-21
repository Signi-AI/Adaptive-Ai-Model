"""
api/routes/learning.py
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.learning import (
    LessonCompletionRead,
    LessonProgress,
    LessonRead,
    SubjectRead,
    TopicDetail,
    TopicProgress,
    TopicRead,
)
from app.services import learning_service, session_service

router = APIRouter(tags=["learning"])


@router.get("/subjects", response_model=list[SubjectRead])
def list_subjects(db: Session = Depends(get_db)) -> list[SubjectRead]:
    return learning_service.get_subjects(db)


@router.get("/subjects/{subject_id}/topics", response_model=list[TopicRead])
def list_topics_for_subject(subject_id: int, db: Session = Depends(get_db)) -> list[TopicRead]:
    subject = learning_service.get_subject(db, subject_id)
    if subject is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
    return learning_service.get_topics_by_subject(db, subject_id)


@router.get("/topics/{topic_id}/lessons", response_model=list[LessonRead])
def list_lessons_for_topic(topic_id: int, db: Session = Depends(get_db)) -> list[LessonRead]:
    topic = learning_service.get_topic(db, topic_id)
    if topic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    return learning_service.get_lessons_by_topic(db, topic_id)


@router.get("/topics/{topic_id}", response_model=TopicDetail)
def get_topic_detail(topic_id: int, db: Session = Depends(get_db)) -> TopicDetail:
    topic = learning_service.get_topic(db, topic_id)
    if topic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    return topic


@router.post("/students/{student_id}/topics/{topic_id}", response_model=TopicProgress)
def select_topic(student_id: int, topic_id: int, db: Session = Depends(get_db)) -> TopicProgress:
    """
    The API-level equivalent of "student selects a topic": confirms
    the student exists, confirms the topic exists, records this as a
    LearningSession, and hands back the topic detail - including,
    per lesson, whether this specific student has already completed
    it - the frontend needs to move on to the AI teaching session
    screen.

    This is POST, not GET, specifically because it now has a real
    side effect (a new session row every time it's called). GET is
    supposed to be safe/idempotent - no state changes - and a page
    refresh or prefetch firing a GET with a write behind it would
    silently spam the session log. If your frontend was already
    calling this as GET, that call needs to change to POST.
    """
    student = learning_service.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    topic = learning_service.get_topic(db, topic_id)
    if topic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")

    session_service.record_session(
        db, student_id=student_id, subject_id=topic.subject_id, topic_id=topic.id
    )

    completed_ids = session_service.get_completed_lesson_ids(
        db, student_id, [lesson.id for lesson in topic.lessons]
    )
    lessons_progress = [
        LessonProgress(
            id=lesson.id,
            title=lesson.title,
            order_index=lesson.order_index,
            completed=lesson.id in completed_ids,
        )
        for lesson in topic.lessons
    ]

    return TopicProgress(
        id=topic.id,
        subject_id=topic.subject_id,
        name=topic.name,
        description=topic.description,
        created_at=topic.created_at,
        lessons=lessons_progress,
    )


@router.post("/students/{student_id}/lessons/{lesson_id}", response_model=LessonRead)
def select_lesson(student_id: int, lesson_id: int, db: Session = Depends(get_db)) -> LessonRead:
    """
    A student opening a specific lesson within a topic. Records a
    LearningSession with lesson_id set (subject_id/topic_id derived
    from the lesson's own topic, so the caller only needs to know the
    lesson), and returns the lesson's full content. Same POST-not-GET
    reasoning as select_topic: this writes a session row.
    """
    student = learning_service.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    lesson = learning_service.get_lesson(db, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")

    session_service.record_session(
        db,
        student_id=student_id,
        subject_id=lesson.topic.subject_id,
        topic_id=lesson.topic_id,
        lesson_id=lesson.id,
    )

    return lesson


@router.post(
    "/students/{student_id}/lessons/{lesson_id}/complete",
    response_model=LessonCompletionRead,
)
def complete_lesson(
    student_id: int, lesson_id: int, db: Session = Depends(get_db)
) -> LessonCompletionRead:
    """
    Marks a lesson complete for a student. Idempotent - calling this
    again for an already-completed lesson returns the original
    completion rather than erroring or creating a duplicate (see
    session_service.mark_lesson_complete and the unique constraint on
    LessonCompletion itself).
    """
    student = learning_service.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    lesson = learning_service.get_lesson(db, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")

    return session_service.mark_lesson_complete(db, student_id=student_id, lesson_id=lesson_id)