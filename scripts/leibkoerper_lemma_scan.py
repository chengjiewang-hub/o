#!/usr/bin/env python3
"""反向检索校勘附录中涉及 Leib / Körper 的改动条目（用于补充 leibkoerper_apparatus.py）。

leibkoerper_apparatus.py 从正文中的目标表达出发去找校勘记录；本脚本反过来，
从校勘附录的条目格式出发（"页,行 词 Einf./Erg./V./gestr." 与 "页,行 … V. für 词"），
找出所有词条中含 Leib / Körper / körperlich 词干的记录，例如 "Leib V. für Körper"。
结果需人工核对（见 胡塞尔_统计/Leibkoerper_改稿与编辑记录.md）。

用法：python3 -I scripts/leibkoerper_lemma_scan.py 胡塞尔_语料 <out.json>
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from leibkoerper_apparatus import pages, apparatus_start, LOC
from leibkoerper_count import VOLUMES
corpus = sys.argv[1]
K = r"[Kk](?:ö|oe|o|6|ä)rper"
W = rf"(?:Leib\w*-?|leib\w*|{K}\w*|k(?:ö|o|6)rperlich\w*)"
P1 = re.compile(rf"(?<![\d,])(\d{{1,3}})\s*,\s*(\d{{1,2}})(?:\s*[-–]\s*\d{{1,2}})?\s+((?:\S+\s+){{0,2}}?{W}(?:\s+\S+){{0,2}}?)\s+(Einf|Erg|V\.|Bleistiftv|Bleist\.-\s*V|gestr|eingefügt)")
P2 = re.compile(rf"(?<![\d,])(\d{{1,3}})\s*,\s*(\d{{1,2}})(?:\s*[-–]\s*\d{{1,2}})?\s+([^|]{{1,60}}?)\s+(?:V\.|Bleistiftv\.|Bleist\.-\s*V\.|Änderung)\s*(?:(?:m|mit)\.?\s*\w+\.?\s*)?(?:in\s+\w+\s+)?f(?:ü|ii|u)r\s+((?:\S+\s+){{0,2}}?{W})")
out = []
for fname, (vol, title, lang, _) in VOLUMES.items():
    if lang != 'de':
        continue
    try:
        txt = open(f"{corpus}/{fname}", encoding='utf-8', errors='replace').read()
    except FileNotFoundError:
        continue
    pl = list(pages(txt)); a0 = apparatus_start(pl)
    if a0 is None:
        continue
    for label, header, flat in pl[a0:]:
        for rx, kind in ((P1, 'lemma'), (P2, 'für')):
            for m in rx.finditer(flat):
                out.append(dict(vol=vol, file=fname, pdf=label, header=header[:50], kind=kind, loc=f"{m.group(1)},{m.group(2)}", entry=flat[m.start():m.end()+80]))
seen=set(); res=[]
for o in out:
    k=(o['vol'],o['loc'],o['entry'][:40])
    if k in seen: continue
    seen.add(k); res.append(o)
json.dump(res, open(sys.argv[2],'w'), ensure_ascii=False, indent=1)
for o in res: print(o['vol'], o['pdf'], o['loc'], '|', o['entry'][:150])
print(len(res))
