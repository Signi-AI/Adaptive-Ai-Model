"""
api/routes/learning.py
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.learning import LessonRead, SubjectRead, TopicRead
from app.services import learning_service

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
