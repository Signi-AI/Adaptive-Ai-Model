"""Import Google Drive textbook files into the local teacher library.

This utility needs internet only while it downloads a public Google Drive file.
The running system reads the copied PDFs and generated chunks locally; it never
reads these links. Each line in book_links.txt must be a Drive *file* link to a
PDF or to a ZIP containing PDFs.
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

import gdown

BACKEND_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_ROOT.parent
LINKS_FILE = BACKEND_ROOT / "book_links.txt"
RAW_DIR = PROJECT_ROOT / "Model" / "data" / "raw"


def _links() -> list[str]:
    if not LINKS_FILE.exists():
        raise SystemExit(f"Links file not found: {LINKS_FILE}")
    return [
        line.strip()
        for line in LINKS_FILE.read_text(encoding="utf-8-sig").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def _safe_name(name: str) -> str:
    """A downloaded archive must never choose a destination path."""
    cleaned = "_".join(Path(name).name.split())
    return cleaned or "textbook.pdf"


def _copy_pdf(pdf: Path, existing: set[str]) -> bool:
    name = _safe_name(pdf.name)
    key = name.casefold()
    if key in existing:
        return False
    shutil.copy2(pdf, RAW_DIR / name)
    existing.add(key)
    return True


def _extract_pdfs(archive: Path, folder: Path) -> list[Path]:
    """Extract PDF files only, safely, to the temporary folder."""
    folder.mkdir(parents=True, exist_ok=True)
    folder_root = folder.resolve()
    pdfs: list[Path] = []
    with zipfile.ZipFile(archive) as zf:
        for member in zf.infolist():
            if member.is_dir() or not member.filename.lower().endswith(".pdf"):
                continue
            destination = (folder / Path(member.filename).name).resolve()
            if destination.parent != folder_root:
                raise ValueError(f"Unsafe archive entry: {member.filename}")
            with zf.open(member) as source, destination.open("wb") as target:
                shutil.copyfileobj(source, target)
            pdfs.append(destination)
    return pdfs


def main() -> int:
    links = _links()
    if not links:
        print(f"Add one public Google Drive file link per line to {LINKS_FILE}.")
        return 2

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    existing = {path.name.casefold() for path in RAW_DIR.rglob("*.pdf")}
    added = skipped = 0

    with tempfile.TemporaryDirectory(prefix="toalm_book_download_") as temp:
        temp_dir = Path(temp)
        for number, link in enumerate(links, 1):
            downloaded = temp_dir / f"download_{number}"
            print(f"Downloading book link {number}/{len(links)}...")
            result = gdown.download(url=link, output=str(downloaded), quiet=False, fuzzy=True)
            if not result or not downloaded.exists():
                print(f"  FAILED: Google Drive did not return a file for: {link}")
                continue

            if zipfile.is_zipfile(downloaded):
                candidates = _extract_pdfs(downloaded, temp_dir / f"archive_{number}")
            elif downloaded.read_bytes()[:5] == b"%PDF-":
                candidates = [downloaded]
            else:
                print("  FAILED: the link must point to a PDF or ZIP of PDFs, not a Drive folder/page.")
                continue

            if not candidates:
                print("  FAILED: no PDFs were found in that ZIP.")
                continue
            for pdf in candidates:
                if _copy_pdf(pdf, existing):
                    added += 1
                else:
                    skipped += 1

    print(f"\nImported PDFs: {added}; already present: {skipped}")
    print(f"Local textbook folder: {RAW_DIR}")
    print("Next: describe the PDFs in Model/data/manifest.json, then run Model/scripts/ingest_content.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
