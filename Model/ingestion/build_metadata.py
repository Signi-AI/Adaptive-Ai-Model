import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ingest_utils import OUT, doc_dir, doc_id, list_pdfs

records = []

for pdf in list_pdfs():
    folder = doc_dir(pdf)
    pages_file = folder / "pages.jsonl"
    topics_file = folder / "topics.json"
    if not pages_file.exists():
        continue

    with open(pages_file, encoding="utf-8") as f:
        pages = [json.loads(line) for line in f]
    topics = json.loads(topics_file.read_text(encoding="utf-8")) if topics_file.exists() else []
    chars = sum(len(p["text"]) for p in pages)

    records.append({
        "id": doc_id(pdf),
        "title": pdf.stem,
        "subject": pdf.parent.name,
        "format": "pdf",
        "pages": len(pages),
        "chars": chars,
        "needs_ocr": chars / max(len(pages), 1) < 50,
        "topic_count": len(topics),
        "topics": topics,
        "source": "Google Drive",
        "path": pdf.as_posix(),
    })

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "metadata.json").write_text(
    json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(f"metadata.json imeundwa: {len(records)} vitabu")

