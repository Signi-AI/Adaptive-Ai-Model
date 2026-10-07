import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Model.ingestion.common import RAW, list_pdfs, norm

STOP_WORDS = {
    "form", "student", "students", "s", "book", "books", "textbook", "grade",
    "class", "std", "standard", "level", "by", "pdf", "notes", "note",
    "teacher", "teachers", "guide", "syllabus", "new", "edition", "part",
    "kidato", "darasa", "kitabu", "mwanafunzi", "mwalimu",
}

MAX_WORDS = 3


def subject_of(pdf):
    words = []
    for token in norm(pdf.stem).split("_"):
        if token in STOP_WORDS or token.isdigit() or "." in token:
            break
        words.append(token)
        if len(words) == MAX_WORDS:
            break
    return "_".join(w.capitalize() for w in words) or "General"


for pdf in list_pdfs():
    name = norm(pdf.name)
    subject = subject_of(pdf)

    target = RAW / subject / name
    target.parent.mkdir(exist_ok=True)
    if target != pdf:
        shutil.move(str(pdf), str(target))
    print(f"{subject}/{name}")

for folder in sorted(RAW.rglob("*"), reverse=True):
    if folder.is_dir() and not any(folder.iterdir()):
        folder.rmdir()