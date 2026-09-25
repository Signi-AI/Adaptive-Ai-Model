
import ast
import operator
import uuid
from typing import Any, Callable, Dict, Optional

from sqlalchemy.orm import Session

from app.models.generated_question import GeneratedQuestion
from app.models.question_template import QuestionTemplate
from app.questions.difficulty_validator import DifficultyValidator, InvalidQuestionError
from app.questions.parameter_engine import ParameterEngine, ParameterGenerationError
from app.utils.seed_utils import generate_seed, get_rng


class QuestionGenerationError(Exception):
    """Inatolewa pale swali halali haliwezi kuzalishwa kutoka kwa template."""


_ALLOWED_BINARY_OPERATORS: Dict[type, Callable[[Any, Any], Any]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_ALLOWED_UNARY_OPERATORS: Dict[type, Callable[[Any], Any]] = {
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def evaluate_expression(expression: str, variables: Dict[str, Any]) -> Any:
    """
    Huhesabu fomula rahisi ya kihesabu (mfano "x + y", "x * y - 2")
    kwa kutumia TU `variables` zilizotolewa, bila kuruhusu function
    calls, attribute access, imports, au code nyingine yoyote hatari.
    """
    try:
        parsed = ast.parse(expression, mode="eval").body
    except SyntaxError as exc:
        raise QuestionGenerationError(
            f"answer_rule.expression '{expression}' is not a valid math expression: {exc}"
        ) from exc
    return _eval_node(parsed, variables)


def _eval_node(node: ast.AST, variables: Dict[str, Any]) -> Any:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise QuestionGenerationError(f"Disallowed value in expression: {node.value!r}")

    if isinstance(node, ast.Name):
        if node.id not in variables:
            raise QuestionGenerationError(
                f"Name '{node.id}' is not among the generated parameters: "
                f"{sorted(variables.keys())}"
            )
        return variables[node.id]

    if isinstance(node, ast.BinOp):
        op_func = _ALLOWED_BINARY_OPERATORS.get(type(node.op))
        if op_func is None:
            raise QuestionGenerationError(
                f"Operator '{type(node.op).__name__}' is not allowed in expressions."
            )
        left = _eval_node(node.left, variables)
        right = _eval_node(node.right, variables)
        try:
            return op_func(left, right)
        except ArithmeticError as exc:
            
            
            # Mfano: kugawanya kwa sifuri. Vigezo vya awali vya
            # ParameterEngine (not_zero/exclude) vinapaswa kuzuia hili
            # kabla — hii ni "safety net" ya mwisho isije ikasababisha
            # crash isiyodhibitiwa.
            raise QuestionGenerationError(
                f"Arithmetic error while evaluating answer_rule.expression: {exc}"
            ) from exc

    if isinstance(node, ast.UnaryOp):
        op_func = _ALLOWED_UNARY_OPERATORS.get(type(node.op))
        if op_func is None:
            raise QuestionGenerationError(
                f"Unary operator '{type(node.op).__name__}' is not allowed."
            )
        return op_func(_eval_node(node.operand, variables))

    raise QuestionGenerationError(
        f"Element '{type(node).__name__}' is not allowed in answer_rule.expression."
    )



class QuestionGenerator:
    """Huratibu uzalishaji wa swali moja HALISI kutoka kwa template, na kuihifadhi."""

    def __init__(self, db: Session):
        self.db = db
        self._parameter_engine = ParameterEngine()
        self._difficulty_validator = DifficultyValidator()

    def generate(
        self,
        template: QuestionTemplate,
        seed: Optional[int] = None,
        session_id: Optional[uuid.UUID] = None,
    ) -> GeneratedQuestion:
        """
        Huzalisha swali MOJA kutoka kwa `template` na kuliHIFADHI
        database-ni kabla ya kulirudisha.

        `seed`: ukipitisha seed maalum, matokeo yatakuwa YALE YALE
            kila wakati (deterministic) — muhimu kwa debugging na
            kwa kuhakiki jibu baadaye bila kuzalisha upya.
            Ukiacha None, seed mpya isiyotabirika itazalishwa.
        `session_id`: hiari — kuunganisha swali hili na kipindi cha
            mwanafunzi, kama kinapatikana.
        """
        resolved_seed = seed if seed is not None else generate_seed()
        rng = get_rng(resolved_seed)

        try:
            parameters = self._parameter_engine.generate_parameters(
                template.parameter_definitions, rng
            )
        except ParameterGenerationError as exc:
            raise QuestionGenerationError(str(exc)) from exc

        correct_answer = self._compute_answer(template.answer_rule, parameters)

        difficulty_value = getattr(template.difficulty, "value", template.difficulty)
        try:
            self._difficulty_validator.validate(
                parameters=parameters,
                correct_answer=correct_answer,
                difficulty=str(difficulty_value),
                answer_rule=template.answer_rule,
            )
        except InvalidQuestionError as exc:
            raise QuestionGenerationError(str(exc)) from exc

        generated_text = self._render_text(template.template_text, parameters)

        generated_question = GeneratedQuestion(
            template_id=template.id,
            session_id=session_id,
            generated_text=generated_text,
            parameters=parameters,
            correct_answer=correct_answer,
            random_seed=resolved_seed,
        )

        self.db.add(generated_question)
        self.db.commit()
        self.db.refresh(generated_question)
        return generated_question

    def generate_many(
        self,
        template: QuestionTemplate,
        count: int,
        session_id: Optional[uuid.UUID] = None,
    ) -> list:
        """
        Huzalisha `count` ya matoleo (versions) TOFAUTI ya swali kutoka
        template ile ile moja — kila moja likiwa na seed yake yenyewe
        isiyotabirika. Hii ndiyo inayothibitisha kigezo cha ukubalifu:
        "One template produces multiple versions."
        """
        return [self.generate(template, session_id=session_id) for _ in range(count)]

    # ---- Sehemu za ndani (internal helpers) ------------------------

    @staticmethod
    def _compute_answer(answer_rule: Dict[str, Any], parameters: Dict[str, Any]) -> Any:
        expression = (answer_rule or {}).get("expression")
        if not expression:
            raise QuestionGenerationError("answer_rule is missing the required 'expression'.")
        return evaluate_expression(expression, parameters)

    @staticmethod
    def _render_text(template_text: str, parameters: Dict[str, Any]) -> str:
        try:
            return template_text.format(**parameters)
        except (KeyError, IndexError) as exc:
            raise QuestionGenerationError(
                f"template_text references a placeholder that is not among the generated "
                f"parameters: {exc}"
            ) from exc