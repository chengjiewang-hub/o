# 胡塞尔著作中 Leibkörper 及相似表达的出现频次（全语料）

统计对象：仓库分支 `claude/magical-johnson-pejc60` 中 `胡塞尔/` 目录下全部 `*_volltext.md`（PDF 文字层 + OCR 转录）。脚本：`scripts/leibkoerper_count.py`、`scripts/leibkoerper_report.py`。

## 统计口径

- **A. 双词干复合词**（主结果）：同一词中同时含 Leib 与 Körper 词干，含屈折、派生、连字符形式；Körper 支持 Koerper / Korper / OCR 误识 K6rper、Kärper；处理软连字符与行末断词（`Leib-⏎körper` → `Leibkörper`）。分为：狭义 Leibkörper 词族（Leibkörper, -s, -n, leibkörperlich, Leibkörperlichkeit, Leib-Körper, 以及 Leibkörperapperzeption 等以其为构词成分的复合词）、Leibeskörper、Körperleib（含 Körper-Leib、körperleiblich）、leiblich-körperlich / körperlich-leiblich 并列形容词、其他。
- **B. 短语／句式**：körperlich(er/en/em…) Leib(e/es/er/ern)、körperliche Leiblichkeit、Körperding Leib、Leib … als (bloßer/materieller/Null-) Körper（Leib 与 als 之间至多 3 词）、Körper, der … Leib ist（否定式“kein / noch nicht Leib”不计）、Leib … wie ein (anderer) Körper、Leib, d.i. … Körper。重叠匹配不重复计数；若短语中的 Körper 本身已是 Leibkörper 复合词，则不再计入 B。
- **C. 参考（不计入合计）**：Leib und Körper / Körper und Leib 并列词组。
- 计数单位为出现位置；目录、正文、附录、校勘注释中的出现均分别计数（未区分作者文本与编者文本）。
- 每万词频率 = 次数 ÷ 机器分词数 × 10000；分母含页眉、脚注、编者文字，OCR 质量影响分母，仅作估算。
- **去重**：Hua IV 有 1952 年版（Biemel）与 2025 年新版 IV/V（Fonfara），二者内容重叠，“德文合计”只计 1952 年 Hua IV + Hua V，新版单列。英译本不适用德文检索，单列且不计入。
- 页码为 PDF 页码（Hua XIX 为 `T分册-页`），不是 Husserliana 印刷页码。

## 一、分卷频次

