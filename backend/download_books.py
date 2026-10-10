import re
import shutil
import sys
import zipfile
from pathlib import Path

import gdown

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Model.ingestion.common import RAW, list_pdfs, norm

LINKS_FILE = Path(__file__).resolve().with_name("book_links.txt")
TMP = Path("backend/data/content/_download")

LINKS = [
    line.strip()
    for line in LINKS_FILE.read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.startswith("#")
]


def file_id(link):
    match = re.search(r"/d/([\w-]+)", link) or re.search(r"id=([\w-]+)", link)
    if not match:
        raise ValueError(f"Link haina ID: {link}")
    return match.group(1)


RAW.mkdir(parents=True, exist_ok=True)
existing = {p.name for p in list_pdfs()}

for link in LINKS:
    TMP.mkdir(parents=True, exist_ok=True)
    zip_path = TMP / "books.zip"
    gdown.download(f"https://drive.google.com/uc?id={file_id(link)}", str(zip_path), quiet=False)

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
