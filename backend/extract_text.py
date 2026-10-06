import json
import re

from pypdf import PdfReader

from common import doc_dir, list_pdfs


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