#!/usr/bin/env python3
"""Find every editorial / text-critical record that involves Leibkörper and related expressions.

Usage: python3 -I leibkoerper_apparatus.py <corpus_dir> <out.json>

Searches, in every German file registered in leibkoerper_count.VOLUMES:
  A. text-critical apparatus at the end of a volume ("Textkritische Anmerkungen/Anhang"):
     entries start with a locator "S,Z" (e.g. "164, 21", "6,1", "305, Anm. 1") and are
     separated by "||" (OCR also "11", "II", "|").
  B. footnote apparatus on the text pages (Fink, Hua Dokumente II/1–2): "81 (Rb.) ...",
     "(V.) ...", "(Einf.) ...".
  C. editor's brackets in the text: <...>, ⟨...⟩, 〈...〉 containing the expression.
Every candidate is printed with the full entry for manual classification.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from leibkoerper_count import VOLUMES, PHRASES, TOKEN_RE, classify_compound  # noqa: E402

LOC = re.compile(r"(?<![\d,.])(\d{1,3})\s*,\s*(?:(\d{1,2})|Anm\.\s*\d)(?:\s*[-–]\s*\d{1,3}(?:\s*,\s*\d{1,2})?)?(?:\s*f{1,2}\.?)?(?![\d])")
SEP = re.compile(r"\s(?:\|\||\|\s?\||11|II|Il|lI|1I|I1|\|)\s")
FN = re.compile(r"(?:(?<!\S)|(?<=[.•·]))(\d{1,3})\s*[(<〈⟨{]\s*(Rb|V|Einf|Erg|F|Zusatz|gestr)\.?[^\s]{0,2}")
KW = re.compile(r"Einf|V\.\s*(?:mit|f|m\.)|V\.\s|gestr|Rb\.|Bleist|Blaust|Rotst|Tinte|Ms\.|statt|Erg\.|eingefügt|eingefiigt|Zusatz|Kl\.|Klammer|Anführungszeichen|Anfiihrungszeichen|unterstr|ausradiert|überschrieben|iiberschrieben|Randbemerkung|Randtitel|Hrsg\.|lautet|ursprünglich|urspriinglich")
BRACKET = re.compile(r"[<⟨〈‹]([^<>⟨⟩〈〉‹›]{0,260})[>⟩〉›]")
APP_HEAD = re.compile(r"TEXTKRITISCH|ANMERKUNGEN ZU|ZUR TEXTGESTALTUNG", re.I)


def flatten(s):
    s = unicodedata.normalize("NFC", s).replace("­\n", "").replace("­", "")
    s = re.sub(r"([A-Za-zÄÖÜäöüß])-[ \t]*\n[ \t]*([a-zäöüß])", r"\1\2", s)
    return re.sub(r"\s+", " ", s)


def pages(text):
    marks = list(re.finditer(r"^##\s+PDF[^\n]*$", text, re.M))
    for i, m in enumerate(marks):
        sm = re.search(r"Teil\s+(\d+),\s*Seite\s+(\d+)", m.group(0))
        label = f"T{sm.group(1)}-{int(sm.group(2)):03d}" if sm else f"{int(re.search(r'Seite\s+(\d+)', m.group(0)).group(1)):03d}"
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        raw = text[m.end():end]
        lines = [l for l in raw.split("\n") if l.strip()]
        yield label, (lines[0] if lines else ""), flatten(raw)


def targets(flat):
    for m in TOKEN_RE.finditer(flat):
        cat = classify_compound(m.group(0))
        if cat:
            yield m.start(), m.end(), "compound", cat, m.group(0)
    for cat, rx in PHRASES:
        for m in rx.finditer(flat):
            if re.search(r"Leib\w*k(?:ö|oe|o|6|ä)rper", m.group(0), re.I):
                continue
            yield m.start(), m.end(), "phrase", cat, m.group(0)


def apparatus_start(page_list):
    """Index of the first page of the end-of-volume apparatus (None if absent)."""
    n = len(page_list)
    for i, (_, header, flat) in enumerate(page_list):
        if i < n * 0.45:
            continue
        if APP_HEAD.search(header) or re.search(r"(?:^|\s)(TEXTKRITISCHE ANMERKUNGEN|TEXTKRITISCHER ANHANG)(?:\s|$)", flat[:300]):
            return i
    return None


def main(corpus: Path, out: Path):
    cands = []
    for fname, (vol, title, lang, _) in VOLUMES.items():
        if lang != "de" or not (corpus / fname).exists():
            continue
        plist = list(pages((corpus / fname).read_text(encoding="utf-8", errors="replace")))
        a0 = apparatus_start(plist)
        for idx, (label, header, flat) in enumerate(plist):
            in_app = (a0 is not None and idx >= a0) or bool(APP_HEAD.search(header))
            for s, e, kind, cat, form in targets(flat):
                rec = dict(vol=vol, file=fname, pdf=label, header=header[:80], kind=kind, cat=cat, form=form)
                # A: end-of-volume apparatus entry
                if in_app:
                    back = flat[max(0, s - 1500):s]
                    locs = list(LOC.finditer(back))
                    seps = list(SEP.finditer(back))
                    start_rel = None
                    if locs:
                        start_rel = locs[-1].start()
                    if seps and (start_rel is None or seps[-1].end() > start_rel):
                        start_rel = seps[-1].end()
                    if start_rel is None:
                        start_rel = max(0, len(back) - 400)
                    entry_start = max(0, s - 1500) + start_rel
                    fwd = flat[e:e + 900]
                    nxt = [m.start() for m in SEP.finditer(fwd)][:1] + [m.start() for m in LOC.finditer(fwd) if m.start() > 3][:1]
                    entry_end = e + (min(nxt) if nxt else 400)
                    entry = flat[entry_start:entry_end].strip()
                    rec.update(where="A 校勘附录", entry=entry, has_kw=bool(KW.search(entry)))
                    cands.append(rec)
                    continue
                # B: footnote apparatus on a text page
                back = flat[max(0, s - 700):s]
                fns = list(FN.finditer(back))
                if fns:
                    fs = max(0, s - 700) + fns[-1].start()
                    between = flat[fs:s]
                    # stop if a later footnote marker or a long stretch of running text intervenes
                    if len(between) < 650:
                        fwd = flat[e:e + 500]
                        nf = FN.search(fwd)
                        entry = flat[fs:e + (nf.start() if nf else 300)].strip()
                        rec.update(where="B 页下异文注", entry=entry, has_kw=True)
                        cands.append(rec)
                        continue
                # C: editor's brackets in the running text
                for bm in BRACKET.finditer(flat[max(0, s - 270):e + 270]):
                    bs = max(0, s - 270) + bm.start()
                    be = max(0, s - 270) + bm.end()
                    if bs <= s and e <= be:
                        rec.update(where="C 编者括号", entry=flat[max(0, bs - 120):be + 120].strip(), has_kw=False)
                        cands.append(rec)
                        break
    out.write_text(json.dumps(cands, ensure_ascii=False, indent=1), encoding="utf-8")
    from collections import Counter
    print(len(cands), Counter((c["vol"], c["where"]) for c in cands).most_common())


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
