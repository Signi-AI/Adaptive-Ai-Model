import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[2] / "offline-rag-gemma-integration")
)

from rag_gemma_pipeline import RAGGemmaPipeline


documents = [
    {
        "text": "Supervised learning uses labeled training data.",
        "metadata": {"topic": "supervised learning"},
    },
    {
        "text": "Classification predicts a category or class.",
        "metadata": {"topic": "classification"},
    },
]


pipeline = RAGGemmaPipeline(model="gemma3:1b")

pipeline.build_knowledge_index(documents)

result = pipeline.ask(
    "What is supervised learning?",
    student_level="beginner",
    top_k=2,
)

assert result["answer"]
assert result["sources"]
assert result["retrieved_content"]

print("Generation test passed.")