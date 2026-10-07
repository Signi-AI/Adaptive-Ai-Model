import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Model.ingestion.common import doc_dir, list_pdfs


def clean(text):
    text = re.sub(r"-\n(\w)", r"\1", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


for pdf in list_pdfs():
    reader = PdfReader(str(pdf))
    pages = [clean(page.extract_text() or "") for page in reader.pages]

    with open(doc_dir(pdf) / "pages.jsonl", "w", encoding="utf-8") as f:
        for number, text in enumerate(pages, start=1):
            f.write(json.dumps({"page": number, "text": text}, ensure_ascii=False) + "\n")

    print(f"{pdf.name}: {len(pages)} pages, {sum(map(len, pages))} chars")