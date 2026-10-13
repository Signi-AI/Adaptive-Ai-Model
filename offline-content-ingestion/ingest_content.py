import json
from pathlib import Path

from document_loader import DocumentLoader
from chunker import TextChunker
from metadata_extractor import MetadataExtractor


class IngestionPipeline:
    """Process raw educational documents into a local knowledge base."""

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
    ):
        self.loader = DocumentLoader()
        self.chunker = TextChunker(
            chunk_size=chunk_size,
            overlap=overlap,
        )
        self.metadata_extractor = MetadataExtractor()

    def process_directory(
        self,
        input_directory: str,
        output_file: str,
    ) -> list[dict]:
        """
        Load, chunk, add metadata, and save educational documents.
        """

        documents = self.loader.load_directory(input_directory)

        processed_records = []

        for document in documents:
            chunks = self.chunker.chunk_text(document["text"])

            for index, chunk in enumerate(chunks, start=1):
                metadata = self.metadata_extractor.extract(
                    text=document["text"],
                    source=document["source"],
                    chunk_id=index,
                )

                processed_records.append(
                    {
                        "text": chunk,
                        "metadata": metadata,
                    }
                )

        self._save_processed_content(
            processed_records,
            output_file,
        )

        return processed_records

    def _save_processed_content(
        self,
        records: list[dict],
        output_file: str,
    ) -> None:
        """Save processed records as JSON."""

        output_path = Path(output_file)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                records,
                file,
                indent=2,
                ensure_ascii=False,
            )


def main():
    """Run the local content ingestion process."""

    base_directory = Path(__file__).parent

    input_directory = base_directory / "raw"
    output_file = base_directory / "processed" / "processed_content.json"

    pipeline = IngestionPipeline(
        chunk_size=500,
        overlap=50,
    )

    records = pipeline.process_directory(
        input_directory=input_directory,
        output_file=output_file,
    )

    print("=" * 60)
    print("OFFLINE CONTENT INGESTION")
    print("=" * 60)
    print(f"Documents processed: {len(set(
        record['metadata']['source']
        for record in records
    ))}")
    print(f"Chunks created: {len(records)}")
    print(f"Output: {output_file}")
    print("Status: SUCCESS")
    print("=" * 60)


if __name__ == "__main__":
    main()