| 卷 | 内容 | Leibkörper | Leibeskörper | Körperleib | leiblich-körperlich | 其他 | **A 复合词合计** | B 短语 | **A+B** | 每万词(A) | 每万词(A+B) | C 参考 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Hua I | Cartesianische Meditationen (1950) | 9 | 0 | 1 | 0 | 0 | **10** | 11 | **21** | 1.329 | 2.790 | 0 |
| Hua II | Die Idee der Phänomenologie (1950) | 0 | 0 | 0 | 0 | 0 | **0** | 0 | **0** | 0.000 | 0.000 | 0 |
| Hua IV | Ideen II (1952, Biemel) | 36 | 2 | 0 | 1 | 0 | **39** | 13 | **52** | 2.668 | 3.557 | 0 |
| Hua IV/V neu（单列，不计入合计） | Ideen II/III Neuedition (Fonfara) | 16 | 4 | 0 | 1 | 0 | **21** | 10 | **31** | 0.666 | 0.983 | 0 |
| Hua V | Ideen III (1952) | 1 | 0 | 0 | 0 | 0 | **1** | 0 | **1** | 0.183 | 0.183 | 0 |
| Hua VI | Krisis | 0 | 0 | 1 | 1 | 0 | **2** | 18 | **20** | 0.108 | 1.075 | 1 |
| Hua VII | Erste Philosophie I | 0 | 0 | 0 | 0 | 0 | **0** | 1 | **1** | 0.000 | 0.063 | 0 |
| Hua VIII | Erste Philosophie II | 10 | 0 | 0 | 0 | 0 | **10** | 7 | **17** | 0.475 | 0.807 | 0 |
| Hua IX | Phänomenologische Psychologie | 24 | 0 | 1 | 0 | 0 | **25** | 20 | **45** | 1.058 | 1.905 | 0 |
| Hua X* | Zeitbewußtsein (Meiner PhB-Ausgabe, Bernet) | 0 | 0 | 0 | 0 | 0 | **0** | 0 | **0** | 0.000 | 0.000 | 0 |
| Hua XI | Analysen zur passiven Synthesis | 0 | 0 | 0 | 0 | 0 | **0** | 2 | **2** | 0.000 | 0.110 | 0 |
| Hua XII | Philosophie der Arithmetik | 0 | 0 | 0 | 0 | 0 | **0** | 0 | **0** | 0.000 | 0.000 | 0 |
| Hua XIII | Intersubjektivität I | 153 | 0 | 9 | 2 | 0 | **164** | 11 | **175** | 7.890 | 8.419 | 1 |
| Hua XIV | Intersubjektivität II | 206 | 1 | 5 | 6 | 0 | **218** | 17 | **235** | 9.689 | 10.445 | 0 |
| Hua XV | Intersubjektivität III | 66 | 0 | 1 | 2 | 1 | **70** | 82 | **152** | 2.537 | 5.508 | 1 |
| Hua XVI | Ding und Raum | 13 | 0 | 1 | 0 | 0 | **14** | 1 | **15** | 1.168 | 1.251 | 0 |
| Hua XVII | Formale und transzendentale Logik | 0 | 0 | 0 | 0 | 0 | **0** | 4 | **4** | 0.000 | 0.231 | 0 |
| Hua XVIII | Logische Untersuchungen I | 0 | 0 | 0 | 0 | 0 | **0** | 0 | **0** | 0.000 | 0.000 | 0 |
| Hua XIX | Logische Untersuchungen II | 0 | 0 | 0 | 0 | 0 | **0** | 0 | **0** | 0.000 | 0.000 | 0 |
| Hua XXI | Studien zur Arithmetik und Geometrie | 0 | 0 | 0 | 0 | 0 | **0** | 0 | **0** | 0.000 | 0.000 | 0 |
| Hua XXII | Aufsätze und Rezensionen 1890–1910 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | **0** | 0.000 | 0.000 | 0 |
| Hua XXIII | Phantasie, Bildbewusstsein, Erinnerung | 0 | 0 | 0 | 0 | 0 | **0** | 0 | **0** | 0.000 | 0.000 | 0 |
| Hua XXIV | Einleitung in die Logik und Erkenntnistheorie | 0 | 0 | 0 | 0 | 0 | **0** | 0 | **0** | 0.000 | 0.000 | 0 |
| Hua XXV | Aufsätze und Vorträge 1911–1921 | 2 | 0 | 0 | 0 | 0 | **2** | 0 | **2** | 0.144 | 0.144 | 0 |
| Hua XXVI | Vorlesungen über Bedeutungslehre | 0 | 0 | 0 | 0 | 0 | **0** | 0 | **0** | 0.000 | 0.000 | 0 |
| Hua XXVII | Aufsätze und Vorträge 1922–1937 | 0 | 0 | 0 | 0 | 0 | **0** | 1 | **1** | 0.000 | 0.083 | 0 |
| Hua XXVIII | Vorlesungen über Ethik und Wertlehre | 0 | 0 | 0 | 0 | 0 | **0** | 0 | **0** | 0.000 | 0.000 | 0 |
| Hua XXXIII | Bernauer Manuskripte | 0 | 0 | 0 | 0 | 0 | **0** | 0 | **0** | 0.000 | 0.000 | 0 |
| Hua XXXIV | Zur phänomenologischen Reduktion | 7 | 0 | 1 | 0 | 0 | **8** | 9 | **17** | 0.362 | 0.769 | 0 |
| Hua XXXIX | Die Lebenswelt | 11 | 0 | 3 | 0 | 0 | **14** | 25 | **39** | 0.356 | 0.991 | 0 |
| Hua XLII | Grenzprobleme der Phänomenologie | 2 | 0 | 0 | 0 | 0 | **2** | 8 | **10** | 0.073 | 0.365 | 0 |
| Mat VIII | Späte Texte über Zeitkonstitution (C-Mss.) | 7 | 0 | 0 | 0 | 0 | **7** | 13 | **20** | 0.443 | 1.266 | 0 |
| Mat XI | Manuskripte zur Konstitution von Raumdingen (D-Mss.) | 4 | 0 | 1 | 0 | 0 | **5** | 5 | **10** | 0.550 | 1.101 | 1 |
| **德文合计（32 种，去重）** | | 551 | 3 | 24 | 12 | 1 | **591** | 248 | **839** | 1.049 | 1.489 | 4 |

