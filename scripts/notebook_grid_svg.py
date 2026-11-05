#!/usr/bin/env python3
"""Generate the two-axis / four-cell diagram for notebook entries 2 and 4."""
import sys
from xml.sax.saxutils import escape

OUT = sys.argv[1]

W, H = 1240, 1090
X0, Y0 = 150, 150          # grid origin
CW, CH = 520, 390          # cell width / height
XM, YM = X0 + CW, Y0 + CH  # grid midlines
X1, Y1 = X0 + 2 * CW, Y0 + 2 * CH

FONT = "'PingFang SC','Noto Sans CJK SC','Source Han Sans SC','Microsoft YaHei','WenQuanYi Zen Hei',sans-serif"

KIND = {  # fill, stroke, text
    "h": ("#e8f0fb", "#3b6fb6", "#1d3f6e"),   # Husserl texts
    "p": ("#fcefe6", "#c0672b", "#6e3510"),   # other philosophers
    "s": ("#e9f5ec", "#3d8b55", "#1f5130"),   # secondary literature
}

CELL_BG = {"A": "#fafafa", "B": "#f6f6f6", "C": "#f6f6f6", "D": "#fafafa"}


def tw(s, size):
    """rough text width estimate"""
    w = 0
    for ch in s:
        w += size * (1.0 if ord(ch) > 0x2E80 else 0.56)
    return w


def wrap(s, size, maxw):
    import re
    toks = re.findall(r"[A-Za-zÄÖÜäöüß0-9.]+|\s|.", s)
    lines, cur = [], ""
    for tok in toks:
        if tw(cur + tok, size) > maxw and cur.strip():
            lines.append(cur.rstrip())
            cur = tok.lstrip()
        else:
            cur += tok
    if cur.strip():
        lines.append(cur)
    return lines


out = []
A = out.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">')
A('<defs>'
  '<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
  '<path d="M0,0 L10,5 L0,10 z" fill="#555"/></marker>'
  '</defs>')
