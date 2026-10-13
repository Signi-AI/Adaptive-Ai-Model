from pathlib import Path

from retrieval_pipeline import RetrievalPipeline


DOCUMENTS = [
    {
        "text": (
            "Supervised learning is a machine learning approach where "
            "a model learns from labeled training data. Each training "
            "example contains an input and a known target output."
        ),
        "metadata": {
            "chunk_id": "ml-001",
            "topic": "supervised-learning",
            "subject": "Machine Learning",
            "lesson": "Introduction to Supervised Learning",
        },
    },
    {
        "text": (
            "Unsupervised learning works with data that does not have "
            "labeled target values. Clustering is a common example "
            "of unsupervised learning."
        ),
        "metadata": {
            "chunk_id": "ml-002",
            "topic": "unsupervised-learning",
            "subject": "Machine Learning",
            "lesson": "Introduction to Unsupervised Learning",
        },
    },
    {
        "text": (
            "Classification is a supervised learning task where a model "
            "predicts a category or class for an input."
        ),
        "metadata": {
            "chunk_id": "ml-003",
            "topic": "classification",
            "subject": "Machine Learning",
            "lesson": "Classification Basics",
        },
    },
    {
        "text": (
            "Regression is a supervised learning task used to predict "
            "continuous numerical values such as prices or temperatures."
        ),
        "metadata": {
            "chunk_id": "ml-004",
            "topic": "regression",
            "subject": "Machine Learning",
            "lesson": "Regression Basics",
        },
    },
]


def print_results(title, results):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

    for position, result in enumerate(results, start=1):
        print(f"\nResult {position}")
        print(f"Score: {result['score']:.4f}")
        print(f"Text: {result['text']}")
        print(f"Metadata: {result['metadata']}")


def main():
    print("Creating local retrieval pipeline...")

    pipeline = RetrievalPipeline()

    # ---------------------------------------------------------
    # Step 1: Build the FAISS index
    # ---------------------------------------------------------

    print()
    print("Building FAISS index...")

    pipeline.build_index(DOCUMENTS)

    print("FAISS index built successfully.")

    # ---------------------------------------------------------
    # Step 2: Semantic retrieval
    # ---------------------------------------------------------

    query = "What is supervised learning?"

    results = pipeline.search(query, top_k=3)

    print_results(
        "TEST 1: SEMANTIC SIMILARITY RETRIEVAL",
        results,
    )

    assert results, "Semantic retrieval returned no results."

    assert "text" in results[0], "Retrieved result has no text chunk."
    assert "metadata" in results[0], "Retrieved result has no metadata."

    assert (
        results[0]["metadata"]["topic"]
        == "supervised-learning"
    ), "Unexpected top result."

    # ---------------------------------------------------------
    # Step 3: Topic-based retrieval
    # ---------------------------------------------------------

    topic = "supervised-learning"

    topic_results = pipeline.search_by_topic(
        query=query,
        topic=topic,
        top_k=3,
    )

    print_results(
        "TEST 2: TOPIC-BASED RETRIEVAL",
        topic_results,
    )

    assert topic_results, "Topic-based retrieval returned no results."

    for result in topic_results:
        assert (
            result["metadata"]["topic"] == topic
        ), "Incorrect topic returned."

        assert (
            "text" in result
        ), "Topic result has no text chunk."

    # ---------------------------------------------------------
    # Step 4: Save vector store
    # ---------------------------------------------------------

    vector_store_path = Path(
        "offline-rag-retrieval/vector_store"
    )

    print()
    print("=" * 60)
    print("TEST 3: SAVE LOCAL VECTOR STORE")
    print("=" * 60)

    pipeline.save(str(vector_store_path))

    print("FAISS index saved successfully.")
    print("Retrieval records saved successfully.")

    index_file = vector_store_path / "index.faiss"
    metadata_file = vector_store_path / "metadata.json"

    assert index_file.exists(), "FAISS index file was not created."
    assert metadata_file.exists(), "Metadata file was not created."

    print(f"Index file: {index_file}")
    print(f"Metadata file: {metadata_file}")

    # ---------------------------------------------------------
    # Step 5: Create a NEW pipeline and load the store
    # ---------------------------------------------------------

    print()
    print("=" * 60)
    print("TEST 4: LOAD SAVED VECTOR STORE")
    print("=" * 60)

    loaded_pipeline = RetrievalPipeline()

    loaded_pipeline.load(str(vector_store_path))

    print("FAISS index loaded successfully.")
    print("Retrieval records loaded successfully.")

    # ---------------------------------------------------------
    # Step 6: Search loaded vector store
    # ---------------------------------------------------------

    loaded_results = loaded_pipeline.search(
        query,
        top_k=3,
    )

    print_results(
        "TEST 5: SEARCH LOADED VECTOR STORE",
        loaded_results,
    )

    assert loaded_results, "Loaded vector store returned no results."

    assert (
        loaded_results[0]["metadata"]["topic"]
        == "supervised-learning"
    ), "Loaded vector store returned an unexpected top result."

    assert (
        "text" in loaded_results[0]
    ), "Loaded result has no text chunk."

    # ---------------------------------------------------------
    # Final validation
    # ---------------------------------------------------------

    print()
    print("=" * 60)
    print("ALL RETRIEVAL AND PERSISTENCE TESTS PASSED.")
    print("=" * 60)


if __name__ == "__main__":
    main()