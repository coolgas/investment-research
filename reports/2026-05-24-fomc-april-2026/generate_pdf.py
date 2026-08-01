import markdown, weasyprint

with open('market-brief.md') as f:
    md = f.read()

html = markdown.markdown(md, extensions=['extra', 'toc'])
html = f'''<html><head><meta charset="utf-8"><style>
body{{font-family:DejaVu Sans;padding:40px;font-size:11pt;line-height:1.6;color:#111}}
h1{{font-size:20pt;border-bottom:2px solid #333;padding-bottom:8px}}
h2{{font-size:16pt;color:#2a4a7f}}
h3{{font-size:13pt;color:#555}}
table{{border-collapse:collapse;width:100%;margin:12px 0}}
th,td{{border:1px solid #ccc;padding:8px;text-align:left}}
th{{background:#2a4a7f;color:#fff}}
tr:nth-child(even){{background:#f5f7fa}}
.up{{color:#1a7a2e}}
.down{{color:#c0392b}}
.num{{font-weight:700}}
code{{background:#eee;padding:2px 5px;border-radius:3px;font-size:10pt}}
pre{{background:#f5f5f5;padding:12px;border-radius:5px;overflow-x:auto}}
blockquote{{border-left:4px solid #2a4a7f;margin-left:0;padding:10px 20px;background:#f9faff}}
hr{{border:none;border-top:1px solid #ddd}}
h1,h2,h3,h4{{page-break-after:avoid}}
table,img,pre,blockquote{{page-break-inside:avoid}}
</style></head><body>{html}</body></html>'''

weasyprint.HTML(string=html).write_pdf('market-brief.pdf')
print('PDF generated successfully')