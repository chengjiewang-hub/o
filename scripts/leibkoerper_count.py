#!/usr/bin/env python3
"""Count Leibkörper and related expressions across the Husserl Markdown corpus.

Usage: python3 -I leibkoerper_count.py <corpus_dir> <out_dir>

Corpus files are the *_volltext.md transcriptions (pages marked by "## ... Seite N").
Scope (same as hua345_Leibkoerper_词频统计.md):
  A. Compound words containing both a Leib and a Körper stem
     (Körper/Koerper/Korper and OCR "K6rper"; hyphenated forms included).
  B. Two-word phrase structures (körperlicher Leib, Leib als Körper, ...).
  C. Reference only, not part of totals: "Leib und Körper" / "Körper und Leib".
"""
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

# file -> (volume label, edition note, language, include in main German total)
VOLUMES = {
    "hua1_volltext.md": ("Hua I", "Cartesianische Meditationen (1950)", "de", True),
    "hua2_volltext.md": ("Hua II", "Die Idee der Phänomenologie (1950)", "de", True),
    "hua4_deutsch_ocr_volltext.md": ("Hua IV", "Ideen II (1952, Biemel)", "de", True),
    "hua4_neu_deutsch_volltext.md": ("Hua IV/V neu", "Ideen II/III Neuedition (Fonfara)", "de", False),
    "hua5_volltext.md": ("Hua V", "Ideen III (1952)", "de", True),
    "hua6_deutsch_volltext.md": ("Hua VI", "Krisis", "de", True),
    "hua7_volltext.md": ("Hua VII", "Erste Philosophie I", "de", True),
    "hua8_volltext.md": ("Hua VIII", "Erste Philosophie II", "de", True),
    "Hua9_deutsch_volltext.md": ("Hua IX", "Phänomenologische Psychologie", "de", True),
    "hua10_volltext.md": ("Hua X*", "Zeitbewußtsein (Meiner PhB-Ausgabe, Bernet)", "de", True),
    "hua11_deutsch_volltext.md": ("Hua XI", "Analysen zur passiven Synthesis", "de", True),
    "hua12_volltext.md": ("Hua XII", "Philosophie der Arithmetik", "de", True),
    "Hua13_deutsch_volltext.md": ("Hua XIII", "Intersubjektivität I", "de", True),
    "Hua14_deutsch_volltext.md": ("Hua XIV", "Intersubjektivität II", "de", True),
    "Hua15_deutsch_volltext.md": ("Hua XV", "Intersubjektivität III", "de", True),
    "hua16_deutsch_volltext.md": ("Hua XVI", "Ding und Raum", "de", True),
    "hua17_deutsch_volltext.md": ("Hua XVII", "Formale und transzendentale Logik", "de", True),
    "hua18_volltext.md": ("Hua XVIII", "Logische Untersuchungen I", "de", True),
    "hua19_volltext.md": ("Hua XIX", "Logische Untersuchungen II", "de", True),
    "hua21_volltext.md": ("Hua XXI", "Studien zur Arithmetik und Geometrie", "de", True),
    "hua22_volltext.md": ("Hua XXII", "Aufsätze und Rezensionen 1890–1910", "de", True),
    "hua23_volltext.md": ("Hua XXIII", "Phantasie, Bildbewusstsein, Erinnerung", "de", True),
    "hua24_volltext.md": ("Hua XXIV", "Einleitung in die Logik und Erkenntnistheorie", "de", True),
    "hua25_volltext.md": ("Hua XXV", "Aufsätze und Vorträge 1911–1921", "de", True),
    "hua26_volltext.md": ("Hua XXVI", "Vorlesungen über Bedeutungslehre", "de", True),
    "hua27_deutsch_volltext.md": ("Hua XXVII", "Aufsätze und Vorträge 1922–1937", "de", True),
    "hua28_volltext.md": ("Hua XXVIII", "Vorlesungen über Ethik und Wertlehre", "de", True),
    "hua33_volltext.md": ("Hua XXXIII", "Bernauer Manuskripte", "de", True),
    "hua34_volltext.md": ("Hua XXXIV", "Zur phänomenologischen Reduktion", "de", True),
    "hua39_volltext.md": ("Hua XXXIX", "Die Lebenswelt", "de", True),
    "hua42_volltext.md": ("Hua XLII", "Grenzprobleme der Phänomenologie", "de", True),
    "mat8_volltext.md": ("Mat VIII", "Späte Texte über Zeitkonstitution (C-Mss.)", "de", True),
    "D_Manuskripte_volltext.md": ("Mat XI", "Manuskripte zur Konstitution von Raumdingen (D-Mss.)", "de", True),
    # English translations: German-term search does not apply; listed for completeness.
    "hua3_volltext.md": ("CW III (en)", "Ideas II, engl. Übers. (Rojcewicz/Schuwer)", "en", False),
    "hua6_englisch_volltext.md": ("Crisis (en)", "Krisis, engl. Übers. (Carr)", "en", False),
    "hua11_englisch_volltext.md": ("CW IX (en)", "Passive Synthesis, engl. Übers.", "en", False),
    "hua16_englisch_volltext.md": ("CW VII (en)", "Thing and Space, engl. Übers.", "en", False),
    "hua17_englisch_volltext.md": ("FTL (en)", "Formal and Transcendental Logic, engl. Übers.", "en", False),
}

