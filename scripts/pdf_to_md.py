#!/usr/bin/env python3
"""批量把 PDF 转成 Markdown。

用法:
    python scripts/pdf_to_md.py <pdf文件夹> [输出文件夹] [--engine pymupdf|marker]

示例:
    python scripts/pdf_to_md.py ~/Desktop/papers chapters
    python scripts/pdf_to_md.py ~/Desktop/papers chapters --engine marker

引擎:
    pymupdf  速度快, 适合文字型 PDF (默认)   pip install pymupdf4llm
    marker   公式/表格/扫描件效果更好, 较慢    pip install marker-pdf
"""
import argparse
import subprocess
import sys
from pathlib import Path


def convert_pymupdf(pdf: Path, out_dir: Path) -> None:
    try:
        import pymupdf4llm
    except ImportError:
        sys.exit("缺少依赖, 请先运行: pip install pymupdf4llm")
    md = pymupdf4llm.to_markdown(str(pdf))
    (out_dir / f"{pdf.stem}.md").write_text(md, encoding="utf-8")


def convert_marker(src: Path, out_dir: Path) -> None:
    try:
        subprocess.run(["marker", str(src), "--output_dir", str(out_dir)], check=True)
    except FileNotFoundError:
        sys.exit("缺少依赖, 请先运行: pip install marker-pdf")


def main() -> None:
    p = argparse.ArgumentParser(description="批量 PDF 转 Markdown")
    p.add_argument("input", type=Path, help="PDF 文件或包含 PDF 的文件夹")
    p.add_argument("output", type=Path, nargs="?", default=Path("md_output"), help="输出文件夹 (默认 md_output)")
    p.add_argument("--engine", choices=["pymupdf", "marker"], default="pymupdf")
    args = p.parse_args()

    if not args.input.exists():
        sys.exit(f"路径不存在: {args.input}")
    args.output.mkdir(parents=True, exist_ok=True)

    if args.engine == "marker":
        convert_marker(args.input, args.output)
        print(f"完成, 输出在 {args.output}")
        return

    pdfs = [args.input] if args.input.is_file() else sorted(args.input.rglob("*.pdf"))
    if not pdfs:
        sys.exit("没有找到 PDF 文件")
    failed = []
    for i, pdf in enumerate(pdfs, 1):
        print(f"[{i}/{len(pdfs)}] {pdf.name}")
        try:
            convert_pymupdf(pdf, args.output)
        except Exception as e:
            failed.append((pdf.name, e))
            print(f"  失败: {e}")
    print(f"完成: 成功 {len(pdfs) - len(failed)}, 失败 {len(failed)}, 输出在 {args.output}")


if __name__ == "__main__":
    main()
