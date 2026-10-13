import json
import re

from pypdf import PdfReader

from ingest_utils import doc_dir, list_pdfs

WORDS = {w: i for i, w in enumerate(
    "one two three four five six seven eight nine ten eleven twelve".split(), 1)}
WORDS.update({w: i for i, w in enumerate(
    "moja mbili tatu nne tano sita saba nane tisa kumi".split(), 1)})
WORDS.update({"kwanza": 1, "pili": 2})
ROMAN = {"i": 1, "l": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6,
         "vii": 7, "viii": 8, "ix": 9, "x": 10, "xi": 11, "xii": 12}

KIND = r"(?:chapter|chaptcr|chapler|unit|topic|sura|mada|kipengele|kitengo)"
NUM = "|".join([r"\d+", r"[ivxl]+"] + list(WORDS))
HEADING = re.compile(
    rf"^\W{{0,3}}({KIND})\s*(?:ya\s+)?({NUM})\b[\s:.\-\u2013\u2014]*(.*)$", re.I)
LEADER = re.compile(r"[.\u2026\u00b7]{3,}")
CONNECTORS = {"and", "of", "for", "in", "on", "to", "with", "the", "from",
              "a", "an", "various", "through", "by", "at", "using", "kwa", "na", "ya"}


def to_int(token):
    token = token.lower()
    return int(token) if token.isdigit() else WORDS.get(token) or ROMAN.get(token)


def clean_title(text):
    text = re.sub(r"[.\u2026\u00b7_]{2,}.*$", "", text)
    text = re.sub(r"\s+\d{1,3}\s*$", "", text)
    text = re.sub(r"[^\w\s,;:&'()/\-]", " ", text)
    return re.sub(r"\s+", " ", text).strip(" .:;,-")


def quality(title):
    words = re.findall(r"[A-Za-z']+", title)
    if len(title) < 4 or not words:
        return 0
    if re.search(r"(.)\1{2}", title.lower()):
        return 0
    if title.isupper() and len(words) > 6:
        return 0
    good = sum(1 for w in words if len(w) >= 3)
    if good / len(words) < 0.75:
        return 0
    return min(len(title), 80)


def title_after(lines, i, inline):
    first, idx = (inline, i) if quality(inline) > 0 else ("", i)
    if not first:
        for j in range(i + 1, min(i + 4, len(lines))):
            if HEADING.match(lines[j]):
                break
            candidate = clean_title(lines[j])
            if quality(candidate) > 0:
                first, idx = candidate, j
                break
    if not first:
        return ""
    if idx + 1 < len(lines) and not HEADING.match(lines[idx + 1]):
        nxt = clean_title(lines[idx + 1])
        if quality(nxt) > 0 and len(nxt.split()) <= 6:
            if first.split()[-1].lower() in CONNECTORS or nxt[0].islower():
                first = f"{first} {nxt}"
    return first


def find_by_title(pages, title, after):
    key = " ".join(re.findall(r"[a-z]+", title.lower())[:3])
    if len(key) < 8:
        return None
    for p in pages:
        if p["page"] <= after:
            continue
        for line in p["text"].splitlines():
            if key in " ".join(re.findall(r"[a-z]+", line.lower())):
                return p["page"]
    return None


def from_bookmarks(reader):
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


def from_text(pages):
    occ = {}
    for p in pages:
        lines = [l.strip() for l in p["text"].splitlines() if l.strip()]
        heads = [(i, HEADING.match(l)) for i, l in enumerate(lines)]
        heads = [(i, m) for i, m in heads if m and to_int(m.group(2))]
        for i, m in heads:
            num = to_int(m.group(2))
            if num > 30:
                continue
            toc = len(heads) >= 3 or bool(LEADER.search(lines[i]))
            occ.setdefault(num, []).append({
                "page": p["page"], "kind": m.group(1), "toc": toc,
                "title": title_after(lines, i, clean_title(m.group(3))),
            })
    if not occ:
        return [], []

    toc_last = max((o["page"] for items in occ.values() for o in items if o["toc"]), default=0)
    topics, missing, prev = [], [], 0
    for num in range(1, max(occ) + 1):
        items = occ.get(num, [])
        title = max((o["title"] for o in items), key=quality, default="")
        if quality(title) == 0:
            title = ""
        bodies = [o["page"] for o in items if not o["toc"] and o["page"] > prev]
        page = min(bodies) if bodies else None
        if page is None and title:
            page = find_by_title(pages, title, max(prev, toc_last))
        if page is None:
            missing.append(num)
            continue
        kind = "Chapter" if not items or items[0]["kind"].lower().startswith("ch") else items[0]["kind"].title()
        topics.append({
            "title": f"{kind} {num}: {title}" if title else f"{kind} {num}",
            "level": 1,
            "start_page": page,
        })
        prev = page
    return topics, missing


def add_end_pages(topics, total):
    for i, topic in enumerate(topics):
        topic["end_page"] = topics[i + 1]["start_page"] if i + 1 < len(topics) else total
    return topics


for pdf in list_pdfs():
    folder = doc_dir(pdf)
    pages_file = folder / "pages.jsonl"
    if not pages_file.exists():
        print(f"{pdf.name}: hakuna pages.jsonl")
        continue
    if (folder / "topics.json").exists():
        print(f"{pdf.name}: imerukwa (topics zipo)")
        continue

    with open(pages_file, encoding="utf-8") as f:
        pages = [json.loads(line) for line in f]

    missing = []
    topics = from_bookmarks(PdfReader(str(pdf)))
    source = "pdf_bookmarks"
    if not topics:
        topics, missing = from_text(pages)
        source = "text"

    topics = add_end_pages(topics, len(pages))
    (folder / "topics.json").write_text(
        json.dumps(topics, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{pdf.name}: {len(topics)} topics ({source})")
    for t in topics:
        print(f"   p{t['start_page']}-{t['end_page']}  {t['title']}")
    if missing:
        print(f"   ONYO: sura hazijapatikana: {missing}")
