import json
import re
import sys
from pathlib import Path

import pypdfium2 as pdfium
import pytesseract

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ingest_utils import doc_dir, list_pdfs

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
LANG = "eng"  # kwa vitabu vya Kiswahili tumia "eng+swa" (inahitaji swa.traineddata)


def clean(text):
    text = re.sub(r"-\n(\w)", r"\1", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def has_text(path):
    if not path.exists():
        return False
    with open(path, encoding="utf-8") as f:
        return any(json.loads(line)["text"] for line in f)


for pdf in list_pdfs():
    out = doc_dir(pdf) / "pages.jsonl"
    if has_text(out):
        print(f"{pdf.name}: ina text tayari, imerukwa")
        continue

    doc = pdfium.PdfDocument(str(pdf))
    total = len(doc)
    print(f"{pdf.name}: OCR ya kurasa {total}")

    with open(out, "w", encoding="utf-8") as f:
        for i in range(total):
            image = doc[i].render(scale=3).to_pil()
            text = clean(pytesseract.image_to_string(image, lang=LANG))
            f.write(json.dumps({"page": i + 1, "text": text}, ensure_ascii=False) + "\n")
            print(f"  ukurasa {i + 1}/{total}: {len(text)} chars")
