from prompt_builder import PromptBuilder


def get_test_data():
    """Return sample student data for validation."""

    return {
        "student_question": (
            "What is the difference between supervised and "
            "unsupervised learning?"
        ),
        "student_level": "Beginner",
        "student_weakness": (
            "The student struggles to distinguish supervised learning "
            "from unsupervised learning."
        ),
        "retrieved_content": (
            "Supervised learning uses labeled training data. "
            "Unsupervised learning works with data without labeled "
            "target values."
        ),
    }


def build_test_prompt():
    """Build a prompt using the standard test data."""

    builder = PromptBuilder()
    data = get_test_data()

    return builder.build_prompt(**data)


def test_student_context():
    """Verify that student context is included."""

    data = get_test_data()
    prompt = build_test_prompt()

    assert data["student_question"] in prompt
    assert data["student_level"] in prompt
    assert data["student_weakness"] in prompt

    print("[PASS] Student context is included")


def test_retrieved_content():
    """Verify that retrieved content is included."""

    data = get_test_data()
    prompt = build_test_prompt()

    assert data["retrieved_content"] in prompt
    assert "RETRIEVED EDUCATIONAL CONTENT" in prompt

    print("[PASS] Retrieved content is included")


def test_artificial_teacher_behavior():
    """Verify that the prompt defines teacher behavior."""

    prompt = build_test_prompt().lower()

    assert "artificial teacher" in prompt
    assert "explain concepts clearly" in prompt
    assert "ask guiding questions" in prompt
    assert "give hints" in prompt

    print("[PASS] Teaching behavior is defined")


def test_student_level_adaptation():
    """Verify that the prompt considers student level."""

    data = get_test_data()
    prompt = build_test_prompt().lower()

    assert "learning level" in prompt
    assert data["student_level"].lower() in prompt
    assert "student's level" in prompt

    print("[PASS] Student level adaptation is defined")


def test_student_weakness_adaptation():
    """Verify that the prompt considers student weakness."""

    data = get_test_data()
    prompt = build_test_prompt().lower()

    assert "known weakness" in prompt
    assert data["student_weakness"].lower() in prompt
    assert "weakness" in prompt

    print("[PASS] Student weakness adaptation is defined")


def test_hint_behavior():
    """Verify that the prompt supports hints."""

    prompt = build_test_prompt().lower()

    assert "give hints" in prompt
    assert "hint" in prompt

    print("[PASS] Hint behavior is defined")


def test_guiding_question_behavior():
    """Verify that the prompt supports guiding questions."""

    prompt = build_test_prompt().lower()

    assert "ask guiding questions" in prompt
    assert "guiding question" in prompt

    print("[PASS] Guiding-question behavior is defined")


def test_prevents_immediate_answers():
    """Verify that unnecessary immediate answers are discouraged."""

    prompt = build_test_prompt().lower()

    assert "do not immediately reveal the final answer" in prompt
    assert "guidance" in prompt
    assert "guide" in prompt
    assert "answer" in prompt

    print("[PASS] Immediate-answer prevention is defined")


def test_final_answer_is_controlled():
    """
    Verify that the prompt does not completely forbid final answers.

    The teacher should guide the student first but may provide an answer
    when appropriate.
    """

    prompt = build_test_prompt().lower()

    assert "if the student explicitly needs the final answer" in prompt
    assert "provide it" in prompt
    assert "explanation" in prompt

    print("[PASS] Controlled final-answer behavior is defined")


def test_retrieved_content_is_primary_source():
    """Verify that retrieved content is used as the primary source."""

    prompt = build_test_prompt().lower()

    assert "retrieved educational content" in prompt
    assert "primary knowledge source" in prompt

    print("[PASS] Retrieved content usage is defined")


def test_empty_student_question_is_rejected():
    """Verify that an empty question is rejected."""

    builder = PromptBuilder()
    data = get_test_data()
    data["student_question"] = ""

    try:
        builder.build_prompt(**data)
    except ValueError:
        print("[PASS] Empty student question is rejected")
        return

    raise AssertionError(
        "Empty student question should raise ValueError"
    )


def test_empty_student_level_is_rejected():
    """Verify that an empty student level is rejected."""

    builder = PromptBuilder()
    data = get_test_data()
    data["student_level"] = ""

    try:
        builder.build_prompt(**data)
    except ValueError:
        print("[PASS] Empty student level is rejected")
        return

    raise AssertionError(
        "Empty student level should raise ValueError"
    )


def test_empty_student_weakness_is_rejected():
    """Verify that an empty student weakness is rejected."""

    builder = PromptBuilder()
    data = get_test_data()
    data["student_weakness"] = ""

    try:
        builder.build_prompt(**data)
    except ValueError:
        print("[PASS] Empty student weakness is rejected")
        return

    raise AssertionError(
        "Empty student weakness should raise ValueError"
    )


def test_empty_retrieved_content_is_rejected():
    """Verify that empty retrieved content is rejected."""

    builder = PromptBuilder()
    data = get_test_data()
    data["retrieved_content"] = ""

    try:
        builder.build_prompt(**data)
    except ValueError:
        print("[PASS] Empty retrieved content is rejected")
        return

    raise AssertionError(
        "Empty retrieved content should raise ValueError"
    )


def run_all_tests():
    """Run all Socratic Artificial Teacher validation tests."""

    print("=" * 70)
    print("SOCRATIC ARTIFICIAL TEACHER - PROMPT VALIDATION")
    print("=" * 70)

    test_student_context()
    test_retrieved_content()
    test_artificial_teacher_behavior()
    test_student_level_adaptation()
    test_student_weakness_adaptation()
    test_hint_behavior()
    test_guiding_question_behavior()
    test_prevents_immediate_answers()
    test_final_answer_is_controlled()
    test_retrieved_content_is_primary_source()

    test_empty_student_question_is_rejected()
    test_empty_student_level_is_rejected()
    test_empty_student_weakness_is_rejected()
    test_empty_retrieved_content_is_rejected()

    print()
    print("=" * 70)
    print("ALL SOCRATIC TEACHER TESTS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()