

import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.question_template import QuestionTemplate, DifficultyLevel
from app.schemas.question import QuestionTemplateCreate, QuestionTemplateUpdate


class QuestionTemplateService:
    """Tabaka la huduma (service layer) kwa ajili ya QuestionTemplate."""

    def __init__(self, db: Session):
        self.db = db


    def create_template(self, data: QuestionTemplateCreate) -> QuestionTemplate:
        """Huunda template mpya ya swali database-ni na kuirudisha."""
        template = QuestionTemplate(
            topic_id=data.topic_id,
            difficulty=data.difficulty,
            template_text=data.template_text,
            # Geuza kila ParameterDefinition (Pydantic) kuwa dict rahisi
            # kabla ya kuhifadhi kwenye column ya JSON
            parameter_definitions={
                key: value.model_dump() for key, value in data.parameter_definitions.items()
            },
            answer_rule=data.answer_rule.model_dump(),
        )
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template

    def get_template(self, template_id: uuid.UUID) -> Optional[QuestionTemplate]:
        """Hutafuta template moja kwa ID yake. Hurudisha None kama haipo."""
        return (
            self.db.query(QuestionTemplate)
            .filter(QuestionTemplate.id == template_id)
            .first()
        )

    def get_templates_by_topic(
        self, topic_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[QuestionTemplate]:
        """Hurudisha templates zote za topic fulani."""
        return (
            self.db.query(QuestionTemplate)
            .filter(QuestionTemplate.topic_id == topic_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


    def get_templates_by_difficulty(
        self, difficulty: DifficultyLevel, skip: int = 0, limit: int = 100
    ) -> List[QuestionTemplate]:
        """Hurudisha templates zote zenye kiwango fulani cha ugumu."""
        return (
            self.db.query(QuestionTemplate)
            .filter(QuestionTemplate.difficulty == difficulty)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_templates_by_topic_and_difficulty(
        self,
        topic_id: uuid.UUID,
        difficulty: DifficultyLevel,
        skip: int = 0,
        limit: int = 100,
    ) -> List[QuestionTemplate]:
        """Hurudisha templates zinazolingana na topic NA ugumu wote wawili."""
        return (
            self.db.query(QuestionTemplate)
            .filter(
                QuestionTemplate.topic_id == topic_id,
                QuestionTemplate.difficulty == difficulty,
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


    def list_templates(self, skip: int = 0, limit: int = 100) -> List[QuestionTemplate]:
        """Hurudisha templates zote (bila kuchuja), na uwezo wa kupagina (pagination)."""
        return self.db.query(QuestionTemplate).offset(skip).limit(limit).all()



    def update_template(
        self, template_id: uuid.UUID, data: QuestionTemplateUpdate
    ) -> Optional[QuestionTemplate]:
        """Hubadilisha template iliyopo. Hurudisha None kama haipo."""
        template = self.get_template(template_id)
        if template is None:
            return None



        # exclude_unset=True: tunachukua TU sehemu ambazo mtumiaji
        # ametuma kwa makusudi, si zote (kwa sababu Update ni ya hiari)
        update_data = data.model_dump(exclude_unset=True)


        # Geuza nested Pydantic objects kuwa dict kabla ya kuhifadhi
        if update_data.get("parameter_definitions") is not None:
            update_data["parameter_definitions"] = {
                key: (val.model_dump() if hasattr(val, "model_dump") else val)
                for key, val in update_data["parameter_definitions"].items()
            }


        if update_data.get("answer_rule") is not None:
            rule = update_data["answer_rule"]
            update_data["answer_rule"] = rule.model_dump() if hasattr(rule, "model_dump") else rule

        # Weka kila thamani mpya kwenye object ya template
        for field, value in update_data.items():
            setattr(template, field, value)

        self.db.commit()
        self.db.refresh(template)
        return template



    def delete_template(self, template_id: uuid.UUID) -> bool:
        """Hufuta template. Hurudisha True ikifanikiwa, False kama haipo."""
        template = self.get_template(template_id)
        if template is None:
            return False
        self.db.delete(template)
        self.db.commit()
        return True