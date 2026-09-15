
from unittest.mock import Base
import uuid

from sqlalchemy import Column, String, ForeignKey, Integer, JSON, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class GeneratedQuestion(Base):

    __tablename__ = "generated_questions"

    # Kitambulisho cha kipekee cha swali hili lililozalishwa
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
        )

    # Uhusiano na template iliyozalisha swali hili — LAZIMA iwepo,
    # kwa sababu kila swali lililozalishwa linatoka kwenye template.
    template_id = Column(
        UUID(as_uuid=True),
        ForeignKey("question_templates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Uhusiano na kipindi cha mwanafunzi aliyepokea swali 
    # ondelete="SET NULL": session ikifutwa, swali lililozalishwa
    # LIBAKI (kwa ajili ya historia/audit), tu kiungo chake kiondolewe.
    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("student_sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Maandishi kamili ya swali baada ya kujazwa thamani halisi
    generated_text = Column(
        String, 
        nullable=False
        )

    # Thamani halisi za parameta zilizotumika kuzalisha swali hili
    parameters = Column(
        JSON, 
        nullable=False, 
        default=dict
        )

    # Jibu sahihi lililohesabiwa wakati wa kuzalisha swali hili
    correct_answer = Column(
        JSON, 
        nullable=False
        )


    # upya matokeo yaleyale endapo itahitajika kwa ajili ya ukaguzi
    random_seed = Column(
        Integer, 
        nullable=True
        )

    # Muda swali hili lilipozalishwa na kuhifadhiwa — database
    # yenyewe ndiyo inayoweka wakati huu kiotomatiki
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now()
        )

    # Uhusiano na QuestionTemplate
    template = relationship("QuestionTemplate", back_populates="generated_questions")

    def __repr__(self) -> str:  
        return (
            f"<GeneratedQuestion id={self.id} template_id={self.template_id} "
            f"session_id={self.session_id}>"
        )