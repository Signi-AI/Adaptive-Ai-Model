import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
STEPS = [
    "download_books.py",
    "organize_books.py",
    "extract_text.py",
    "ocr_text.py",
    "extract_topics.py",
    "build_metadata.py",
]

for step in STEPS:
    print(f"\n=== {step} ===")
    result = subprocess.run([sys.executable, str(HERE / step)])
    if result.returncode != 0:
        print(f"Imeshindwa kwenye {step}. Rekebisha kisha endesha tena.")
        sys.exit(result.returncode)

print("\nImekamilika. Angalia backend/data/content/processed/metadata.json")
