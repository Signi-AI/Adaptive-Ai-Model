from teaching_prompt import TeachingPrompt


class PromptBuilder:
    """Build prompts for the Socratic Artificial Teacher."""

    def __init__(self):
        self.teaching_prompt = TeachingPrompt()

    def build_prompt(
        self,
        student_question: str,
        student_level: str,
        student_weakness: str,
        retrieved_content: str,
    ) -> str:
        """
        Build an Artificial Teacher prompt.

        Args:
            student_question: The student's question.
            student_level: The student's learning level.
            student_weakness: The student's known weakness.
            retrieved_content: Relevant retrieved educational content.

        Returns:
            A complete teaching prompt ready to be passed to Gemma.
        """

        return self.teaching_prompt.build(
            student_question=student_question,
            student_level=student_level,
            student_weakness=student_weakness,
            retrieved_content=retrieved_content,
        )