from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("generated_questions.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False, index=True)

    is_correct = Column(Boolean, nullable=False)
    response_time_seconds = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # auto-set by DB

    student = relationship("Student", back_populates="attempts")
    topic = relationship("Topic", back_populates="attempts")
    question = relationship("GeneratedQuestion")