import json
from pathlib import Path

from document_loader import DocumentLoader
from chunker import TextChunker
from metadata_extractor import MetadataExtractor
from ingest_content import IngestionPipeline


BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"
SAMPLE_FILE = RAW_DIR / "sample_machine_learning.txt"
OUTPUT_FILE = PROCESSED_DIR / "processed_content.json"


def test_document_loading():
    """Verify that documents load successfully."""

    loader = DocumentLoader()

    text = loader.load_document(str(SAMPLE_FILE))

    assert text.strip(), "Document text should not be empty."
    assert "Machine Learning" in text

    print("[PASS] Documents load successfully")


def test_chunking():
    """Verify that document content is split into chunks."""

    loader = DocumentLoader()
    chunker = TextChunker(chunk_size=500, overlap=50)

    text = loader.load_document(str(SAMPLE_FILE))
    chunks = chunker.chunk_text(text)

    assert len(chunks) > 0, "At least one chunk should be created."

    for chunk in chunks:
        assert chunk.strip(), "Chunks should not be empty."

    print(f"[PASS] Content chunked successfully ({len(chunks)} chunks)")


def test_metadata():
    """Verify that chunks contain topic metadata."""

    loader = DocumentLoader()
    chunker = TextChunker(chunk_size=500, overlap=50)
    metadata_extractor = MetadataExtractor()

    text = loader.load_document(str(SAMPLE_FILE))
    chunks = chunker.chunk_text(text)

    for index, _chunk in enumerate(chunks, start=1):
        metadata = metadata_extractor.extract(
            text=text,
            source=str(SAMPLE_FILE),
            chunk_id=index,
        )

        assert "topic" in metadata
        assert metadata["topic"]
        assert "source" in metadata
        assert "chunk_id" in metadata

    print("[PASS] Chunks contain topic metadata")


def test_full_pipeline():
    """Verify the complete offline ingestion pipeline."""

    pipeline = IngestionPipeline(
        chunk_size=500,
        overlap=50,
    )

    records = pipeline.process_directory(
        input_directory=str(RAW_DIR),
        output_file=str(OUTPUT_FILE),
    )

    assert len(records) > 0
    assert OUTPUT_FILE.exists()

    with OUTPUT_FILE.open("r", encoding="utf-8") as file:
        saved_records = json.load(file)

    assert len(saved_records) == len(records)

    for record in saved_records:
        assert "text" in record
        assert "metadata" in record
        assert record["text"].strip()
        assert record["metadata"]["topic"]
        assert record["metadata"]["source"]

    print("[PASS] Full ingestion pipeline works offline")


def main():
    print("=" * 60)
    print("OFFLINE CONTENT INGESTION TESTS")
    print("=" * 60)

    test_document_loading()
    test_chunking()
    test_metadata()
    test_full_pipeline()

    print("=" * 60)
    print("ALL INGESTION TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()