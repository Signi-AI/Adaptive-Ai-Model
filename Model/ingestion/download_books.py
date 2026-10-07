import shutil
import zipfile
from pathlib import Path

import gdown

from common import RAW, list_pdfs, norm

LINKS_FILE = Path(__file__).resolve().with_name("book_links.txt")
TMP = Path("backend/data/content/_download")

LINKS = [
    line.strip()
    for line in LINKS_FILE.read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.startswith("#")
]

RAW.mkdir(parents=True, exist_ok=True)
existing = {p.name for p in list_pdfs()}

for link in LINKS:
    TMP.mkdir(parents=True, exist_ok=True)
    zip_path = TMP / "books.zip"
    gdown.download(link, str(zip_path), fuzzy=True, quiet=False)

    with zipfile.ZipFile(zip_path) as z:
        z.extractall(TMP / "unzipped")

    added = skipped = 0
    for pdf in (TMP / "unzipped").rglob("*.pdf"):
        name = norm(pdf.name)
        if name in existing:
            skipped += 1
            continue
        shutil.move(str(pdf), str(RAW / name))
        existing.add(name)
        added += 1

    print(f"Imeongezwa: {added} | Imerukwa (zipo tayari): {skipped}")
    shutil.rmtree(TMP, ignore_errors=True)