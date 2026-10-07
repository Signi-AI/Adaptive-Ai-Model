import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Model.ingestion.common import doc_dir, list_pdfs
NUMBERS = (
    r"\d+|[ivx]+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve"
    r"|moja|mbili|tatu|nne|tano|sita|saba|nane|tisa|kumi|kwanza|pili"
)

HEADING = re.compile(
    rf"^\s*(chapter|unit|topic|sura|mada|kipengele|kitengo)\s*(ya\s+)?({NUMBERS})\b.{{0,80}}$",
    re.I,
)


def from_toc(reader):
    topics = []

    def walk(items, level):
        for item in items:
            if isinstance(item, list):
                walk(item, level + 1)
                continue
            try:
                page = reader.get_destination_page_number(item) + 1
            except Exception:
                continue
            if level <= 2:
                topics.append({"title": item.title.strip(), "level": level, "start_page": page})

    try:
        walk(reader.outline, 1)
    except Exception:
        pass
    return sorted(topics, key=lambda t: t["start_page"])


def from_headings(pages):
    topics = []
    for page in pages:
        for line in page["text"].splitlines():
            if HEADING.match(line):
                topics.append({"title": line.strip(), "level": 1, "start_page": page["page"]})
                break
    return topics


def add_end_pages(topics, total):
    for i, topic in enumerate(topics):
        topic["end_page"] = topics[i + 1]["start_page"] if i + 1 < len(topics) else total
    return topics


for pdf in list_pdfs():
    folder = doc_dir(pdf)
    if (folder / "topics.json").exists():
        print(f"{pdf.name}: imerukwa (topics zipo)")
        continue
    pages_file = folder / "pages.jsonl"
    if not pages_file.exists():
        print(f"{pdf.name}: endesha extract_text.py kwanza")
        continue

    with open(pages_file, encoding="utf-8") as f:
        pages = [json.loads(line) for line in f]

    topics = from_toc(PdfReader(str(pdf)))
    source = "pdf_toc"
    if not topics:
        topics, source = from_headings(pages), "headings"

    topics = add_end_pages(topics, len(pages))
    (folder / "topics.json").write_text(
        json.dumps(topics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"{pdf.name}: {len(topics)} topics ({source})")