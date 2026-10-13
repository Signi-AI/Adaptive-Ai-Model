from gemma_client import GemmaClient
from prompt_builder import PromptBuilder
from retrieval_service import RetrievalService


class RAGGemmaPipeline:
    """
    End-to-end offline RAG + Gemma teaching pipeline.

    Flow:
        Student Question
            ↓
        Retrieval
            ↓
        Retrieved Content
            ↓
        Grounded Teaching Prompt
            ↓
        Local Gemma
            ↓
        Teaching Response + Source Metadata
    """

    def __init__(self, model: str = "gemma3:1b"):
        self.retrieval_service = RetrievalService()
        self.prompt_builder = PromptBuilder()
        self.gemma_client = GemmaClient(model=model)

    def build_knowledge_index(self, documents: list[dict]) -> None:
        """
        Build the local retrieval index.

        Each document must contain:
            text
            metadata
        """

        self.retrieval_service.build_index(documents)

    def ask(
        self,
        question: str,
        student_level: str = "beginner",
        top_k: int = 3,
    ) -> dict:
        """
        Run the complete RAG + Gemma pipeline.

        Returns:
            question
            answer
            sources
            retrieved_content
        """

        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        # Step 1: Retrieve relevant educational content.
        retrieved_content = self.retrieval_service.retrieve(
            question,
            top_k=top_k,
        )

        if not retrieved_content:
            return {
                "question": question,
                "answer": (
                    "I could not find relevant educational content "
                    "for this question."
                ),
                "sources": [],
                "retrieved_content": [],
            }

        # Step 2: Build a grounded teaching prompt.
        prompt = self.prompt_builder.build(
            question=question,
            retrieved_content=retrieved_content,
            student_level=student_level,
        )

        # Step 3: Send the grounded prompt to local Gemma.
        answer = self.gemma_client.generate(prompt)

        # Step 4: Preserve source metadata.
        sources = []

        for item in retrieved_content:
            sources.append(
                {
                    "score": item["score"],
                    "metadata": item["metadata"],
                }
            )

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "retrieved_content": retrieved_content,
        }


if __name__ == "__main__":
    print("RAG + Gemma pipeline module loaded successfully.")