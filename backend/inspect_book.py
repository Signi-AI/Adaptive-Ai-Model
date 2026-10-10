import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Model.ingestion.common import doc_dir, list_pdfs

KEYWORDS = re.compile(r"chapter|unit|topic|sura|mada|kipengele|kitengo|contents|yaliyomo", re.I)

for pdf in list_pdfs():
    folder = doc_dir(pdf)
    with open(folder / "pages.jsonl", encoding="utf-8") as f:
        pages = [json.loads(line) for line in f]

    reader = PdfReader(str(pdf))
    try:
        bookmarks = len(reader.outline)
    except Exception:
        bookmarks = 0

    chars = sum(len(p["text"]) for p in pages)
    print("=" * 60)
    print(pdf.name)
    print(f"pages={len(pages)} chars={chars} avg/page={chars // max(len(pages), 1)} bookmarks={bookmarks}")

    print("--- mistari yenye maneno muhimu (kurasa 30 za kwanza) ---")
    shown = 0
    for p in pages[:30]:
        for line in p["text"].splitlines():
            if KEYWORDS.search(line) and shown < 25:
                print(f"p{p['page']}: {line.strip()[:90]}")
                shown += 1