德文合计分词数约 5,635,836。Hua X* 为 Meiner 哲学丛书版《内时间意识现象学》（Bernet 编），非 Husserliana X 原卷。

## 二、按复合词次数排序（德文，去重后）

| 排名 | 卷 | A 复合词 | 占比 |
|---:|---|---:|---:|
| 1 | Hua XIV Intersubjektivität II | 218 | 36.9% |
| 2 | Hua XIII Intersubjektivität I | 164 | 27.7% |
| 3 | Hua XV Intersubjektivität III | 70 | 11.8% |
| 4 | Hua IV Ideen II (1952, Biemel) | 39 | 6.6% |
| 5 | Hua IX Phänomenologische Psychologie | 25 | 4.2% |
| 6 | Hua XXXIX Die Lebenswelt | 14 | 2.4% |
| 7 | Hua XVI Ding und Raum | 14 | 2.4% |
| 8 | Hua VIII Erste Philosophie II | 10 | 1.7% |
| 9 | Hua I Cartesianische Meditationen (1950) | 10 | 1.7% |
| 10 | Hua XXXIV Zur phänomenologischen Reduktion | 8 | 1.4% |
| 11 | Mat VIII Späte Texte über Zeitkonstitution (C-Mss.) | 7 | 1.2% |
| 12 | Mat XI Manuskripte zur Konstitution von Raumdingen (D-Mss.) | 5 | 0.8% |
| 13 | Hua XXV Aufsätze und Vorträge 1911–1921 | 2 | 0.3% |
| 14 | Hua XLII Grenzprobleme der Phänomenologie | 2 | 0.3% |
| 15 | Hua VI Krisis | 2 | 0.3% |
| 16 | Hua V Ideen III (1952) | 1 | 0.2% |

复合词为 0 的卷：Hua XXXIII、Hua XXVIII、Hua XXVII、Hua XXVI、Hua XXIV、Hua XXIII、Hua XXII、Hua XXI、Hua XVIII、Hua XVII、Hua XIX、Hua XII、Hua XI、Hua X*、Hua VII、Hua II。

## 三、完整词形频次（A 类，全部德文文件，含新版 IV/V）

