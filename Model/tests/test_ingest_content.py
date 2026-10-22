"""Ingestion tests: build a small real PDF, ingest it, and check the output is what the teacher needs."""
import json
import sys
from pathlib import Path

import pytest

try:
    import pymupdf as fitz
except ImportError:  # pragma: no cover
    import fitz

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import ingest_content as ic  # noqa: E402
from artificial_teacher.retrieval_service import RetrievalService  # noqa: E402

PAGES = [
    "Linear equations. A linear equation has one unknown. To solve 2x + 4 = 10 subtract 4 from both sides, then divide by 2. The answer is x = 3.",
    "Balancing. Whatever you do to one side of an equation you must do to the other side. This keeps the equation balanced and the solution unchanged.",
    "Fractions. A fraction shows part of a whole. The numerator is the top number and the denominator is the bottom number of the fraction.",
    "Multiplying fractions. Multiply the numerators together and multiply the denominators together, then simplify the fraction if you can.",
    "",  # a page with no text layer (like a scanned page)
]


def _make_pdf(path: Path) -> None:
    doc = fitz.open()
    for i, body in enumerate(PAGES, 1):
        page = doc.new_page()
        page.insert_textbox(fitz.Rect(40, 60, 550, 700), body, fontsize=11)
        page.insert_text((40, 30), "TIE Mathematics Form 2", fontsize=9)   # running header on every page
        page.insert_text((290, 820), str(i), fontsize=9)                  # page number
    doc.save(path)
    doc.close()


@pytest.fixture()
def workspace(tmp_path):
    pdf = tmp_path / "math_form2.pdf"
    _make_pdf(pdf)
    manifest = {"books": [{
        "file": "math_form2.pdf", "subject": "Mathematics", "class_level": "Form 2", "language": "en",
        "source": "Test Mathematics Form 2", "edition": "2021", "license_note": "test only",
        "topics": [{"name": "Linear Equations", "pages": [1, 2]}, {"name": "Fractions", "pages": [3, 4]},
                   {"name": "Broken", "pages": [5, 5]}, {"name": "OutOfRange", "pages": [4, 99]}],
    }]}
    mpath = tmp_path / "manifest.json"
    mpath.write_text(json.dumps(manifest))
    return tmp_path, mpath


def test_end_to_end_ingest_and_retrieve(workspace):
    root, mpath = workspace
    out, rep = root / "chunks.jsonl", root / "report.json"
    report = ic.ingest(mpath, out, rep, ocr=False, ocr_lang="eng", root=root)

    rows = [json.loads(line) for line in out.read_text().splitlines()]
    assert report["total_chunks"] == len(rows) >= 2
    topics = {r["topic"] for r in rows}
    assert topics == {"Linear Equations", "Fractions"}
    for r in rows:
        assert r["subject"] == "Mathematics" and r["class_level"] == "Form 2" and r["source"] == "Test Mathematics Form 2"
        assert "TIE Mathematics" not in r["text"]  # running header removed (book has >= 5 pages)
    entry = report["books"][0]
    assert entry["pages_total"] == 5 and entry["pages_without_text"] == 1
    assert any("outside 1-5" in w for w in entry["warnings"])        # bad page range reported
    assert any("0 chunks" in w for w in entry["warnings"])            # empty topic reported

    hits = RetrievalService(out).retrieve(subject="Mathematics", class_level="Form 2",
                                          topic="Linear Equations", query="how to balance both sides")
    assert hits and hits[0].chunk.topic == "Linear Equations"


def test_running_headers_and_page_numbers_are_removed(workspace):
    root, _ = workspace
    pages = ic.extract_pages(root / "math_form2.pdf", ocr=False, ocr_lang="eng")
    texts = [t for _, t, _ in pages]
    repeated = ic.find_repeated_lines(texts)
    cleaned = ic.clean_page_text(texts[0], repeated)
    assert "TIE Mathematics" not in cleaned
    assert not cleaned.strip().endswith("1")
    assert "linear equation" in cleaned.lower()


def test_clean_page_text_rejoins_hyphenated_words_and_drops_page_numbers():
    raw = "The equa-\ntion is solved.\n\n12\n\nPage 13\nNext line"
    out = ic.clean_page_text(raw)
    assert "equation is solved." in out and "12" not in out and "Page 13" not in out


def test_chunking_respects_size_and_pages():
    long_page = " ".join(f"Sentence number {i} explains one small idea about equations." for i in range(60))
    chunks = ic.chunk_pages([(7, long_page), (8, "Short closing paragraph that is long enough to be kept as text.")])
    assert len(chunks) >= 3
    assert all(len(text) <= ic.MAX_CHARS + 50 for text, _, _ in chunks)
    assert chunks[0][1] == 7 and chunks[-1][2] == 8


def test_duplicates_are_dropped(tmp_path):
    pdf = tmp_path / "b.pdf"
    doc = fitz.open()
    for _ in range(2):
        doc.new_page().insert_textbox(fitz.Rect(40, 60, 550, 700),
                                      "Identical paragraph about fractions that appears twice in this test book.", fontsize=11)
    doc.save(pdf)
    doc.close()
    m = tmp_path / "m.json"
    m.write_text(json.dumps({"books": [{"file": "b.pdf", "subject": "Mathematics", "class_level": "Form 2",
                                        "language": "en", "source": "Dup Book", "topics": [
                                            {"name": "A", "pages": [1, 1]}, {"name": "B", "pages": [2, 2]}]}]}))
    report = ic.ingest(m, tmp_path / "o.jsonl", tmp_path / "r.json", False, "eng", tmp_path)
    assert report["total_chunks"] == 1 and report["duplicate_chunks_dropped"] == 1


def test_manifest_requires_documentation_keys(tmp_path):
    m = tmp_path / "m.json"
    m.write_text(json.dumps({"books": [{"file": "x.pdf", "subject": "Mathematics"}]}))
    with pytest.raises(SystemExit):
        ic.load_manifest(m)


def test_missing_pdf_is_reported_not_crashed(tmp_path):
    m = tmp_path / "m.json"
    m.write_text(json.dumps({"books": [{"file": "ghost.pdf", "subject": "S", "class_level": "Form 1",
                                        "language": "en", "source": "Ghost"}]}))
    report = ic.ingest(m, tmp_path / "o.jsonl", tmp_path / "r.json", False, "eng", tmp_path)
    assert report["total_chunks"] == 0 and "FILE NOT FOUND" in report["books"][0]["warnings"][0]


def test_mostly_blank_book_is_flagged_as_scanned(tmp_path):
    pdf = tmp_path / "scan.pdf"
    doc = fitz.open()
    for _ in range(4):
        doc.new_page()  # no text layer at all, like a scanned page
    doc.new_page().insert_textbox(fitz.Rect(40, 60, 550, 700), "One real page of text about equations and balance.", fontsize=11)
    doc.save(pdf)
    doc.close()
    m = tmp_path / "m.json"
    m.write_text(json.dumps({"books": [{"file": "scan.pdf", "subject": "Mathematics", "class_level": "Form 2",
                                        "language": "en", "source": "Scanned Book"}]}))
    report = ic.ingest(m, tmp_path / "o.jsonl", tmp_path / "r.json", False, "eng", tmp_path)
    assert any("probably scanned" in w for w in report["books"][0]["warnings"])
