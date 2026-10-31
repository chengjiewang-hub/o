#!/usr/bin/env python3
"""Build the Markdown report + CSV from hits.json produced by leibkoerper_count.py.

Usage: python3 -I leibkoerper_report.py <hits.json> <out_dir>
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from leibkoerper_count import VOLUMES  # noqa: E402

CATS = ["狭义 Leibkörper 词族", "Leibeskörper 词族", "Körperleib 词族",
        "leiblich-körperlich 型并列形容词", "其他双词干复合词"]
SHORT = ["Leibkörper", "Leibeskörper", "Körperleib", "leiblich-körperlich", "其他"]


def main(src: Path, out: Path):
    d = json.loads(src.read_text(encoding="utf-8"))
    hits, words = d["hits"], d["words"]
    out.mkdir(parents=True, exist_ok=True)

    by = defaultdict(Counter)
    for h in hits:
        by[h["file"]][(h["kind"], h["cat"])] += 1
    pcats = sorted({h["cat"] for h in hits if h["kind"] == "phrase"})

    L = []
    L.append("# 胡塞尔著作中 Leibkörper 及相似表达的出现频次（全语料）\n")
    L.append("统计对象：仓库分支 `claude/magical-johnson-pejc60` 中 `胡塞尔/` 目录下全部 `*_volltext.md`"
             "（PDF 文字层 + OCR 转录）。脚本：`scripts/leibkoerper_count.py`、`scripts/leibkoerper_report.py`。\n")
    L.append("## 统计口径\n")
    L.append("- **A. 双词干复合词**（主结果）：同一词中同时含 Leib 与 Körper 词干，含屈折、派生、连字符形式；"
             "Körper 支持 Koerper / Korper / OCR 误识 K6rper、Kärper；处理软连字符与行末断词（`Leib-⏎körper` → `Leibkörper`）。"
             "分为：狭义 Leibkörper 词族（Leibkörper, -s, -n, leibkörperlich, Leibkörperlichkeit, Leib-Körper, 以及 Leibkörperapperzeption 等以其为构词成分的复合词）、"
             "Leibeskörper、Körperleib（含 Körper-Leib、körperleiblich）、leiblich-körperlich / körperlich-leiblich 并列形容词、其他。")
    L.append("- **B. 短语／句式**：körperlich(er/en/em…) Leib(e/es/er/ern)、körperliche Leiblichkeit、Körperding Leib、"
             "Leib … als (bloßer/materieller/Null-) Körper（Leib 与 als 之间至多 3 词）、Körper, der … Leib ist（否定式“kein / noch nicht Leib”不计）、"
             "Leib … wie ein (anderer) Körper、Leib, d.i. … Körper。重叠匹配不重复计数；若短语中的 Körper 本身已是 Leibkörper 复合词，则不再计入 B。")
    L.append("- **C. 参考（不计入合计）**：Leib und Körper / Körper und Leib 并列词组。")
    L.append("- 计数单位为出现位置；目录、正文、附录、校勘注释中的出现均分别计数（未区分作者文本与编者文本）。")
    L.append("- 每万词频率 = 次数 ÷ 机器分词数 × 10000；分母含页眉、脚注、编者文字，OCR 质量影响分母，仅作估算。")
    L.append("- **去重**：Hua IV 有 1952 年版（Biemel）与 2025 年新版 IV/V（Fonfara），二者内容重叠，"
             "“德文合计”只计 1952 年 Hua IV + Hua V，新版单列。英译本不适用德文检索，单列且不计入。")
    L.append("- 页码为 PDF 页码（Hua XIX 为 `T分册-页`），不是 Husserliana 印刷页码。\n")

    # main table
    L.append("## 一、分卷频次\n")
    L.append("| 卷 | 内容 | " + " | ".join(SHORT) + " | **A 复合词合计** | B 短语 | **A+B** | 每万词(A) | 每万词(A+B) | C 参考 |")
    L.append("|---|---|" + "---:|" * (len(SHORT) + 7))
    tot = Counter()
    rows_csv = []
    for fname, (vol, title, lang, main_total) in VOLUMES.items():
        if fname not in words:
            continue
        c = by[fname]
        a = [c[("compound", k)] for k in CATS]
        A = sum(a)
        B = sum(v for (k, _), v in c.items() if k == "phrase")
        C = sum(v for (k, _), v in c.items() if k == "reference")
        w = words[fname]
        if lang == "en":
            continue
        mark = "" if main_total else "（单列，不计入合计）"
        L.append(f"| {vol}{mark} | {title} | " + " | ".join(str(x) for x in a)
                 + f" | **{A}** | {B} | **{A + B}** | {A / w * 1e4:.3f} | {(A + B) / w * 1e4:.3f} | {C} |")
        rows_csv.append([vol, title, w] + a + [A, B, A + B, C])
        if main_total:
            for k, x in zip(CATS, a):
                tot[k] += x
            tot["A"] += A
            tot["B"] += B
            tot["C"] += C
            tot["w"] += w
    L.append(f"| **德文合计（{sum(1 for f,v in VOLUMES.items() if v[3] and f in words)} 种，去重）** | | "
             + " | ".join(str(tot[k]) for k in CATS)
             + f" | **{tot['A']}** | {tot['B']} | **{tot['A'] + tot['B']}** | {tot['A'] / tot['w'] * 1e4:.3f} | "
               f"{(tot['A'] + tot['B']) / tot['w'] * 1e4:.3f} | {tot['C']} |")
    L.append(f"\n德文合计分词数约 {tot['w']:,}。Hua X* 为 Meiner 哲学丛书版《内时间意识现象学》（Bernet 编），非 Husserliana X 原卷。\n")

    # ranking
    L.append("## 二、按复合词次数排序（德文，去重后）\n")
    rk = sorted(((sum(by[f][("compound", k)] for k in CATS), VOLUMES[f][0], VOLUMES[f][1])
                 for f in words if VOLUMES[f][3]), reverse=True)
    L.append("| 排名 | 卷 | A 复合词 | 占比 |")
    L.append("|---:|---|---:|---:|")
    for i, (n, vol, title) in enumerate([r for r in rk if r[0] > 0], 1):
        L.append(f"| {i} | {vol} {title} | {n} | {n / tot['A'] * 100:.1f}% |")
    zero = [r[1] for r in rk if r[0] == 0]
    L.append(f"\n复合词为 0 的卷：{'、'.join(zero)}。\n")

    # forms
    L.append("## 三、完整词形频次（A 类，全部德文文件，含新版 IV/V）\n")
    fc = Counter((h["cat"], h["form"]) for h in hits if h["kind"] == "compound" and h["lang"] == "de")
    fv = defaultdict(Counter)
    for h in hits:
        if h["kind"] == "compound" and h["lang"] == "de":
            fv[(h["cat"], h["form"])][h["vol"]] += 1
    L.append("| 词族 | 原始词形（OCR 原样） | 次数 | 分布 |")
    L.append("|---|---|---:|---|")
    for (cat, form), n in sorted(fc.items(), key=lambda x: (CATS.index(x[0][0]), -x[1], x[0][1])):
        dist = "，".join(f"{v} {k}" for v, k in sorted(((v, k) for k, v in fv[(cat, form)].items()), reverse=True))
        L.append(f"| {cat} | `{form}` | {n} | {dist} |")
    L.append("\n`Leibkorper`、`Leibk6rper` 等是 OCR 对 `Leibkörper` 的误识（主要见 Hua XIII），已计入同一词族。\n")

    # phrases
    L.append("## 四、短语／句式（B 类）分卷\n")
    vols_b = [f for f in words if VOLUMES[f][2] == "de" and any(by[f][("phrase", c)] for c in pcats)]
    L.append("| 结构 | " + " | ".join(VOLUMES[f][0] for f in vols_b) + " |")
    L.append("|---|" + "---:|" * len(vols_b))
    for c in pcats:
        L.append(f"| {c} | " + " | ".join(str(by[f][("phrase", c)]) for f in vols_b) + " |")
    L.append("")

    # reference
    L.append("## 五、参考：Leib und Körper / Körper und Leib（不计入合计）\n")
    for h in hits:
        if h["kind"] == "reference" and h["lang"] == "de":
            L.append(f"- {h['vol']} p.{h['page']}：`{h['form']}` — …{h['context'][:200]}…")
    L.append("")

    # caveats
    L.append("## 六、说明与局限\n")
    L.append("- 语料并非胡塞尔全集：缺 Hua III（德文）、XX、XXIX–XXXII、XXXV–XXXVIII、XL、XLI、XLIII 等卷以及 Materialien 其余各卷；"
             "`hua3_volltext.md` 实为《观念 II》英译本（Collected Works III），不是德文 Hua III。")
    L.append("- 已与此前人工核对过的 `hua345_Leibkoerper_词频统计.md` 交叉验证：Hua IV 复合词 39、Hua V 1、新版 IV/V 21，三项完全一致。"
             "短语类为自动规则匹配，Hua IV 为 13（旧表人工扩充为 15，差异来自“Körper … ist Leib”“leiblich … als körperlich”等松散句式），故 B 类是保守下限。")
    L.append("- 部分卷有空白页（无文字层、OCR 未补）：Hua VII 25 页、VIII 34 页、I 14 页、II 12 页、IV/V 新版 9 页、X* 8 页等，这些页上的出现无法统计。")
    L.append("- 英译本中 Leibkörper 通常被译为 “living body / Body-body / bodily-body” 等，不在德文检索范围内。")
    L.append("- 完整命中清单（卷、PDF 页、类别、原词形、上下文）见 `leibkoerper_hits.csv`。\n")

    (out / "Leibkoerper_全集词频统计.md").write_text("\n".join(L), encoding="utf-8")
    with open(out / "leibkoerper_hits.csv", "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["卷", "文件", "PDF页", "类型", "类别", "词形", "上下文"])
        for h in hits:
            wr.writerow([h["vol"], h["file"], h["page"], h["kind"], h["cat"], h["form"], h["context"]])
    with open(out / "leibkoerper_by_volume.csv", "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["卷", "内容", "词数"] + SHORT + ["A合计", "B短语", "A+B", "C参考"])
        wr.writerows(rows_csv)


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
