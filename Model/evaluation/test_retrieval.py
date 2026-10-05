import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[2] / "offline-rag-gemma-integration")
)

from retrieval_service import RetrievalService


documents = [
    {
        "text": "Supervised learning uses labeled training data.",
        "metadata": {"topic": "supervised learning"},
    },
    {
        "text": "Unsupervised learning finds patterns without labels.",
        "metadata": {"topic": "unsupervised learning"},
    },
    {
        "text": "Classification predicts a category or class.",
        "metadata": {"topic": "classification"},
    },
]


service = RetrievalService()
service.build_index(documents)

results = service.retrieve(
    "What is supervised learning?",
    top_k=3,
)

assert results
assert "supervised learning" in results[0]["text"].lower()

print("Retrieval test passed.")