import re
from pathlib import Path

RAW = Path("backend/data/content/raw")
OUT = Path("backend/data/content/processed")


def norm(name):
    return re.sub(r"[^a-z0-9.]+", "_", name.lower()).strip("_")


def list_pdfs():
    return sorted(RAW.rglob("*.pdf"))


def doc_id(pdf):
    return f"{norm(pdf.parent.name)}__{norm(pdf.stem)}"


def doc_dir(pdf):
    path = OUT / doc_id(pdf)
    path.mkdir(parents=True, exist_ok=True)
    return path

