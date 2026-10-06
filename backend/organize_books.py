import re
import shutil

from common import RAW, list_pdfs

SUBJECTS = {
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Geography",
    "History",
    "English",
    "Kiswahili",
    "Computer Science",
    "Civics",
    "Commerce",
    "Economics",
    "Book Keeping",
    "Business Studies",
    "Agriculture",
    "Bible knowledge",
    "Animal health and production",
    "historia ya tanzania na maadili",
    "Engneer science",
    "Art& design",
    "Autobody repair and painting",
    "Agro mechanics",
    "Graphic design",
    "Elimu ya kiislamu",
    "ICT",
    "Arabic language",
    "Additional mathematics",
    "Microeconomics",
    "organic chemistry",
    "General ang inorganic chemistry",
    "Physical chemistry",
    "Inorganic chemistry",
    "physical geography",
    "Human geography",
    "Practical geography",
    "Academic communication",
    "fasihi ya kiswahili",
    "Accoutancy",
    "Tunza afya",
    "Stad za awali za maisha",
    "Naipenda nchi yangu",
    "Sanaa bunifu na michezo",
    "kuhesabu sayansi na tehama",
    "stadi za awali za lugha",
    "Arithmetics",
    "Kuhesabu",
    "writing",
    "reading",
    "Kuandika",
    "Kusoma",
    "Health",
    "Afya",
    "culture",
    "culture & sports",
    "Sayansi",
    "Science",
    "Vocational studies",
    "Maarifa ya jamii"
}





def detect(text):
    normalized_text = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    for subject in sorted(SUBJECTS, key=len, reverse=True):
        normalized_subject = re.sub(r"[^a-z0-9]+", " ", subject.lower()).strip()
        if normalized_subject in normalized_text:
            return subject
    return None


for pdf in list_pdfs():
    name = re.sub(r"[^a-z0-9.]+", "_", pdf.name.lower()).strip("_")
    subject = detect(name) or detect(pdf.parent.name.lower())
    if not subject:
        subject = input(f"Somo la '{pdf.name}'? ").strip().title() or "General"

    target = RAW / subject / name
    target.parent.mkdir(exist_ok=True)
    if target != pdf:
        shutil.move(str(pdf), str(target))
    print(f"{pdf.name} -> {subject}/{name}")

for folder in sorted(RAW.rglob("*"), reverse=True):
    if folder.is_dir() and not any(folder.iterdir()):
        folder.rmdir()