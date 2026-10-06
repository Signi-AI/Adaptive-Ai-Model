import re
from pathlib import Path

RAW = Path("backend/data/content/raw")
OUT = Path("backend/data/content/processed")


def list_pdfs():
    return sorted(RAW.rglob("*.pdf"))


def doc_id(pdf):
    return re.sub(r"[^a-z0-9]+", "_", pdf.stem.lower()).strip("_")


def doc_dir(pdf):
    path = OUT / doc_id(pdf)
    path.mkdir(parents=True, exist_ok=True)
    return path