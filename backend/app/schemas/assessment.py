
import uuid
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field


class AnswerSubmissionRequest(BaseModel):
    """
    Schema ya jibu analotuma mwanafunzi kwa swali fulani
    lililokwisha zalishwa (GeneratedQuestion).
    """

    generated_question_id: uuid.UUID = Field(
        ..., description="ID of the GeneratedQuestion being answered."
    )
    submitted_answer: Union[str, int, float] = Field(
        ..., description="The student's answer, as typed or selected."
    )
    session_id: Optional[uuid.UUID] = Field(
        None, description="Optional student session this attempt belongs to."
    )


class AssessmentResultResponse(BaseModel):
    """
    Schema ya matokeo yanayorudishwa kwa mwanafunzi/frontend baada ya
    jibu kuhakikiwa na kuhifadhiwa kama Attempt.
    """

    attempt_id: uuid.UUID
    generated_question_id: uuid.UUID
    is_correct: bool
    submitted_answer: str = Field(
        ..., description="The submitted answer, as it was stored on the Attempt."
    )
    submitted_at: datetime

    model_config = {"from_attributes": True}