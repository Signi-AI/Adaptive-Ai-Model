
import math
from typing import Any, Dict

# Kiwango cha juu cha ukubwa (magnitude) kinachotarajiwa kwa kila
# kiwango cha ugumu — hii ni ukaguzi wa jumla tu (sanity bound),
# si sheria kali ya kihisabati.
_DIFFICULTY_MAGNITUDE_BOUNDS = {
    "easy": 20,
    "medium": 200,
    "hard": 10_000,
}

# Jibu sahihi linaruhusiwa kuwa kubwa zaidi ya parameta zenyewe
# (mfano kuzidisha kunaweza kutoa jibu kubwa kuliko x na y wote),
# kwa hiyo tunatumia kipimo tofauti, kikubwa zaidi, kwa jibu.
_ANSWER_MAGNITUDE_MULTIPLIER = 50


class InvalidQuestionError(Exception):
    """Inatolewa pale swali lililozalishwa halikubaliki kihisabati au kiugumu."""


class DifficultyValidator(object):
    """Huhakiki kuwa parameta na jibu vinakubalika kwa ugumu na hisabati sahihi."""

    def validate(
        self,
        parameters: Dict[str, Any],
        correct_answer: Any,
        difficulty: str,
        answer_rule: Dict[str, Any],
    ) -> None:
        """
        Hutupa `InvalidQuestionError` endapo swali lililozalishwa
        halikubaliki. Hurudisha None (hakuna return value) ikiwa
        kila kitu ni sahihi.
        """
        self._validate_finite(parameters, correct_answer)
        self._validate_magnitude(parameters, correct_answer, difficulty)
        self._validate_division_safety(parameters, answer_rule)


    @staticmethod
    def _is_non_finite_number(value: Any) -> bool:
        return isinstance(value, float) and not math.isfinite(value)

    def _validate_finite(self, parameters: Dict[str, Any], correct_answer: Any) -> None:
        """Hakikisha hakuna NaN au infinity popote (matokeo ya 0/0, n.k.)."""
        for name, value in parameters.items():
            if self._is_non_finite_number(value):
                raise InvalidQuestionError(
                    f"Parameter '{name}' has an invalid value (NaN/infinity): {value}"
                )
        if self._is_non_finite_number(correct_answer):
            raise InvalidQuestionError(
                f"The computed correct answer is not a valid number (NaN/infinity): {correct_answer}"
            )

    def _validate_magnitude(
        self, parameters: Dict[str, Any], correct_answer: Any, difficulty: str
    ) -> None:
        """Hakikisha ukubwa wa namba unaendana na kiwango cha ugumu."""
        bound = _DIFFICULTY_MAGNITUDE_BOUNDS.get(str(difficulty).lower())
        if bound is None:
            # Kiwango cha ugumu hakitambuliki kwenye jedwali letu —
            # ruka ukaguzi huu badala ya kuzuia uzalishaji bure.
            return

        for name, value in parameters.items():
            if isinstance(value, (int, float)) and abs(value) > bound:
                raise InvalidQuestionError(
                    f"Parameter '{name}'={value} exceeds the expected magnitude for difficulty "
                    f"'{difficulty}' (limit ±{bound})."
                )

        if isinstance(correct_answer, (int, float)):
            answer_bound = bound * _ANSWER_MAGNITUDE_MULTIPLIER
            if abs(correct_answer) > answer_bound:
                raise InvalidQuestionError(
                    f"Correct answer {correct_answer} is unreasonably large for difficulty "
                    f"'{difficulty}' (limit ±{answer_bound})."
                )

    def _validate_division_safety(
        self, parameters: Dict[str, Any], answer_rule: Dict[str, Any]
    ) -> None:
        """Kama fomula ina mgawanyo (/), hakikisha hakuna sehemu ya kugawia iliyo sifuri."""
        expression = (answer_rule or {}).get("expression", "") or ""
        if "/" not in expression:
            return

        for name, value in parameters.items():
            # Ukaguzi rahisi: jina la parameta linaonekana kwenye
            # expression na thamani yake ni sifuri -> hatari ya
            # kugawanya kwa sifuri.
            if name in expression and isinstance(value, (int, float)) and value == 0:
                raise InvalidQuestionError(
                    f"Formula '{expression}' may divide by parameter '{name}', "
                    "which is zero."
                )