| 词族 | 原始词形（OCR 原样） | 次数 | 分布 |
|---|---|---:|---|
| 狭义 Leibkörper 词族 | `Leibkörper` | 279 | 136 Hua XIV，48 Hua XV，29 Hua IV，19 Hua IX，10 Hua VIII，8 Hua IV/V neu，6 Mat VIII，6 Hua XXXIV，5 Hua XXXIX，5 Hua I，4 Hua XVI，2 Mat XI，1 Hua XLII |
| 狭义 Leibkörper 词族 | `Leibkorper` | 92 | 92 Hua XIII |
| 狭义 Leibkörper 词族 | `Leibkörpers` | 59 | 28 Hua XIV，12 Hua XV，9 Hua XVI，2 Hua IV，2 Hua I，1 Mat XI，1 Mat VIII，1 Hua XXXIV，1 Hua V，1 Hua IX，1 Hua IV/V neu |
| 狭义 Leibkörper 词族 | `Leibkörperlichkeit` | 31 | 17 Hua XIV，3 Hua IX，3 Hua IV，2 Hua XXXIX，2 Hua XXV，2 Hua XV，2 Hua IV/V neu |
| 狭义 Leibkörper 词族 | `Leibkorpers` | 22 | 22 Hua XIII |
| 狭义 Leibkörper 词族 | `Leibk6rper` | 14 | 14 Hua XIII |
| 狭义 Leibkörper 词族 | `Leib-Körper` | 9 | 4 Hua IV/V neu，3 Hua XXXIX，1 Mat XI，1 Hua I |
| 狭义 Leibkörper 词族 | `Leibkorperlichkeit` | 9 | 9 Hua XIII |
| 狭义 Leibkörper 词族 | `Leibkörpern` | 8 | 6 Hua XIV，1 Hua XXXIX，1 Hua XLII |
| 狭义 Leibkörper 词族 | `leibkörperlichen` | 8 | 5 Hua XIV，2 Hua XV，1 Hua I |
| 狭义 Leibkörper 词族 | `Leibk6rpers` | 4 | 4 Hua XIII |
| 狭义 Leibkörper 词族 | `leibkörperlich` | 4 | 3 Hua XIV，1 Hua IV |
| 狭义 Leibkörper 词族 | `leibkörperliche` | 4 | 2 Hua XIV，1 Hua XV，1 Hua IV |
| 狭义 Leibkörper 词族 | `LEIBKÖRPERS` | 3 | 3 Hua XIV |
| 狭义 Leibkörper 词族 | `LEIBKORPER` | 2 | 2 Hua XIII |
| 狭义 Leibkörper 词族 | `Leibkörperapperzeption` | 2 | 2 Hua XIV |
| 狭义 Leibkörper 词族 | `Erscheinung-dieses-Leibkörpers` | 1 | 1 Hua IV/V neu |
| 狭义 Leibkörper 词族 | `LEIBKORPERS` | 1 | 1 Hua XIII |
| 狭义 Leibkörper 词族 | `LEIBKÖRPERLICHKEIT` | 1 | 1 Hua XIV |
| 狭义 Leibkörper 词族 | `Leib-Körperlichkeit` | 1 | 1 Hua IX |
| 狭义 Leibkörper 词族 | `Leibkorperanalogons` | 1 | 1 Hua XIII |
| 狭义 Leibkörper 词族 | `Leibkorperapperzeption` | 1 | 1 Hua XIII |
| 狭义 Leibkörper 词族 | `Leibkorpererscheinung` | 1 | 1 Hua XIII |
| 狭义 Leibkörper 词族 | `Leibkorpererscheinungen` | 1 | 1 Hua XIII |
| 狭义 Leibkörper 词族 | `Leibkorperform` | 1 | 1 Hua XIII |
| 狭义 Leibkörper 词族 | `Leibkorperkonstitution` | 1 | 1 Hua XIII |
| 狭义 Leibkörper 词族 | `Leibkorperliehkeit` | 1 | 1 Hua XIII |
| 狭义 Leibkörper 词族 | `Leibkorperwahmeh` | 1 | 1 Hua XIII |
| 狭义 Leibkörper 词族 | `Leibkörperlich` | 1 | 1 Hua XIV |
| 狭义 Leibkörper 词族 | `Leibkörperlichen` | 1 | 1 Hua XIV |
| 狭义 Leibkörper 词族 | `Leibkörperwahrnehmung` | 1 | 1 Hua XIV |
| 狭义 Leibkörper 词族 | `deslLeibkörpers` | 1 | 1 Hua XV |
| 狭义 Leibkörper 词族 | `leibkorperlich-seelische` | 1 | 1 Hua XIII |
| Leibeskörper 词族 | `Leibeskörper` | 5 | 3 Hua IV/V neu，2 Hua IV |
| Leibeskörper 词族 | `Leibeskörpers` | 2 | 1 Hua XIV，1 Hua IV/V neu |
| Körperleib 词族 | `Körperleib` | 9 | 4 Hua XIV，2 Hua XXXIX，1 Hua XVI，1 Hua XV，1 Hua I |
| Körperleib 词族 | `Korperleib` | 5 | 5 Hua XIII |
| Körperleib 词族 | `Korperleibes` | 2 | 2 Hua XIII |
| Körperleib 词族 | `Körper-Leib` | 2 | 1 Hua XXXIV，1 Hua IX |
| Körperleib 词族 | `KorperleibfHi` | 1 | 1 Hua XIII |
| Körperleib 词族 | `Korperleiblichkeit` | 1 | 1 Hua XIII |
| Körperleib 词族 | `Körperleibes` | 1 | 1 Hua XIV |
| Körperleib 词族 | `Körperleibstellung` | 1 | 1 Mat XI |
| Körperleib 词族 | `körperleibliche` | 1 | 1 Hua VI |
| Körperleib 词族 | `körperleiblichen` | 1 | 1 Hua XXXIX |
| leiblich-körperlich 型并列形容词 | `leiblich-körperliche` | 2 | 1 Hua IV/V neu，1 Hua IV |
| leiblich-körperlich 型并列形容词 | `leiblich-körperlichen` | 2 | 1 Hua XV，1 Hua XIV |
| leiblich-körperlich 型并列形容词 | `Körperlich-Leiblichen` | 1 | 1 Hua XIV |
| leiblich-körperlich 型并列形容词 | `Leiblichkeit-Korperlichkeit` | 1 | 1 Hua XIII |
| leiblich-körperlich 型并列形容词 | `korperlich-leibliche` | 1 | 1 Hua XIII |
| leiblich-körperlich 型并列形容词 | `körperlich-leiblich` | 1 | 1 Hua XV |
| leiblich-körperlich 型并列形容词 | `körperlich-leibliche` | 1 | 1 Hua XIV |
| leiblich-körperlich 型并列形容词 | `leiblich-körperlich` | 1 | 1 Hua XIV |
| leiblich-körperlich 型并列形容词 | `leiblich-körperlicher` | 1 | 1 Hua XIV |
| leiblich-körperlich 型并列形容词 | `leiblichkörperlich` | 1 | 1 Hua VI |
| leiblich-körperlich 型并列形容词 | `leiblichkörperlichen` | 1 | 1 Hua XIV |
| 其他双词干复合词 | `Als-ob-ich-denzweiten-Körper-dort-als-meinen-Leib-hätte` | 1 | 1 Hua XV |

