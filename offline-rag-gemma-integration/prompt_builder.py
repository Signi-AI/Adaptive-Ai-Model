class PromptBuilder:
    """
    Build grounded teaching prompts for the local Gemma model.

    The retrieved educational content is treated as the primary
    knowledge source for the response.
    """

    SYSTEM_INSTRUCTIONS = """
You are an Artificial Teacher helping a student learn.

Your responsibilities:
- Explain concepts clearly and step by step.
- Use the retrieved educational content as your primary source.
- Keep the explanation appropriate for the student's level.
- Ask guiding questions when they help the student reason.
- Give hints before immediately giving a final answer when appropriate.
- Correct misunderstandings clearly.
- Do not invent facts that are not supported by the retrieved content.
- If the retrieved content does not contain enough information, say so
  instead of pretending that the information was retrieved.
- Focus on teaching and understanding, not just producing an answer.

Important grounding rule:
Use the retrieved educational content below as the main source for
your answer.
"""

    def build(
        self,
        question: str,
        retrieved_content: list[dict],
        student_level: str = "beginner",
    ) -> str:
        """
        Build a grounded prompt from the student's question
        and retrieved educational content.
        """

        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        if not retrieved_content:
            raise ValueError("Retrieved content cannot be empty.")

        if not student_level or not student_level.strip():
            raise ValueError("Student level cannot be empty.")

        context_parts = []

        for index, item in enumerate(retrieved_content, start=1):
            text = item.get("text", "").strip()
            metadata = item.get("metadata", {})

            if not text:
                continue

            context_parts.append(
                f"""
SOURCE {index}
Content:
{text}

Metadata:
{metadata}
"""
            )

        if not context_parts:
            raise ValueError(
                "Retrieved content contains no usable text."
            )

        retrieved_context = "\n".join(context_parts)

        prompt = f"""
{self.SYSTEM_INSTRUCTIONS}

Student level:
{student_level}

Student question:
{question}

Retrieved educational content:
{retrieved_context}

Instructions for your response:
1. Answer the student's question using the retrieved content.
2. Explain the concept clearly and at an appropriate level.
3. Use examples when they are supported by the retrieved content.
4. Do not introduce unsupported facts as if they came from the sources.
5. If the sources are insufficient, clearly state that limitation.
6. Help the student understand the reasoning behind the answer.

Teaching response:
"""

        return prompt.strip()


if __name__ == "__main__":
    builder = PromptBuilder()

    sample_content = [
        {
            "text": (
                "Supervised learning is a machine learning approach "
                "where a model learns from labeled training data."
            ),
            "metadata": {
                "topic": "machine learning",
                "source": "sample_machine_learning.txt",
            },
        }
    ]

    prompt = builder.build(
        question="What is supervised learning?",
        retrieved_content=sample_content,
        student_level="beginner",
    )

    print(prompt)