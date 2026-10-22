"""Ingest Tanzania textbooks (PDF) into data/processed/chunks.jsonl.

Usage (from the model folder):
    python scripts/ingest_content.py                      # uses data/manifest.json
    python scripts/ingest_content.py --ocr                # OCR pages that have no text layer
    python scripts/ingest_content.py --manifest other.json --out other_chunks.jsonl

You describe every book in a manifest (see data/manifest.example.json). The manifest is
the audit trail the project issue demands: source, subject, class, language, edition, licence note.
Topic page ranges come from the book's table of contents. That is the controlled, reliable way to
tie text to topics; automatic topic detection on scanned books is not trustworthy.

READ THE REPORT (data/processed/ingest_report.json). A pipeline that finishes without
errors can still have produced garbage if the PDF was scanned, so the report lists empty pages,
chunks per topic, and topics that ended up with nothing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

try:
    import pymupdf as fitz  # PyMuPDF >= 1.24
except ImportError:  # pragma: no cover
    import fitz  # type: ignore[no-redef]

REQUIRED_BOOK_KEYS = ("file", "subject", "class_level", "language", "source")
MIN_TEXT_CHARS = 30          # a page with less text than this is treated as "no text layer"
SCANNED_WARN_RATIO = 0.20    # warn when more than 20% of pages have no text
TARGET_CHARS = 900
MAX_CHARS = 1300
MIN_CHUNK_CHARS = 40


# ----------------------------------------------------------------------------- extraction
def _ocr_page(page, lang: str, dpi: int = 200) -> str:
    import pytesseract  # optional dependency
    from PIL import Image

    pix = page.get_pixmap(dpi=dpi, alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return pytesseract.image_to_string(img, lang=lang)


def extract_pages(pdf_path: Path, ocr: bool, ocr_lang: str) -> list[tuple[int, str, bool]]:
    """Returns [(page_number_1_based, text, used_ocr)]."""
    pages: list[tuple[int, str, bool]] = []
    with fitz.open(pdf_path) as doc:
        for i, page in enumerate(doc, 1):
            text = page.get_text("text") or ""
            used_ocr = False
            if ocr and len(text.strip()) < MIN_TEXT_CHARS:
                text = _ocr_page(page, ocr_lang)
                used_ocr = True
            pages.append((i, text, used_ocr))
    return pages


# ----------------------------------------------------------------------------- cleaning
def _line_key(line: str) -> str:
    return re.sub(r"\d+", "#", line.strip().casefold())


def find_repeated_lines(page_texts: list[str]) -> set[str]:
    """Short lines that appear on >= 40% of pages are running headers/footers."""
    if len(page_texts) < 5:
        return set()
    counts: Counter[str] = Counter()
    for text in page_texts:
        keys = {_line_key(ln) for ln in text.splitlines() if 0 < len(ln.strip()) <= 80}
        counts.update(keys)
    limit = 0.4 * len(page_texts)
    return {k for k, c in counts.items() if c >= limit}


def clean_page_text(text: str, repeated: set[str] | None = None) -> str:
    text = text.replace("\u00ad", "")
    text = re.sub(r"(\w)-\n([a-z])", r"\1\2", text)  # re-join words hyphenated at line ends
    repeated = repeated or set()
    paragraphs: list[str] = []
    current: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if line and (re.fullmatch(r"(?:page\s*)?\d{1,4}", line, flags=re.I) or _line_key(line) in repeated):
            continue
        if not line:
            if current:
                paragraphs.append(" ".join(current))
                current = []
        else:
            current.append(line)
    if current:
        paragraphs.append(" ".join(current))
    return "\n\n".join(re.sub(r"\s+", " ", p).strip() for p in paragraphs if p.strip())


# ------------------------------------------------------------------------------ chunking
def _pieces(paragraph: str) -> list[str]:
    if len(paragraph) <= MAX_CHARS:
        return [paragraph]
    out: list[str] = []
    for sentence in re.split(r"(?<=[.!?])\s+", paragraph):
        while len(sentence) > MAX_CHARS:  # no punctuation at all: hard split
            out.append(sentence[:MAX_CHARS])
            sentence = sentence[MAX_CHARS:]
        out.append(sentence)
    return out


def chunk_pages(pages: list[tuple[int, str]]) -> list[tuple[str, int, int]]:
    """pages = [(page_no, cleaned_text)] -> [(chunk_text, page_start, page_end)]."""
    chunks: list[tuple[str, int, int]] = []
    buf: list[str] = []
    size = 0
    start = end = 0

    def flush() -> None:
        nonlocal buf, size
        text = " ".join(buf).strip()
        if len(text) >= MIN_CHUNK_CHARS:
            chunks.append((text, start, end))
        buf, size = [], 0

    for page_no, text in pages:
        for para in text.split("\n\n"):
            for piece in _pieces(para.strip()):
                if not piece:
                    continue
                if buf and size + len(piece) + 1 > TARGET_CHARS:
                    flush()
                if not buf:
                    start = page_no
                buf.append(piece)
                size += len(piece) + 1
                end = page_no
    flush()
    return chunks


# ------------------------------------------------------------------------------- manifest
def load_manifest(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    books = data.get("books")
    if not isinstance(books, list) or not books:
        raise SystemExit(f"{path}: expected a non-empty 'books' list.")
    for n, book in enumerate(books, 1):
        missing = [k for k in REQUIRED_BOOK_KEYS if not book.get(k)]
        if missing:
            raise SystemExit(f"{path}: book #{n} is missing required keys: {', '.join(missing)}")
    return books


def ingest(manifest_path: Path, out_path: Path, report_path: Path, ocr: bool, ocr_lang: str, root: Path) -> dict:
    books = load_manifest(manifest_path)
    seen_hashes: set[str] = set()
    report: dict = {"books": [], "total_chunks": 0, "duplicate_chunks_dropped": 0}
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", encoding="utf-8") as out:
        for book in books:
            pdf = (root / book["file"]).resolve() if not Path(book["file"]).is_absolute() else Path(book["file"])
            entry: dict = {"file": book["file"], "warnings": []}
            report["books"].append(entry)
            if not pdf.exists():
                entry["warnings"].append(f"FILE NOT FOUND: {pdf}")
                continue
            for key in ("edition", "license_note"):
                if not book.get(key):
                    entry["warnings"].append(f"manifest has no '{key}' (the issue requires it documented)")

            raw_pages = extract_pages(pdf, ocr, ocr_lang)
            texts = {n: t for n, t, _ in raw_pages}
            repeated = find_repeated_lines(list(texts.values()))
            empty_pages = [n for n, t in texts.items() if len(t.strip()) < MIN_TEXT_CHARS]
            entry.update(
                pages_total=len(raw_pages),
                pages_without_text=len(empty_pages),
                pages_ocr=sum(1 for _, _, o in raw_pages if o),
                empty_page_numbers=empty_pages[:30],
            )
            if raw_pages and len(empty_pages) / len(raw_pages) > SCANNED_WARN_RATIO:
                entry["warnings"].append(
                    f"{len(empty_pages)}/{len(raw_pages)} pages have no text layer. This book is probably "
                    "scanned. Re-run with --ocr (needs Tesseract) or use a text-based edition."
                )

            topics = book.get("topics") or [{"name": None, "pages": [1, len(raw_pages)]}]
            per_topic: dict[str, int] = {}
            for topic in topics:
                name = topic.get("name")
                try:
                    first, last = topic["pages"]
                except (KeyError, ValueError, TypeError):
                    entry["warnings"].append(f"topic {name!r}: 'pages' must be [first, last]")
                    continue
                if not (1 <= first <= last <= len(raw_pages)):
                    entry["warnings"].append(f"topic {name!r}: page range {first}-{last} is outside 1-{len(raw_pages)}")
                    continue
                cleaned = [(n, clean_page_text(texts[n], repeated)) for n in range(first, last + 1)]
                count = 0
                for text, p_start, p_end in chunk_pages(cleaned):
                    digest = hashlib.sha1(re.sub(r"\W+", "", text.casefold()).encode()).hexdigest()
                    if digest in seen_hashes:
                        report["duplicate_chunks_dropped"] += 1
                        continue
                    seen_hashes.add(digest)
                    chunk_id = hashlib.sha1(f"{book['source']}|{name}|{digest}".encode()).hexdigest()[:12]
                    record = {
                        "id": chunk_id,
                        "text": text,
                        "subject": book["subject"],
                        "class_level": book["class_level"],
                        "topic": name,
                        "language": book["language"],
                        "source": book["source"],
                        "edition": book.get("edition"),
                        "page_start": p_start,
                        "page_end": p_end,
                    }
                    out.write(json.dumps(record, ensure_ascii=False) + "\n")
                    count += 1
                per_topic[name or "(whole book)"] = count
                if count == 0:
                    entry["warnings"].append(f"topic {name!r} produced 0 chunks (empty or scanned pages?)")
            entry["chunks_per_topic"] = per_topic
            report["total_chunks"] += sum(per_topic.values())

    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main() -> int:
    model_root = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", default=str(model_root / "data/manifest.json"))
    ap.add_argument("--out", default=str(model_root / "data/processed/chunks.jsonl"))
    ap.add_argument("--report", default=str(model_root / "data/processed/ingest_report.json"))
    ap.add_argument("--ocr", action="store_true", help="OCR pages without a text layer (needs Tesseract)")
    ap.add_argument("--ocr-lang", default="eng+swa", help="Tesseract languages, default eng+swa")
    args = ap.parse_args()

    manifest = Path(args.manifest)
    if not manifest.exists():
        print(f"Manifest not found: {manifest}\nCopy data/manifest.example.json to data/manifest.json and edit it.")
        return 2
    report = ingest(manifest, Path(args.out), Path(args.report), args.ocr, args.ocr_lang, model_root)

    print(f"\nTotal chunks written: {report['total_chunks']}  (duplicates dropped: {report['duplicate_chunks_dropped']})")
    problems = 0
    for b in report["books"]:
        print(f"\n{b['file']}")
        print(f"  pages: {b.get('pages_total', '?')}  no-text pages: {b.get('pages_without_text', '?')}  OCR pages: {b.get('pages_ocr', 0)}")
        for topic, n in (b.get("chunks_per_topic") or {}).items():
            print(f"  {n:>4} chunks  {topic}")
        for w in b["warnings"]:
            problems += 1
            print(f"  WARNING: {w}")
    print(f"\nReport: {args.report}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
