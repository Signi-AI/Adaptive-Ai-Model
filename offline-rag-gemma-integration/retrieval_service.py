from pathlib import Path
import sys


# Allow this integration to reuse the already validated
# offline-rag-retrieval components.
RETRIEVAL_DIR = (
    Path(__file__).resolve().parent.parent
    / "offline-rag-retrieval"
)

sys.path.insert(0, str(RETRIEVAL_DIR))

from retrieval_pipeline import RetrievalPipeline


class RetrievalService:
    """
    Service responsible for retrieving relevant educational content.

    This integration reuses the validated local FAISS retrieval pipeline.
    No cloud service is required.
    """

    def __init__(self):
        self.pipeline = RetrievalPipeline()

    def build_index(self, documents: list[dict]) -> None:
        """
        Build the local retrieval index from educational documents.

        Each document must contain:
        - text
        - metadata
        """
        if not documents:
            raise ValueError("Documents cannot be empty.")

        self.pipeline.build_index(documents)

    def retrieve(
        self,
        question: str,
        top_k: int = 3,
    ) -> list[dict]:
        """
        Retrieve educational content relevant to the student's question.
        """

        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        return self.pipeline.search(
            question,
            top_k=top_k,
        )


if __name__ == "__main__":
    print("Retrieval service module loaded successfully.")