
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class DifficultyLevel(str, Enum):
    """Viwango vya ugumu — vinavyolingana na enum ya kwenye model."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ParameterDefinition(BaseModel):


#Hii inaeleza TU *jinsi* thamani itakavyozalishwa baadaye —
#kuzalisha thamani halisi ni nje ya wigo wa faili hili.
    type: str = Field(..., description="Data type of the parameter, e.g. 'int', 'float', 'str'.")
    min: Optional[float] = Field(None, description="Minimum value, for numeric types.")
    max: Optional[float] = Field(None, description="Maximum value, for numeric types.")
    choices: Optional[List[Any]] = Field(None, description="Allowed discrete values, if applicable.")

    # Inaruhusu funguo za ziada zisizotambulika sasa bila kuvunja templates zilizopo
    model_config = {"extra": "allow"}


class AnswerRule(BaseModel):
    """
    Inaeleza jinsi jibu sahihi litakavyohesabiwa kutoka kwa parameta
    zitakazozalishwa. Imeachwa ya jumla kwa makusudi; kuihesabu/
    kuitekeleza ni nje ya wigo wa faili hili.
    """

    expression: str = Field(..., description="Expression evaluated against parameters, e.g. 'x + y'.")

    model_config = {"extra": "allow"}


class QuestionTemplateBase(BaseModel):
    """Sehemu za msingi zinazoshirikiwa na schema zote za template."""

    topic_id: uuid.UUID
    difficulty: DifficultyLevel
    template_text: str = Field(..., min_length=1, description="Question text with {placeholders}.")
    parameter_definitions: Dict[str, ParameterDefinition]
    answer_rule: AnswerRule

    @field_validator("template_text")
    @classmethod
    def must_contain_placeholder(cls, v: str) -> str:
    # Hakikisha template ina angalau placeholder moja — bila hiyo
    # si "template" tena bali ni swali tuli (static) tena
        if "{" not in v or "}" not in v:
            raise ValueError("template_text must contain at least one {placeholder}.")
        return v


class QuestionTemplateCreate(QuestionTemplateBase):
    
    #Schema inayotumika wakati wa kuunda template mpya.

    pass


class QuestionTemplateUpdate(BaseModel):
    
    #Schema inayotumika wakati wa kubadilisha template iliyopo.
    #Sehemu zote ni hiari (optional) — unaweza kubadilisha sehemu
    #moja tu bila kulazimika kutuma sehemu zingine zote.
    

    difficulty: Optional[DifficultyLevel] = None
    template_text: Optional[str] = None
    parameter_definitions: Optional[Dict[str, ParameterDefinition]] = None
    answer_rule: Optional[AnswerRule] = None


class QuestionTemplateOut(QuestionTemplateBase):
    """Schema inayorudishwa kwa mtumiaji/API baada ya kusoma template."""

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    # Inaruhusu kuunda schema hii moja kwa moja kutoka kwa SQLAlchemy object
    model_config = {"from_attributes": True}