A(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>')

# title
A(f'<text x="{W/2}" y="42" text-anchor="middle" font-size="24" font-weight="700" fill="#222">“先验”的两轴四格：身体与构造者的定位</text>')
A(f'<text x="{W/2}" y="68" text-anchor="middle" font-size="13" fill="#666">笔记本第 2、4 条 · 条件角色（“X 是 Y 的可能性条件”）在四格中都能成立，格子说明的是方法与地位</text>')

# column headers
for i, (t1, t2) in enumerate([("不经悬搁", "世界有效性保持：回溯论证，或在世界信念下描述"),
                              ("经悬搁", "世界有效性中止：在反思中展示（aufweisbar）")]):
    cx = X0 + CW * i + CW / 2
    A(f'<text x="{cx}" y="{Y0-30}" text-anchor="middle" font-size="18" font-weight="700" fill="#333">{t1}</text>')
    A(f'<text x="{cx}" y="{Y0-11}" text-anchor="middle" font-size="12" fill="#666">{escape(t2)}</text>')
A(f'<text x="{X1}" y="{Y0-58}" text-anchor="end" font-size="12" fill="#999">方法轴 →</text>')

# row headers (rotated)
for i, (t1, t2) in enumerate([("世间的", "（悬搁后：被构造的，属于“现象”）"),
                              ("非世间的", "（构造者 / 运作者一侧）")]):
    cy = Y0 + CH * i + CH / 2
    A(f'<text transform="translate({X0-58},{cy}) rotate(-90)" text-anchor="middle" font-size="18" font-weight="700" fill="#333">{t1}</text>')
    A(f'<text transform="translate({X0-38},{cy}) rotate(-90)" text-anchor="middle" font-size="12" fill="#666">{escape(t2)}</text>')
A(f'<text transform="translate({X0-100},{Y0+CH}) rotate(-90)" text-anchor="middle" font-size="12" fill="#999">地位轴 →</text>')

# cells
cells = {"A": (X0, Y0), "C": (XM, Y0), "B": (X0, YM), "D": (XM, YM)}
titles = {"A": "A  经验性条件", "C": "C  被构造的条件", "B": "B  回溯推出的先验主体", "D": "D  运作着的构造者"}
levels = {"A": "层面 ①", "C": "层面 ②", "B": "胡塞尔三层中无此格", "D": "层面 ③"}
for k, (x, y) in cells.items():
    A(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="{CELL_BG[k]}" stroke="#bbb" stroke-width="1.5"/>')
    ty = y + (28 if k in "AC" else 58)
    tx = x + (48 if k in "AB" else 14)
    A(f'<text x="{tx}" y="{ty}" font-size="17" font-weight="700" fill="#222">{escape(titles[k])}</text>')
    lx_ = x + CW - (14 if k in "AB" else 90)
    A(f'<text x="{lx_}" y="{ty}" text-anchor="end" font-size="12" fill="#888">{escape(levels[k])}</text>')
A(f'<rect x="{X0}" y="{Y0}" width="{2*CW}" height="{2*CH}" fill="none" stroke="#888" stroke-width="2"/>')


def chip(x, y, w, name, sub, kind, dashed=False):
    fill, stroke, col = KIND[kind]
    nl = wrap(name, 13, w - 16)
    sl = wrap(sub, 11.5, w - 16) if sub else []
    h = 10 + 17 * len(nl) + 15 * len(sl) + 6
    da = ' stroke-dasharray="5,3"' if dashed else ""
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="1.4"{da}/>')
    ty = y + 22
    for l in nl:
        A(f'<text x="{x+8}" y="{ty}" font-size="13" font-weight="700" fill="{col}">{escape(l)}</text>')
        ty += 17
    for l in sl:
        A(f'<text x="{x+8}" y="{ty-1}" font-size="11.5" fill="#444">{escape(l)}</text>')
        ty += 15
    return h


def column(x, y, w, items, gap=9):
    for it in items:
        h = chip(x, y, w, *it)
        y += h + gap
    return y


# --- A (top-left): chips area x 205..645
cw2 = 212
column(X0 + 52, Y0 + 44, cw2, [
    ("胡塞尔 1925", "Hua XIV 375：身体是“经验性的可能性条件”；“我的身体躯体……物理关系”", "h"),
    ("胡塞尔：心理学现象学", "Hua IX；《危机》§72 与 D 平行的“先验心理学”", "h"),
])
column(X0 + 52 + cw2 + 10, Y0 + 44, cw2, [
    ("康德（身体）", "身体只是经验对象", "p"),
    ("Strawson · Stroud", "分析哲学的“先验论证”：有身体的个人是指称的条件", "p", True),
    ("Sandu 2018", "身体是条件，但进不了 C、也进不了 D", "s"),
])

# --- B (bottom-left)
column(X0 + 52, YM + 92, cw2, [
    ("康德：先验统觉", "KrV B 135：“不包含任何杂多”；靠演绎回溯推出", "p"),
])
column(X0 + 52 + cw2 + 10, YM + 92, cw2, [
    ("Natorp（新康德主义）", "纯粹自我不可对象化，只能“重构”", "p", True),
])
A(f'<text x="{X0+52}" y="{Y1-40}" font-size="12" fill="#777">胡塞尔的批评：康德的“bloß regressive Methode”</text>')
A(f'<text x="{X0+52}" y="{Y1-22}" font-size="12" fill="#777">导致“mythische Begriffsbildung”（《危机》§28、§30）</text>')

# --- C (top-right): chips area x 672..1082
rx = XM + 12
cw3 = 200
column(rx, Y0 + 44, cw3, [
    ("胡塞尔：《观念 II》引线方法", "被构造的身体作为分析的引线", "h"),
    ("胡塞尔 1915–17", "Hua XIII 375 “身体的先验演绎”：位置在 C，论证是 B 式的", "h"),
    ("胡塞尔 1927", "Hua XIV 547：身体躯体只是“事实上”必然", "h"),
])
column(rx + cw3 + 10, Y0 + 44, cw3, [
    ("《危机》§54（1936）", "身体与人“属于'现象'”", "h"),
    ("Carman 1999", "对胡塞尔的解读：身体只在 C，D 中无身体（批评）", "s"),
])

# --- D (bottom-right)
column(rx, YM + 92, cw3, [
    ("《危机》§54（1936）", "原自我：自我极、习性、能力", "h"),
    ("胡塞尔 1921/22", "Hua XIV 61：对身体的 somatologische Wahrnehmung 是“自在的第一者”", "h"),
    ("胡塞尔 1927", "Hua XIV 547：动觉", "h"),
    ("Fink", "现象学旁观者；在 A/C 中只是“非本真的世间化”", "p"),
])
column(rx + cw3 + 10, YM + 92, cw3, [
    ("胡塞尔 1931", "Hua XV 385 f.：“我是原事实”；质素的原事实", "h"),
    ("胡塞尔 1932 年夏", "Hua Dok II/2 151 页边注：“但也包括身体躯体！”", "h"),
    ("Zahavi 1994", "有身体的先验主体性？", "s", True),
    ("Heinämaa 等 2014", "身体同时在 A/C 与 D（“一枚硬币的两面”）", "s"),
])

# --- arrows in the right margin of the right column
ax1, ax2 = X1 - 64, X1 - 26
A(f'<line x1="{ax1}" y1="{Y1-40}" x2="{ax1}" y2="{Y0+70}" stroke="#555" stroke-width="2.4" marker-end="url(#ah)"/>')
A(f'<text transform="translate({ax1-9},{YM}) rotate(-90)" text-anchor="middle" font-size="12" fill="#333">自我客体化 D→C：Hua XV 300（1931）·《危机》§54 · Jacobs 2014</text>')
A(f'<line x1="{ax2}" y1="{Y0+70}" x2="{ax2}" y2="{Y1-40}" stroke="#555" stroke-width="1.8" stroke-dasharray="6,4" marker-end="url(#ah)"/>')
A(f'<text transform="translate({ax2-9},{YM}) rotate(-90)" text-anchor="middle" font-size="12" fill="#333">C→D：Hua XXXVI（1914–21）有身体的主体</text>')

# --- Kant Opus postumum: dashed double arrow in left margin of left column
kx = X0 + 26
A(f'<line x1="{kx}" y1="{Y0+70}" x2="{kx}" y2="{Y1-40}" stroke="#c0672b" stroke-width="1.8" stroke-dasharray="6,4" marker-start="url(#ah)" marker-end="url(#ah)"/>')
A(f'<text transform="translate({kx-10},{YM+170}) rotate(-90)" text-anchor="middle" font-size="12" fill="#6e3510">康德《遗著》：在 A 与 B 之间搭桥？（待查）</text>')

# --- boundary placements
# Heidegger on the horizontal midline, left column
hx, hw = X0 + 50, 320
A(f'<rect x="{hx}" y="{YM-28}" width="{hw}" height="56" rx="8" fill="#fcefe6" stroke="#c0672b" stroke-width="1.6"/>')
A(f'<text x="{hx+hw/2}" y="{YM-7}" text-anchor="middle" font-size="13" font-weight="700" fill="#6e3510">Heidegger 1927（Hua IX 601 f.）</text>')
A(f'<text x="{hx+hw/2}" y="{YM+13}" text-anchor="middle" font-size="11.5" fill="#444">构造者 = 生存着的具体的人：拒绝纵轴的二分</text>')
# Merleau-Ponty at the crossing
mw = 220
A(f'<rect x="{XM-mw/2}" y="{YM-28}" width="{mw}" height="56" rx="8" fill="#fcefe6" stroke="#c0672b" stroke-width="2"/>')
A(f'<text x="{XM}" y="{YM-7}" text-anchor="middle" font-size="13" font-weight="700" fill="#6e3510">梅洛-庞蒂</text>')
A(f'<text x="{XM}" y="{YM+13}" text-anchor="middle" font-size="11.5" fill="#444">还原不可完成：落在两条格线的交点上</text>')

# --- legend
ly = Y1 + 34
lx = X0
for kind, label in [("h", "胡塞尔文本（年份 · 出处）"), ("p", "其他哲学家"), ("s", "研究文献")]:
    fill, stroke, col = KIND[kind]
    A(f'<rect x="{lx}" y="{ly-14}" width="26" height="18" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>')
    A(f'<text x="{lx+34}" y="{ly}" font-size="13" fill="#333">{escape(label)}</text>')
    lx += 34 + tw(label, 13) + 30
A(f'<rect x="{lx}" y="{ly-14}" width="26" height="18" rx="4" fill="#fff" stroke="#888" stroke-width="1.4" stroke-dasharray="5,3"/>')
A(f'<text x="{lx+34}" y="{ly}" font-size="13" fill="#333">虚线框：未对照原文 / 待查</text>')
A(f'<text x="{X0}" y="{ly+30}" font-size="13" fill="#333">第三根轴（不画入）：本质必然 / 事实必然——Tengelyi 2014；胡塞尔 1931，Hua XV 385 f.：“一切本质必然性都是它的事实的环节”。</text>')
A(f'<text x="{X0}" y="{ly+54}" font-size="13" fill="#333">本研究的论点：胡塞尔对身体的使用在先验与经验之间摇摆。四格用于诊断：同一身体功能在 A、C、D 之间未加标明的移动（见第 2、6 条）。</text>')

A('</svg>')
open(OUT, "w", encoding="utf-8").write("\n".join(out))
print("written", OUT)
