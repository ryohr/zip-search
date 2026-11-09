#!/usr/bin/env python3
"""utf_ken_all.csv から、index.html が読み込む data.js を生成します。

使い方:
    python3 build_data.py utf_ken_all.csv
    （引数を省略すると同じフォルダの utf_ken_all.csv を使います）

必要な列だけを抜き出して1ファイルにまとめるだけなので、
町域名の整形や分割行の結合は index.html 側で行います。
"""
import csv
import json
import sys
from pathlib import Path

src = Path(sys.argv[1] if len(sys.argv) > 1 else "utf_ken_all.csv")
out = Path(__file__).with_name("data.js")

# KEN_ALL の列: 2=郵便番号, 3〜5=読み(都道府県/市区町村/町域), 6〜8=漢字(同)
COLS = (2, 3, 4, 5, 6, 7, 8)

raw = src.read_bytes()
try:
    text = raw.decode("utf-8-sig")
except UnicodeDecodeError:
    text = raw.decode("cp932")  # 旧形式の KEN_ALL.CSV（Shift_JIS）にも対応

lines = []
for row in csv.reader(text.splitlines()):
    if len(row) < 9:
        continue
    lines.append("\t".join(row[i].strip() for i in COLS))

payload = json.dumps("\n".join(lines), ensure_ascii=False)
out.write_text(
    "// build_data.py で生成。手で編集しないでください。\n"
    f"window.KEN_ALL_TSV = {payload};\n",
    encoding="utf-8",
)
print(f"{len(lines):,} 行を {out.name} に書き出しました（{out.stat().st_size / 1e6:.1f} MB）")
