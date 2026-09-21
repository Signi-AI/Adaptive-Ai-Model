
import random
from typing import Any, Dict

# Idadi ya majaribio tunayoruhusu kabla ya kukata tamaa kupata
# thamani inayokidhi vikwazo (mfano: not_zero, exclude)
MAX_GENERATION_RETRIES = 50

class ParameterGenerationError(Exception):
    """Inatolewa pale parameta haiwezi kuzalishwa kihalali."""


class ParameterEngine(object):
    """Huzalisha thamani halisi za parameta kutoka kwa ufafanuzi wa template."""

    def generate_parameters(
        self, parameter_definitions: Dict[str, Dict[str, Any]], rng: random.Random
    ) -> Dict[str, Any]:
        """
        Huzalisha dict ya {jina_la_parameta: thamani_halisi} kwa
        kila placeholder iliyoainishwa kwenye template.

        `rng` lazima iwe RNG iliyowekwa seed tayari (angalia
        `seed_utils.get_rng`), ili matokeo yawe reproducible.
        """
        if not parameter_definitions:
            raise ParameterGenerationError(
                "parameter_definitions cannot be empty — the template has no placeholders."
            )

        generated: Dict[str, Any] = {}
        for name, definition in parameter_definitions.items():
            generated[name] = self._generate_single(name, definition, rng)
        return generated


    def _generate_single(
        self, name: str, definition: Dict[str, Any], rng: random.Random
    ) -> Any:
        """
        Huzalisha thamani MOJA halali kwa parameta moja, ikijaribu
        tena (retry) endapo thamani iliyopatikana inakiuka vikwazo
        vya "invalid values" (mfano exclude, not_zero).
        """
        exclude = set(definition.get("exclude", []) or [])
        if definition.get("not_zero"):
            exclude.add(0)

        for _ in range(MAX_GENERATION_RETRIES):
            candidate = self._sample(name, definition, rng)
            if candidate not in exclude:
                return candidate

        raise ParameterGenerationError(
            f"Could not generate a valid value for parameter '{name}' after "
            f"{MAX_GENERATION_RETRIES} attempts (constraints too strict: exclude={exclude}).")




    def _sample(self, name: str, definition: Dict[str, Any], rng: random.Random) -> Any:
        """Huchota thamani MOJA ya kubahatisha kulingana na 'type' ya parameta."""
        param_type = definition.get("type")

        if param_type == "int":
            return self._sample_int(name, definition, rng)
        if param_type == "float":
            return self._sample_float(name, definition, rng)
        if param_type in ("choice", "str"):
            return self._sample_choice(name, definition, rng)

        raise ParameterGenerationError(
            f"Unrecognized parameter type '{param_type}' for parameter '{name}'. "
            "Supported types: 'int', 'float', 'choice'/'str'."
        )



    @staticmethod
    def _sample_int(name: str, definition: Dict[str, Any], rng: random.Random) -> int:
        lo, hi = definition.get("min"), definition.get("max")
        if lo is None or hi is None:
            raise ParameterGenerationError(
                f"Parameter '{name}' of type 'int' requires 'min' and 'max'."
            )
        if int(lo) > int(hi):
            raise ParameterGenerationError(
                f"Parameter '{name}': min ({lo}) cannot be greater than max ({hi})."
            )
        return rng.randint(int(lo), int(hi))



    @staticmethod
    def _sample_float(name: str, definition: Dict[str, Any], rng: random.Random) -> float:
        lo, hi = definition.get("min"), definition.get("max")
        if lo is None or hi is None:
            raise ParameterGenerationError(
                f"Parameter '{name}' of type 'float' requires 'min' and 'max'."
            )
        if float(lo) > float(hi):
            raise ParameterGenerationError(
                f"Parameter '{name}': min ({lo}) cannot be greater than max ({hi})."
            )
        precision = definition.get("precision", 2)
        return round(rng.uniform(float(lo), float(hi)), int(precision))

    @staticmethod
    def _sample_choice(name: str, definition: Dict[str, Any], rng: random.Random) -> Any:
        choices = definition.get("choices")
        if not choices:
            raise ParameterGenerationError(
                f"Parameter '{name}' of type 'choice'/'str' requires a non-empty 'choices' list."
            )
        return rng.choice(choices)
    
    