PAGE_RE = re.compile(r"^##\s+PDF[^\n]*?Seite\s+(\d+)", re.M)
PART_RE = re.compile(r"^##\s+PDF\s+Teil\s+(\d+),\s*Seite\s+(\d+)", re.M)

K = r"k(?:ö|oe|o|6|ä)rper"  # Körper incl. OCR variants (ö→o, ö→6, ö→ä)
KC = r"[kK](?:ö|oe|o|6|ä)rper"
WORD = r"[A-Za-zÄÖÜäöüß0-9]+"
TOKEN_RE = re.compile(r"[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß0-9]*(?:-[A-Za-zÄÖÜäöüß0-9]+)*")


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = text.replace("­\n", "").replace("­", "")
    text = text.replace("¬\n", "")
    # line-break hyphenation: "Leib-\nkörper" -> "Leibkörper" (lowercase continuation only)
    text = re.sub(r"([A-Za-zÄÖÜäöüß])-[ \t]*\n[ \t]*([a-zäöüß])", r"\1\2", text)
    return text


def split_pages(text: str):
    """Yield (page_label, page_text)."""
    marks = []
    for m in re.finditer(r"^##\s+PDF[^\n]*$", text, re.M):
        line = m.group(0)
        pm = PART_RE.match(line)
        if pm:
            label = f"T{pm.group(1)}-{int(pm.group(2)):03d}"
        else:
            sm = re.search(r"Seite\s+(\d+)", line)
            label = f"{int(sm.group(1)):03d}" if sm else line
        marks.append((m.start(), m.end(), label))
    if not marks:
        yield ("?", text)
        return
    for i, (s, e, label) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        yield (label, text[e:end])


def kfold(s: str) -> str:
    return re.sub(K, "körper", s.lower())


def classify_compound(tok: str):
    t = kfold(tok)
    if "leib" not in t or "körper" not in t:
        return None
    if re.search(r"leibe?s-?körper", t):
        return "Leibeskörper 词族"
    if re.search(r"leib-?körper", t):
        return "狭义 Leibkörper 词族"
    if re.search(r"körper-?leib", t):
        return "Körperleib 词族"
    if re.search(r"leiblich\w*-?körperlich|körperlich\w*-?leiblich", t):
        return "leiblich-körperlich 型并列形容词"
    return "其他双词干复合词"


