"""Bayesian Knowledge Tracing (BKT) engine.

Pure math only: no database, no API, no framework imports.
Mastery = probability (0-1) that a student knows a topic.
"""
from dataclasses import dataclass

# Keep mastery off exactly 0/1, otherwise it can get stuck there forever
MIN_MASTERY = 1e-4
MAX_MASTERY = 1.0 - 1e-4


@dataclass(frozen=True)
class BKTParams:
    p_l0: float = 0.3  # P(L0): chance the student already knew the topic
    p_t: float = 0.1   # P(T): chance of learning it after one attempt
    p_g: float = 0.2   # P(G): guess - answers correctly without knowing
    p_s: float = 0.1   # P(S): slip - answers wrongly despite knowing

    def __post_init__(self):
        for name in ("p_l0", "p_t", "p_g", "p_s"):
            value = getattr(self, name)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1, got {value}")
        # If guess + slip >= 1, a correct answer would not raise mastery
        if self.p_g + self.p_s >= 1.0:
            raise ValueError("p_g + p_s must be less than 1")


@dataclass(frozen=True)
class BKTResult:
    previous: float   # mastery before this answer
    posterior: float  # mastery after seeing the answer, before learning
    new: float        # final mastery to store (posterior + learning step)
    correct: bool


DEFAULT_PARAMS = BKTParams()


def clamp(value: float) -> float:
    return max(MIN_MASTERY, min(MAX_MASTERY, value))


def initial_mastery(params: BKTParams = DEFAULT_PARAMS) -> float:
    # Starting mastery for a student with no attempts on a topic
    return params.p_l0


def posterior_correct(prior: float, params: BKTParams = DEFAULT_PARAMS) -> float:
    # P(L|correct) = L(1-S) / [L(1-S) + (1-L)G]
    numerator = prior * (1.0 - params.p_s)
    denominator = numerator + (1.0 - prior) * params.p_g
    # Zero only when a correct answer is impossible; keep prior unchanged
    return numerator / denominator if denominator > 0.0 else prior


def posterior_incorrect(prior: float, params: BKTParams = DEFAULT_PARAMS) -> float:
    # P(L|incorrect) = L*S / [L*S + (1-L)(1-G)]
    numerator = prior * params.p_s
    denominator = numerator + (1.0 - prior) * (1.0 - params.p_g)
    return numerator / denominator if denominator > 0.0 else prior


def apply_transition(posterior: float, params: BKTParams = DEFAULT_PARAMS) -> float:
    # Chance the student learned the topic during this attempt:
    # L_next = P(L|answer) + (1 - P(L|answer)) * T
    return posterior + (1.0 - posterior) * params.p_t


def update_mastery(
    prior: float, correct: bool, params: BKTParams = DEFAULT_PARAMS
) -> BKTResult:
    """Return previous, posterior and new mastery for one answer."""
    if not 0.0 <= prior <= 1.0:
        raise ValueError(f"prior must be between 0 and 1, got {prior}")

    correct = bool(correct)
    if correct:
        posterior = posterior_correct(prior, params)
    else:
        posterior = posterior_incorrect(prior, params)

    new = apply_transition(posterior, params)
    return BKTResult(
        previous=prior,
        posterior=clamp(posterior),
        new=clamp(new),
        correct=correct,
    )