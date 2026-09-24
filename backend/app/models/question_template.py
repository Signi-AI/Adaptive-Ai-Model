
import enum
import uuid

from sqlalchemy import Column, String, ForeignKey, Enum, JSON, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class DifficultyLevel(str, enum.Enum):
    """Viwango vinavyokubalika vya ugumu wa template ya swali."""

    EASY = "easy"      # rahisi
    MEDIUM = "medium"   # wastani
    HARD = "hard"       # ngumu


class QuestionTemplate(Base):

    __tablename__ = "question_templates"

    # Kitambulisho cha kipekee (UUID) cha template
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
        )



    # Uhusiano na Topic — kila template LAZIMA iwe ya topic fulani.
    # ondelete="CASCADE": template ikifutwa moja kwa moja database
    # haiathiri Topic (ni upande wa "child" tu).
    topic_id = Column(
        UUID(as_uuid=True),
        ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


    # Kiwango cha ugumu wa template hii (EASY/MEDIUM/HARD)
    difficulty = Column(
        Enum(DifficultyLevel, name="difficulty_level"),
        nullable=False,
        index=True,
    )

    # Maandishi ya swali yenye placeholders, mfano "{x} + {y} = ?"
    template_text = Column(
        String, 
        nullable=False
        )


    # Ufafanuzi wa kila parameta/placeholder iliyoko kwenye template_text
    parameter_definitions = Column(
        JSON,
        nullable=False,
        default=dict
        )

    # Kanuni ya kuhesabu jibu sahihi kutoka kwa parameta
    answer_rule = Column(
        JSON, 
        nullable=False
        , default=dict
        )


    # Muda template ilipoundwa — database yenyewe ndiyo inaweka wakati
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
        )


    # Muda template ilipobadilishwa mara ya mwisho — database
    # inaisasisha kiotomatiki kila UPDATE inapotokea
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )



    # Uhusiano na Topic (upande "mmoja" wa one-to-many).
    topic = relationship(
        "Topic", 
        back_populates="question_templates"
    )

    generated_questions = relationship(
        "GeneratedQuestion", back_populates="template", cascade="all, delete-orphan"
        )



    def __repr__(self) -> str: 
        # Muonekano rahisi wa object hii wakati wa debugging/logging
        return (
            f"<QuestionTemplate id={self.id} topic_id={self.topic_id} "
            f"difficulty={self.difficulty}>"
        )