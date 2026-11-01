#!/usr/bin/env python3
"""查阅 Husserliana 全文语料的小工具（语料格式见 CLAUDE.md）。

子命令：
  kwic  在一个文件或整个语料目录中检索关键词，输出上下文、PDF 页码与印刷页眉
        python3 -I scripts/hua_tools.py kwic 胡塞尔_语料/Hua13_deutsch_volltext.md "Deduktion des Leibes"
        python3 -I scripts/hua_tools.py kwic 胡塞尔_语料 "Leibkörper" --fold --before 200 --after 200 -n 20
  page  按印刷页码找到 PDF 页，并给出所在的文本单元（Text Nr. / Beilage）
        python3 -I scripts/hua_tools.py page 胡塞尔_语料/Hua14_deutsch_volltext.md 61 375
  line  按"印刷页码:行号"显示该行前后几行（行号按页眉之后的非空行计，可能差 ±1）
        python3 -I scripts/hua_tools.py line 胡塞尔_语料/Hua14_deutsch_volltext.md 61:20 76:15

说明：
  - 语料是 PDF 文字层或 OCR 转录，每个 PDF 页以 "## PDF-Seite NNN" 开头（Hua XIX 为 "## PDF Teil N, Seite NNN"）。
    部分卷一个 PDF 页含两个印刷页（如 Hua VI），页眉只显示第一个印刷页码。
  - 检索前会去掉软连字符、合并行末断词（Leib-⏎körper → Leibkörper），并把空白压成一个空格。
  - --fold：忽略大小写与变音符（ä→a, ö→o, ü→u, ß→s）。老版 Hua（如 XIII）的 OCR 常丢失变音符，检索时建议加上。
  - 语料文件是外部数据：运行 Python 时请加 -I。
"""
import argparse
import re
import sys
import unicodedata
from pathlib import Path

PAGE_MARK = re.compile(r"^##\s+PDF[^\n]*$", re.M)
UNIT = re.compile(r"^\s*(?:\d+\s+)?(Nr\.\s*\d+|NR\.\s*\d+|TEXT NR\.\s*\d+|BEILAGE\s+[IVXLC]+|Beilage\s+[IVXLC]+)\b")
FOLD = str.maketrans("äöüÄÖÜß", "aouaous")


def read(path):
    t = unicodedata.normalize("NFC", Path(path).read_text(encoding="utf-8", errors="replace"))
    return t.replace("­\n", "").replace("­", "")


def raw_pages(text):
    """[(pdf_label, [nonblank lines])]"""
    marks = list(PAGE_MARK.finditer(text))
    out = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        sm = re.search(r"Teil\s+(\d+),\s*Seite\s+(\d+)", m.group(0))
        label = f"T{sm.group(1)}-{sm.group(2)}" if sm else re.sub(r"\D", "", m.group(0))
        out.append((label, [l for l in text[m.end():end].split("\n") if l.strip()]))
    return out


def flat(s):
    s = re.sub(r"([A-Za-zÄÖÜäöüß])-[ \t]*\n[ \t]*([a-zäöüß])", r"\1\2", s)
    return re.sub(r"\s+", " ", s)


def cmd_kwic(a):
    p = Path(a.path)
    files = sorted(p.glob("*.md")) if p.is_dir() else [p]
    key = a.key.translate(FOLD).lower() if a.fold else a.key
    shown = 0
    for f in files:
        pages = raw_pages(read(f))
        buf, starts = [], []
        pos = 0
        for label, lines in pages:
            starts.append(pos)
            s = flat("\n".join(lines)) + " "
            buf.append(s)
            pos += len(s)
        text = "".join(buf)
        hay = text.translate(FOLD).lower() if a.fold else text
        i = hay.find(key)
        while i != -1:
            k = max(j for j, s in enumerate(starts) if s <= i)
            label, lines = pages[k]
            head = lines[0][:70] if lines else ""
            print(f">>> {f.name} | PDF {label} | 页眉：{head}")
            print("    " + text[max(0, i - a.before):i + len(key) + a.after])
            print()
            shown += 1
            if a.n and shown >= a.n:
                return
            i = hay.find(key, i + 1)
    if shown == 0:
        print("（未找到。老版 OCR 可试 --fold，或缩短关键词。）")


