from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingService:
    """Generate text embeddings using a local Sentence Transformer model."""

    def __init__(self, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(
            model_name,
            local_files_only=True,
        )

    def encode(self, texts: list[str]):
        """Convert a list of texts into normalized embedding vectors."""
        return self.model.encode(
            texts,
            normalize_embeddings=True,
        )

    def encode_query(self, query: str):
        """Convert a single query into a normalized embedding vector."""
        return self.model.encode(
            query,
            normalize_embeddings=True,
        )


if __name__ == "__main__":
    service = EmbeddingService()

    texts = [
        "Machine learning allows computers to learn from data.",
        "Supervised learning uses labeled training data.",
    ]

    embeddings = service.encode(texts)

    print("Embedding service test successful.")
    print(f"Number of texts: {len(texts)}")
    print(f"Embedding dimensions: {embeddings.shape[1]}")