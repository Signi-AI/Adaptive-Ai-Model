# TOALM V2 — Artificial Teacher MODEL component

This folder is the whole AI model component. It is **separate from `backend/`**: its own folder, its own
Python environment, its own `.env`, its own tests, its own server. The backend talks to it over HTTP
(see `docs/INFERENCE.md`). Place it next to the backend:

```
toalm-v2/
├── backend/          (FastAPI, PostgreSQL, students, progress, mastery ...)
└── model/            <-- this folder
```

## Layout

```
model/
├── README.md
├── requirements.txt            own dependencies
├── .env.example                copy to .env
├── artificial_teacher/         the code
│   ├── gemma_client.py         talks to local Gemma (through Ollama)
│   ├── retrieval_service.py    searches the textbooks, filtered by subject + class + topic
│   ├── prompt_builder.py       the one stable prompt format
│   ├── service.py              context in -> teaching response out
│   ├── student_context.py      input/output contract models
│   ├── server.py               the HTTP server the backend calls
│   └── settings.py             paths and .env loading
├── scripts/
│   ├── ingest_content.py       PDF books -> searchable chunks (+ quality report)
│   └── smoke_test_model.py     live test against the real model
├── data/
│   ├── raw/                    <== YOUR TEXTBOOK PDFs GO HERE
│   ├── manifest.example.json   copy to data/manifest.json and describe your books
│   ├── processed/              generated: chunks.jsonl, ingest_report.json
│   └── evaluation/             reserved for the formal test set (never used for training or retrieval)
├── tests/                      52 tests, no Ollama needed
└── docs/INFERENCE.md           API contract + how the backend calls the model
```

## Where the textbooks go

**Put every textbook PDF inside `model/data/raw/`.** Subfolders are optional but recommended:

```
model/data/raw/mathematics/form-2/mathematics_form2.pdf
model/data/raw/mathematics/std-5/hisabati_darasa5.pdf
model/data/raw/biology/form-2/biology_form2.pdf
```

Copying the file is only half of it. The system does not guess what a book is. You describe each book in
`model/data/manifest.json` (copy `data/manifest.example.json` and edit it). **A PDF that is not listed in the
manifest is ignored.** For every book you must give:

| Field | Meaning |
|---|---|
| `file` | Path from the `model` folder, for example `data/raw/mathematics/form-2/mathematics_form2.pdf` |
| `subject` | Must equal the subject name in your database, for example `Mathematics` |
| `class_level` | Must equal your ClassLevel value exactly, for example `Form 2` or `Std 5` |
| `language` | `en` or `sw` |
| `source` | Book title and publisher |
| `edition`, `license_note` | Edition/year and who allowed you to use the book (your issue requires this) |
| `topics` | List of `{"name": "...", "pages": [first, last]}`. Page numbers are PDF page numbers (page 1 = first page of the file, not the number printed on the page). Read them from the book's table of contents. Topic names must equal your database topic names. |

`data/raw/*.pdf` and the generated `data/processed/` files are in `.gitignore` on purpose: the books are
copyrighted and large, so they are not pushed to GitHub. Share them inside the team another way (USB drive, shared folder).

## Setup, step by step

**0. Requirements.** Python 3.10 or newer (check with `python --version`). Internet is needed ONCE, to
download Ollama and the model. After that the system runs offline.

**1. Create this component's own environment.** Open a terminal in the `model` folder.
- Windows: `python -m venv .venv` then `.venv\Scripts\activate`
- Linux/macOS: `python3 -m venv .venv` then `source .venv/bin/activate`

The prompt should now start with `(.venv)`.

**2. Install the Python packages.** `pip install -r requirements.txt`

**3. Install Ollama** (the program that runs Gemma on your machine).
- Windows: download the installer from https://ollama.com/download, run it, finish the wizard. It then runs in the background.
- Linux: `curl -fsSL https://ollama.com/install.sh | sh`
- Check: open a NEW terminal and run `ollama --version`. A version number means it worked.

**4. Download the model.** `ollama pull gemma3:4b` (about 3.3 GB). Then `ollama list` must show `gemma3:4b`.
Low-RAM machine: use `gemma3:1b`. Strong machine (plenty of RAM, ideally a GPU): test `gemma3:12b`.
Write the chosen model into `.env` (step 5) and document it, your issue requires the exact model and version.
Keep Ollama on its default address `127.0.0.1`. Do NOT expose it to the network.

**5. Create your settings file.** Copy `.env.example` to `.env` (same folder). Defaults work. Change `TEACHER_MODEL` if you chose another size.

**6. Add the books.** Follow "Where the textbooks go" above: PDFs into `data/raw/`, then `data/manifest.json`.

**7. Ingest the books.** `python scripts/ingest_content.py`
Read everything it prints and `data/processed/ingest_report.json`. A WARNING about "no text layer" means that
book is scanned (see "Scanned books"). A topic with `0 chunks` means the teacher knows nothing about that topic.
Fix the manifest or the book, then run it again. Exit code 0 means no warnings.

**8. Smoke test the real model.** `python scripts/smoke_test_model.py`
Other class/topic: `python scripts/smoke_test_model.py --class-level "Std 5" --topic "Fractions" --language sw`
It prints a reply for a weak student, a strong student, and a wrong answer. Read them yourself. Passing the
automatic checks does not prove the teaching is good.

**9. Start the model server.** `uvicorn artificial_teacher.server:app --host 127.0.0.1 --port 8100`
Use exactly ONE worker (the concurrency limit lives inside the process). Check it in a browser:
http://127.0.0.1:8100/health should show `"status":"ok"`. `"degraded"` means Ollama is not running or the model is not downloaded.

**10. Run the tests.** `pytest tests`

## Scanned books (optional)
If the ingest report says a book has no text layer: install Tesseract (Windows: the UB Mannheim installer;
Linux: `sudo apt install tesseract-ocr tesseract-ocr-eng tesseract-ocr-swa`), uncomment `pytesseract` and `Pillow`
in `requirements.txt`, run `pip install -r requirements.txt`, then `python scripts/ingest_content.py --ocr`.
OCR of mathematics (fractions, exponents, equations) is poor. Check the result by eye, or find a text-based edition.

## What was verified, and what was not
Verified: 52 tests; a real PDF ingested and searched; the real server started from a different directory, called
over HTTP with the API key, using a stand-in for Ollama. NOT verified: a live reply from real Gemma, OCR, and
Kiswahili quality. Step 8 verifies the first on your hardware.

## Known limits
- Retrieval matches words, not meaning (BM25). Topic filtering makes it work well, but it misses paraphrases.
- Topic tagging depends on the manifest page ranges. Wrong ranges mean wrong lessons.
- The model can make arithmetic mistakes. Send `verified_solution_steps` from your question engine instead of letting it calculate.
- Default language (Std = Kiswahili, Form = English) is an assumption. Confirm with teachers.
- One server and one model means students queue. Measure real latency on the real hardware.
- Not built yet, on purpose: fine-tuning (`TRAINING.md`), formal evaluation (`EVALUATION.md`), `DATASET.md`. Build the
  evaluation set first, then decide from its failures whether fine-tuning is needed.
