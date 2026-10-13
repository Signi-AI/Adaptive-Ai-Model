from pathlib import Path
import re


class MetadataExtractor:
    """Create metadata for processed educational content."""

    def extract(
        self,
        text: str,
        source: str,
        chunk_id: int,
        topic: str | None = None,
    ) -> dict:
        """
        Create metadata for a text chunk.

        Args:
            text: The original document text.
            source: Path or filename of the source document.
            chunk_id: Number identifying the chunk.
            topic: Optional topic name.

        Returns:
            A dictionary containing metadata.
        """

        source_path = Path(source)

        if topic is None:
            topic = self._extract_topic(text, source_path)

        return {
            "chunk_id": chunk_id,
            "source": source_path.name,
            "topic": topic,
        }

    def _extract_topic(self, text: str, source_path: Path) -> str:
        """
        Determine a topic from the first meaningful line.
        Falls back to the filename if necessary.
        """

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if lines:
            topic = lines[0]
        else:
            topic = source_path.stem.replace("_", " ")

        return self._normalize_topic(topic)

    def _normalize_topic(self, topic: str) -> str:
        """Convert a topic into a consistent searchable format."""

        topic = topic.lower().strip()
        topic = re.sub(r"[^a-z0-9\s-]", "", topic)
        topic = re.sub(r"\s+", "-", topic)

        return topic