ADJ = r"(?:körperlich|korperlich|k6rperlich|koerperlich)(?:e|en|er|em|es)?"
LEIB_N = r"Leib(?:e|es|s|er|ern)?\b"
PHRASES = [
    ("körperlich + Leib", re.compile(
        rf"\b(?:materiell-)?{ADJ}\s+(?:(?:{WORD})\s+){{0,1}}?{LEIB_N}")),
    ("körperlich + Leiblichkeit", re.compile(rf"\b{ADJ}\s+Leiblichkeit\b")),
    ("Körperding Leib", re.compile(rf"\b{KC}ding\s+Leib\b")),
    ("Leib … als (…) Körper", re.compile(
        rf"\b{LEIB_N}(?:\s+{WORD}){{0,3}}?\s+als\s+(?:(?:ein|eine|einen|einem|einer|der|den|dem|des|bloßen?|bloßer|materiellen?|materieller|physischen?|physischer|Null)\s*)*{KC}s?\b|\b{LEIB_N}\s+als\s+Null{K}\b",
        re.I if False else 0)),
    ("Körper, der (…) Leib ist", re.compile(
        rf"\b{KC}s?,?\s+(?:der|welcher)\s+(?:{WORD}\s+){{0,2}}Leib\s+ist\b")),
    ("Leib … wie (ein anderer) Körper", re.compile(
        rf"\b{LEIB_N}(?:\s+{WORD}){{0,3}}?\s+wie\s+(?:ein|jeder|andere|anderer|ein\s+anderer|sonst\s+ein)?\s*{KC}\b")),
    ("Leib, d.i. … Körper", re.compile(
        rf"\b{LEIB_N},?\s+(?:d\.\s?i\.|d\.\s?h\.|das\s+ist|nämlich)\s+(?:{WORD},?\s+){{0,3}}{KC}\b")),
]
REFERENCE = [
    ("Leib und Körper", re.compile(rf"\bLeib(?:e|es|s)?\s+und\s+{KC}s?\b")),
    ("Körper und Leib", re.compile(rf"\b{KC}s?\s+und\s+Leib(?:e|es|s)?\b")),
]


def ctx(s: str, a: int, b: int, w: int = 90) -> str:
    return re.sub(r"\s+", " ", s[max(0, a - w):b + w]).strip()


def main(corpus: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    hits = []
    words = {}
    for fname, (vol, title, lang, main_total) in VOLUMES.items():
        path = corpus / fname
        if not path.exists():
            print("missing", fname, file=sys.stderr)
            continue
        text = normalize(path.read_text(encoding="utf-8", errors="replace"))
        nwords = 0
        for page, ptxt in split_pages(text):
            nwords += len(TOKEN_RE.findall(ptxt))
            # A: compounds
            for m in TOKEN_RE.finditer(ptxt):
                tok = m.group(0)
                cat = classify_compound(tok)
                if cat:
                    hits.append(dict(file=fname, vol=vol, lang=lang, page=page, kind="compound",
                                     cat=cat, form=tok, context=ctx(ptxt, m.start(), m.end())))
            # A': OCR-split compound "Leib körper" (lowercase k)
            for m in re.finditer(rf"\bLeib\s+(k(?:ö|o|6|oe)rper(?:s|n)?)\b", ptxt):
                hits.append(dict(file=fname, vol=vol, lang=lang, page=page, kind="compound",
                                 cat="狭义 Leibkörper 词族", form=f"Leib {m.group(1)} [OCR拆词]",
                                 context=ctx(ptxt, m.start(), m.end())))
            # B: phrases (no overlapping double count within a page)
            taken = []
            for cat, rx in PHRASES:
                for m in rx.finditer(ptxt):
                    if any(m.start() < e and s < m.end() for s, e in taken):
                        continue
                    # skip if the Körper part is itself already a Leibkörper compound
                    if re.search(r"Leib\w*" + K, m.group(0), re.I):
                        continue
                    # negated identity ("Körper, der kein/noch nicht Leib ist") is a contrast, not a Leib-Körper structure
                    if cat.startswith("Körper, der") and re.search(r"\b(kein|nicht)\b", m.group(0)):
                        continue
                    taken.append((m.start(), m.end()))
                    hits.append(dict(file=fname, vol=vol, lang=lang, page=page, kind="phrase",
                                     cat=cat, form=re.sub(r"\s+", " ", m.group(0)),
                                     context=ctx(ptxt, m.start(), m.end())))
            for cat, rx in REFERENCE:
                for m in rx.finditer(ptxt):
                    hits.append(dict(file=fname, vol=vol, lang=lang, page=page, kind="reference",
                                     cat=cat, form=re.sub(r"\s+", " ", m.group(0)),
                                     context=ctx(ptxt, m.start(), m.end())))
        words[fname] = nwords
    (out / "hits.json").write_text(json.dumps(dict(words=words, hits=hits), ensure_ascii=False, indent=1),
                                   encoding="utf-8")
    c = Counter((h["vol"], h["kind"]) for h in hits)
    for fname, (vol, *_rest) in VOLUMES.items():
        print(f"{vol:14s} words={words.get(fname, 0):>8} compound={c[(vol,'compound')]:>4} "
              f"phrase={c[(vol,'phrase')]:>4} ref={c[(vol,'reference')]:>4}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
