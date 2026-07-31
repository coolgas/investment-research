#!/usr/bin/env python3
"""Stage 3: convert report md -> styled PDF via weasyprint (orchestrator step)."""
import re, markdown, os, sys

SRC = "/root/workspace/investment-research/reports/2026-07-31-gold-suppression/market-brief.md"
OUT = "/root/workspace/investment-research/reports/2026-07-31-gold-suppression/market-brief.pdf"

CSS = """
@page { size: A4; margin: 1.6cm; }
body { font-family: 'DejaVu Sans', sans-serif; font-size: 9.5pt; line-height: 1.45; color: #1a1a1a; }
h1 { font-size: 15pt; color: #0d2a4a; border-bottom: 2px solid #0d2a4a; padding-bottom: 4px; }
h2 { font-size: 12pt; color: #0d2a4a; margin-top: 14px; border-bottom: 1px solid #c8d4e2; padding-bottom: 2px; }
h3 { font-size: 10.5pt; color: #1a3a5c; }
table { width: 100%; border-collapse: collapse; table-layout: fixed; margin: 8px 0; }
th { background-color: #0d2a4a; color: #fff; font-size: 7.5pt; padding: 4px 5px; text-align: left; }
td { font-size: 7.5pt; padding: 3px 5px; border-bottom: 1px solid #d9d9d9; }
tr:nth-child(even) td { background-color: #f2f5f9; }
span.up { color: #1a7f37; font-weight: bold; }
span.down { color: #c62828; font-weight: bold; }
span.num { color: #0d3a6e; font-weight: bold; }
em { color: #55606e; font-size: 8pt; }
p { margin: 4px 0; }
ul, ol { margin: 4px 0; padding-left: 18px; }
li { margin: 2px 0; }
strong { color: #0d2a4a; }
hr { border: none; border-top: 1px solid #c8d4e2; margin: 10px 0; }
"""

with open(SRC) as f:
    md = f.read()
md = re.sub(r'^---\n.*?\n---\n', '', md, count=1, flags=re.DOTALL).lstrip()
body = markdown.markdown(md, extensions=['tables', 'fenced_code', 'nl2br'])
html = f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'

os.makedirs(os.path.dirname(OUT), exist_ok=True)
from weasyprint import HTML
HTML(string=html).write_pdf(OUT)

size = os.path.getsize(OUT)
print(f"PDF written: {OUT} ({size} bytes)")
assert size > 10000, f"PDF too small: {size} bytes"
print("PASS: PDF > 10KB")