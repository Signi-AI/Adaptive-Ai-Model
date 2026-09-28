import json
from pathlib import Path

import faiss
import numpy as np

from embedding_service import EmbeddingService


class RetrievalPipeline:
    """Local FAISS-based retrieval pipeline."""

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.index = None
        self.records = []

    def build_index(self, documents: list[dict]):
        """
        Generate embeddings and build a FAISS similarity index.

        Each document must contain:
        - text
        - metadata
        """

        texts = [document["text"] for document in documents]

        embeddings = self.embedding_service.encode(texts)

        embeddings = np.asarray(embeddings, dtype="float32")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

        self.records = documents

    def search(self, query: str, top_k: int = 3):
        """Retrieve the most relevant document chunks."""

        if self.index is None:
            raise RuntimeError("The FAISS index has not been built.")

        query_embedding = self.embedding_service.encode_query(query)

        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32",
        )

        top_k = min(top_k, self.index.ntotal)

        scores, indices = self.index.search(
            query_embedding,
            top_k,
        )

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            record = self.records[index]

            results.append(
                {
                    "score": float(score),
                    "text": record["text"],
                    "metadata": record["metadata"],
                }
            )

        return results

    def search_by_topic(
        self,
        query: str,
        topic: str,
        top_k: int = 3,
    ):
        """
        Retrieve relevant document chunks restricted to a topic.
        """

        if self.index is None:
            raise RuntimeError("The FAISS index has not been built.")

        query_embedding = self.embedding_service.encode_query(query)

        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32",
        )

        candidate_count = min(
            max(top_k * 5, top_k),
            self.index.ntotal,
        )

        scores, indices = self.index.search(
            query_embedding,
            candidate_count,
        )

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            record = self.records[index]

            if record["metadata"].get("topic") == topic:
                results.append(
                    {
                        "score": float(score),
                        "text": record["text"],
                        "metadata": record["metadata"],
                    }
                )

            if len(results) >= top_k:
                break

        return results

    def save(self, directory: str):
        """Save the FAISS index and retrieval records locally."""

        if self.index is None:
            raise RuntimeError("The FAISS index has not been built.")

        directory_path = Path(directory)
        directory_path.mkdir(parents=True, exist_ok=True)

        faiss.write_index(
            self.index,
            str(directory_path / "index.faiss"),
        )

        with open(
            directory_path / "metadata.json",
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.records,
                file,
                indent=2,
                ensure_ascii=False,
            )

    def load(self, directory: str):
        """Load a previously saved FAISS index and retrieval records."""

        directory_path = Path(directory)

        self.index = faiss.read_index(
            str(directory_path / "index.faiss"),
        )

        with open(
            directory_path / "metadata.json",
            "r",
            encoding="utf-8",
        ) as file:
            self.records = json.load(file)