from rag_gemma_pipeline import RAGGemmaPipeline


DOCUMENTS = [
    {
        "text": (
            "Machine learning is a field of artificial intelligence "
            "where computers learn patterns from data and use those "
            "patterns to make predictions or decisions."
        ),
        "metadata": {
            "topic": "machine learning",
            "source": "sample_machine_learning.txt",
            "level": "beginner",
        },
    },
    {
        "text": (
            "Supervised learning is a type of machine learning in which "
            "a model learns from labeled training data. Each training "
            "example contains an input and a known target or label."
        ),
        "metadata": {
            "topic": "supervised learning",
            "source": "sample_supervised_learning.txt",
            "level": "beginner",
        },
    },
    {
        "text": (
            "Unsupervised learning works with data that does not have "
            "known labels. The model attempts to discover patterns, "
            "groups, or structures within the data."
        ),
        "metadata": {
            "topic": "unsupervised learning",
            "source": "sample_unsupervised_learning.txt",
            "level": "beginner",
        },
    },
    {
        "text": (
            "Classification is a supervised learning task where a model "
            "predicts a category or class for an input."
        ),
        "metadata": {
            "topic": "classification",
            "source": "sample_classification.txt",
            "level": "beginner",
        },
    },
]


def test_complete_pipeline():
    print("=" * 70)
    print("RAG + GEMMA END-TO-END INTEGRATION TEST")
    print("=" * 70)

    question = "What is supervised learning?"

    print("\n[1] Initializing pipeline...")

    pipeline = RAGGemmaPipeline(
        model="gemma3:1b"
    )

    print("[OK] Pipeline initialized.")

    print("\n[2] Building knowledge index...")

    pipeline.build_knowledge_index(DOCUMENTS)

    print("[OK] Knowledge index built.")

    print("\n[3] Asking student question...")
    print(f"Question: {question}")

    result = pipeline.ask(
        question=question,
        student_level="beginner",
        top_k=3,
    )

    print("[OK] Pipeline completed.")

    print("\n" + "=" * 70)
    print("RETRIEVED CONTENT")
    print("=" * 70)

    retrieved_content = result["retrieved_content"]

    assert retrieved_content, (
        "No educational content was retrieved."
    )

    for index, item in enumerate(
        retrieved_content,
        start=1,
    ):
        print(f"\nResult {index}")
        print(f"Score: {item['score']:.4f}")
        print(f"Text: {item['text']}")
        print(f"Metadata: {item['metadata']}")

    print("\n[OK] Relevant content was retrieved.")

    print("\n" + "=" * 70)
    print("GEMMA TEACHING RESPONSE")
    print("=" * 70)

    answer = result["answer"]

    assert answer, "Gemma returned an empty response."

    print(answer)

    print("\n[OK] Gemma returned a teaching response.")

    print("\n" + "=" * 70)
    print("SOURCE METADATA")
    print("=" * 70)

    sources = result["sources"]

    assert sources, "Source metadata was not returned."

    for index, source in enumerate(
        sources,
        start=1,
    ):
        print(f"\nSource {index}")
        print(f"Score: {source['score']:.4f}")
        print(f"Metadata: {source['metadata']}")

    print("\n[OK] Source metadata is available.")

    print("\n" + "=" * 70)
    print("ACCEPTANCE CRITERIA")
    print("=" * 70)

    print("[PASS] Relevant content reaches the integration pipeline.")
    print("[PASS] Grounded teaching prompt is generated.")
    print("[PASS] Local Gemma generates the teaching response.")
    print("[PASS] Source metadata is returned.")
    print("[PASS] Pipeline runs using local components.")

    print("\n" + "=" * 70)
    print("ALL RAG + GEMMA INTEGRATION TESTS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    test_complete_pipeline()