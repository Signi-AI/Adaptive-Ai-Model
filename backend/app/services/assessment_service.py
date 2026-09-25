
import uuid
from typing import Any, Optional

from sqlalchemy.orm import Session

from app.models.attempt import Attempt
from app.models.generated_question import GeneratedQuestion
from app.questions.answer_engine import AnswerEngine, AnswerValidationError


class AssessmentError(Exception):
    """Inatolewa pale jaribio la kuhakiki jibu halikuweza kukamilika (data batili au haipo)."""


class AssessmentService(object):
    """Huratibu uhakiki wa jibu la mwanafunzi na uhifadhi wa Attempt inayotokana nalo."""

    def __init__(self, db: Session):
        self.db = db
        self._answer_engine = AnswerEngine()

    def submit_answer(
        self,
        generated_question_id: uuid.UUID,
        submitted_answer: Any,
        session_id: Optional[uuid.UUID] = None,
    ) -> Attempt:
        """Huhakiki jibu la mwanafunzi na kuhifadhi Attempt inayotokana nalo."""
        generated_question = self._get_generated_question(generated_question_id)

        try:
            result = self._answer_engine.evaluate(
                correct_answer=generated_question.correct_answer,
                submitted_answer=submitted_answer,
            )
        except AnswerValidationError as exc:
            raise AssessmentError(f"Invalid submission: {exc}") from exc

        attempt = Attempt(
            generated_question_id=generated_question.id,
            session_id=session_id,
            submitted_answer=str(submitted_answer),
            is_correct=result.is_correct,
        )
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)
        return attempt


    def _get_generated_question(self, generated_question_id: uuid.UUID) -> GeneratedQuestion:
        """Husoma GeneratedQuestion iliyohifadhiwa — HAIZALISHI mpya."""
        generated_question = (
            self.db.query(GeneratedQuestion)
            .filter(GeneratedQuestion.id == generated_question_id)
            .first()
        )
        if generated_question is None:
            raise AssessmentError(
                f"GeneratedQuestion with id '{generated_question_id}' was not found."
            )
        return generated_question