`Leibkorper`、`Leibk6rper` 等是 OCR 对 `Leibkörper` 的误识（主要见 Hua XIII），已计入同一词族。

## 四、短语／句式（B 类）分卷

| 结构 | Hua I | Hua IV | Hua IV/V neu | Hua VI | Hua VII | Hua VIII | Hua IX | Hua XI | Hua XIII | Hua XIV | Hua XV | Hua XVI | Hua XVII | Hua XXVII | Hua XXXIV | Hua XXXIX | Hua XLII | Mat VIII | Mat XI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Körper, der (…) Leib ist | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Körperding Leib | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Leib … als (…) Körper | 2 | 3 | 5 | 0 | 0 | 0 | 2 | 0 | 10 | 4 | 26 | 1 | 0 | 0 | 0 | 6 | 1 | 0 | 3 |
| Leib … wie (ein anderer) Körper | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Leib, d.i. … Körper | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| körperlich + Leib | 9 | 5 | 3 | 16 | 1 | 7 | 12 | 2 | 1 | 11 | 53 | 0 | 2 | 1 | 5 | 16 | 7 | 13 | 2 |
| körperlich + Leiblichkeit | 0 | 1 | 0 | 2 | 0 | 0 | 6 | 0 | 0 | 2 | 3 | 0 | 2 | 0 | 4 | 3 | 0 | 0 | 0 |

## 五、参考：Leib und Körper / Körper und Leib（不计入合计）

- Hua VI p.066：`Körper und Leib` — …n in seinen Eigenschaften, darstellende sein zu können. 30 So sind rein wahrnehmungsmäßig Körper und Leib wesentlich unterschieden; Leib nämlich als der einzig wirklich wahrnehmungsmäßige Leib, m…
- Hua XIII p.309：`K6rper und Leib` — …niipfe also in einer Einheit des Bewusstseins als Identisehes den urspriinglieh gegebenen K6rper und Leib mit dem in jener Standpunktbeschauung ausserlich erseheinenden K6rper, der, weil er derse…
- Hua XV p.009：`Körper und Leib` — …. . . . . . . . . . . . . . . . . . . 282 BEILAGE XVIII. Die Weise, wie der Leib sich als Körper und Leib konstituiert, sowie die Weisen, wie überhaupt seine Konstitution und Aussendingkonstituti…
- Mat XI p.204：`Leib und Körper` — …g können alle sich notwendig mitkonstituierenden Gleichstellungen (Homogenisierungen) von Leib und Körper oder körperlichem Leib als Körper gleich anderen, Menschheit als Tierspezies unter Tiersp…

## 六、说明与局限

- 语料并非胡塞尔全集：缺 Hua III（德文）、XX、XXIX–XXXII、XXXV–XXXVIII、XL、XLI、XLIII 等卷以及 Materialien 其余各卷；`hua3_volltext.md` 实为《观念 II》英译本（Collected Works III），不是德文 Hua III。
- 已与此前人工核对过的 `hua345_Leibkoerper_词频统计.md` 交叉验证：Hua IV 复合词 39、Hua V 1、新版 IV/V 21，三项完全一致。短语类为自动规则匹配，Hua IV 为 13（旧表人工扩充为 15，差异来自“Körper … ist Leib”“leiblich … als körperlich”等松散句式），故 B 类是保守下限。
- 部分卷有空白页（无文字层、OCR 未补）：Hua VII 25 页、VIII 34 页、I 14 页、II 12 页、IV/V 新版 9 页、X* 8 页等，这些页上的出现无法统计。
- 英译本中 Leibkörper 通常被译为 “living body / Body-body / bodily-body” 等，不在德文检索范围内。
- 完整命中清单（卷、PDF 页、类别、原词形、上下文）见 `leibkoerper_hits.csv`。