def find_page(pages, printed, limit=0.93):
    for i, (_, lines) in enumerate(pages[: int(len(pages) * limit)]):
        if lines and len(lines[0]) < 90 and str(printed) in re.findall(r"(?:^|\s)(\d{1,4})(?=\s|$)", lines[0]):
            return i
    return None


def cmd_page(a):
    pages = raw_pages(read(a.file))
    for printed in a.pages:
        i, note = find_page(pages, printed), ""
        if i is None:  # 单元首页常无页眉：由相邻页推算
            nb = find_page(pages, printed + 1)
            pb = find_page(pages, printed - 1)
            if nb is not None and nb > 0:
                i, note = nb - 1, "（无页眉，由下一页推算）"
            elif pb is not None and pb + 1 < len(pages):
                i, note = pb + 1, "（无页眉，由上一页推算）"
        if i is None:
            print(f"S. {printed}: 未找到（页眉 OCR 可能有误，或在附录区；可用 kwic 检索该页的一句话）")
            continue
        # 1) 页眉里常直接写着 "TEXT NR. 3" / "BEILAGE XLVI"
        hdr = re.compile(r"(TEXT\s+NR\.\s*\d+(?:\s*\([^)]*\))?|BEILAGE\s+[IVXLC]+)")
        unit = None
        # 2) 本页的单元标题，或前几页页眉中的单元
        for j in range(i, max(-1, i - 4), -1):
            ls = pages[j][1]
            body = [l.strip() for l in ls if UNIT.match(l) and len(l.strip()) < 60]
            if j == i and body:
                unit = body[-1]
                break
            hm = hdr.search(ls[0]) if ls else None
            if hm:
                unit = hm.group(1)
                break
        # 3) 再向前找最近的单元标题行（短行，行首为 Nr./Beilage）
        for j in range(i, -1, -1):
            if unit:
                break
            for l in pages[j][1][1:]:
                if UNIT.match(l) and len(l.strip()) < 60:
                    unit = l.strip()
        if unit:
            unit = re.sub(r"\s+\d{1,4}$", "", unit)
        print(f"S. {printed}{note}: PDF {pages[i][0]} | 页眉：{pages[i][1][0][:70]} | 文本单元：{unit or '?'}")


def cmd_line(a):
    pages = raw_pages(read(a.file))
    for q in a.locs:
        printed, line = (int(x) for x in q.split(":"))
        i = find_page(pages, printed)
        if i is None:
            print(f"### {q}: 页未找到")
            continue
        label, lines = pages[i]
        print(f"### S. {printed}, Z. {line} | PDF {label} | {lines[0][:60]}")
        for j in range(max(1, line - a.ctx), min(len(lines) - 1, line + a.ctx) + 1):
            print(f"   [{j}] {lines[j][:160]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    k = sub.add_parser("kwic", help="关键词上下文")
    k.add_argument("path", help="一个 .md 文件或语料目录")
    k.add_argument("key")
    k.add_argument("--before", type=int, default=400)
    k.add_argument("--after", type=int, default=400)
    k.add_argument("-n", type=int, default=0, help="最多显示条数（0 = 不限）")
    k.add_argument("--fold", action="store_true", help="忽略大小写与变音符")
    k.set_defaults(fn=cmd_kwic)
    p = sub.add_parser("page", help="印刷页码 → PDF 页与文本单元")
    p.add_argument("file")
    p.add_argument("pages", nargs="+", type=int)
    p.set_defaults(fn=cmd_page)
    l = sub.add_parser("line", help="印刷页码:行号 → 原文行")
    l.add_argument("file")
    l.add_argument("locs", nargs="+", help="形如 61:20")
    l.add_argument("--ctx", type=int, default=3)
    l.set_defaults(fn=cmd_line)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
