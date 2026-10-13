import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class GeneratedQuestion(Base):
    """A concrete question generated from a reusable question template."""

    __tablename__ = "generated_questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_id = Column(
        UUID(as_uuid=True),
        ForeignKey("question_templates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    subject_id = Column(
        UUID(as_uuid=True),
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    topic_id = Column(
        UUID(as_uuid=True),
        ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    lesson_id = Column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    learning_objective_id = Column(
        UUID(as_uuid=True),
        ForeignKey("learning_objectives.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user_sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    generated_text = Column(String, nullable=False)
    parameters = Column(JSON, nullable=False, default=dict)
    correct_answer = Column(JSON, nullable=False)
    random_seed = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    template = relationship("QuestionTemplate", back_populates="generated_questions")
    subject = relationship("Subject")
    topic = relationship("Topic")
    lesson = relationship("Lesson")
    learning_objective = relationship("LearningObjective")

    def __repr__(self) -> str:
        return f"<GeneratedQuestion id={self.id} template_id={self.template_id}>"
