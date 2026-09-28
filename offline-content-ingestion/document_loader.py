from pathlib import Path


class DocumentLoader:
    """Load educational text documents from local storage."""

    def load_document(self, file_path: str) -> str:
        """
        Load a single .txt document and return its text.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Document not found: {path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        if path.suffix.lower() != ".txt":
            raise ValueError(
                f"Unsupported file type: {path.suffix}. "
                "Only .txt files are supported."
            )

        return path.read_text(encoding="utf-8")

    def load_directory(self, directory_path: str) -> list[dict]:
        """
        Load all .txt documents from a local directory.

        Returns:
            A list containing each document's source path and text.
        """

        directory = Path(directory_path)

        if not directory.exists():
            raise FileNotFoundError(
                f"Directory not found: {directory}"
            )

        if not directory.is_dir():
            raise ValueError(
                f"Path is not a directory: {directory}"
            )

        documents = []

        for file_path in sorted(directory.glob("*.txt")):
            documents.append(
                {
                    "source": str(file_path),
                    "filename": file_path.name,
                    "text": self.load_document(str(file_path)),
                }
            )

        return documents