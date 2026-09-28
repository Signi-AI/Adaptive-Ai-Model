from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def main():
    print("Loading local embedding model...")

    model = SentenceTransformer(
        MODEL_NAME,
        local_files_only=True,
    )

    text = "Machine learning helps computers learn from data."

    embedding = model.encode(text)

    print("Embedding generated successfully.")
    print(f"Embedding dimensions: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")


if __name__ == "__main__":
    main()