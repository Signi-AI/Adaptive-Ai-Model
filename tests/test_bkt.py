"""Unit tests for the BKT engine (pure math, no database needed)."""
import pytest

from app.adaptive.bkt_engine import (
    MAX_MASTERY,
    MIN_MASTERY,
    BKTParams,
    apply_transition,
    initial_mastery,
    posterior_correct,
    posterior_incorrect,
    update_mastery,
)

# Fixed params so expected values can be checked by hand
PARAMS = BKTParams(p_l0=0.3, p_t=0.1, p_g=0.2, p_s=0.1)
GRID = [0.0, 0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99, 1.0]


def test_initial_mastery_is_p_l0():
    assert initial_mastery(PARAMS) == 0.3


# Hand check: 0.3*0.9=0.27; 0.27 + 0.7*0.2 = 0.41
def test_posterior_correct_formula():
    assert posterior_correct(0.3, PARAMS) == pytest.approx(0.27 / 0.41)


# Hand check: 0.3*0.1=0.03; 0.03 + 0.7*0.8 = 0.59
def test_posterior_incorrect_formula():
    assert posterior_incorrect(0.3, PARAMS) == pytest.approx(0.03 / 0.59)


def test_transition_formula():
    assert apply_transition(0.5, PARAMS) == pytest.approx(0.55)


def test_correct_answer_updates_mastery():
    result = update_mastery(0.3, True, PARAMS)
    assert result.previous == 0.3
    assert result.posterior == pytest.approx(0.658537, abs=1e-6)
    assert result.new == pytest.approx(0.692683, abs=1e-6)
    assert result.correct is True


def test_incorrect_answer_updates_mastery():
    result = update_mastery(0.3, False, PARAMS)
    assert result.previous == 0.3
    assert result.posterior == pytest.approx(0.050847, abs=1e-6)
    assert result.new == pytest.approx(0.145763, abs=1e-6)
    assert result.correct is False


@pytest.mark.parametrize("prior", [g for g in GRID if 0.0 < g < 1.0])
def test_correct_always_raises_mastery(prior):
    assert update_mastery(prior, True, PARAMS).new > prior


@pytest.mark.parametrize("prior", [g for g in GRID if 0.0 < g < 1.0])
def test_incorrect_always_lowers_posterior(prior):
    assert update_mastery(prior, False, PARAMS).posterior < prior


@pytest.mark.parametrize("prior", [0.5, 0.7, 0.9])
def test_incorrect_lowers_mastery_at_moderate_to_high_prior(prior):
    assert update_mastery(prior, False, PARAMS).new < prior


# Known BKT behaviour: the learning step can outweigh a wrong answer at very low mastery
def test_incorrect_can_raise_mastery_at_very_low_prior():
    assert update_mastery(0.1, False, PARAMS).new > 0.1


@pytest.mark.parametrize("prior", GRID)
@pytest.mark.parametrize("correct", [True, False])
def test_mastery_stays_in_bounds(prior, correct):
    result = update_mastery(prior, correct, PARAMS)
    assert 0.0 <= result.posterior <= 1.0
    assert 0.0 <= result.new <= 1.0
    assert MIN_MASTERY <= result.new <= MAX_MASTERY


# Without clamping, mastery would hit exactly 1.0 and never drop again
def test_long_correct_streak_stays_below_one_and_can_still_drop():
    mastery = 0.3
    for _ in range(200):
        mastery = update_mastery(mastery, True, PARAMS).new
    assert mastery <= MAX_MASTERY < 1.0
    assert update_mastery(mastery, False, PARAMS).new < mastery


def test_long_incorrect_streak_stays_above_zero_and_can_still_rise():
    mastery = 0.3
    for _ in range(200):
        mastery = update_mastery(mastery, False, PARAMS).new
    assert mastery >= MIN_MASTERY > 0.0
    assert update_mastery(mastery, True, PARAMS).new > mastery


def test_sequence_correct_correct_incorrect():
    m1 = update_mastery(0.3, True, PARAMS)
    m2 = update_mastery(m1.new, True, PARAMS)
    m3 = update_mastery(m2.new, False, PARAMS)
    assert m1.new == pytest.approx(0.692683, abs=1e-6)
    assert m2.new == pytest.approx(0.919231, abs=1e-6)
    assert m3.new == pytest.approx(0.628501, abs=1e-6)
    assert m3.previous == m2.new


# Correct answer is impossible here (prior 0, no guessing): must not divide by zero
def test_zero_denominator_does_not_crash():
    params = BKTParams(p_l0=0.3, p_t=0.1, p_g=0.0, p_s=0.1)
    result = update_mastery(0.0, True, params)
    assert 0.0 <= result.new <= 1.0


def test_result_exposes_previous_and_new():
    result = update_mastery(0.42, True, PARAMS)
    assert result.previous == 0.42
    assert result.new != result.previous


@pytest.mark.parametrize("prior", [-0.1, 1.1])
def test_invalid_prior_raises(prior):
    with pytest.raises(ValueError):
        update_mastery(prior, True, PARAMS)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"p_l0": 1.5},
        {"p_t": -0.1},
        {"p_g": 2.0},
        {"p_s": -1.0},
        {"p_g": 0.6, "p_s": 0.5},
    ],
)
def test_invalid_params_raise(kwargs):
    with pytest.raises(ValueError):
        BKTParams(**kwargs)