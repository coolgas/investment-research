#!/usr/bin/env python3
"""
md2pdf.py — Convert markdown to PDF with CJK support.

Usage:
    python3 md2pdf.py input.md [output.pdf]

    Default: uses WeasyPrint (proper formatting + emoji, CJK via system fonts).
    Use --embed-font to use fpdf2 with embedded font subset (no emoji, but
    works on viewers without CJK fonts installed).

Requirements:
    pip install weasyprint markdown fonttools fpdf2
    apt-get install fonts-wqy-microhei
"""
import re
import sys
import os
import subprocess


def _find_cjk_font() -> str:
    try:
        result = subprocess.run(
            ['fc-match', '--format=%{file}', 'WenQuanYi Micro Hei'],
            capture_output=True, text=True, timeout=5)
        path = result.stdout.strip()
        if path and os.path.exists(path):
            return path
    except Exception:
        pass
    for p in [
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    ]:
        if os.path.exists(p):
            return p
    raise FileNotFoundError(
        "No CJK font found. Install with: apt-get install fonts-wqy-microhei")


def _subset_font(font_path: str, text: str) -> str:
    from fontTools.subset import Subsetter, Options
    from fontTools.ttLib import TTFont, TTCollection
    if font_path.endswith('.ttc'):
        ttc = TTCollection(font_path)
        ttc[0].save('/tmp/wqy-single-ttf.tmp')
        font = TTFont('/tmp/wqy-single-ttf.tmp')
    else:
        font = TTFont(font_path)
    chars = sorted(set(c for c in text if not c.isspace()))
    opts = Options()
    opts.layout_features = ['*']
    subsetter = Subsetter(options=opts)
    subsetter.populate(unicodes=[ord(c) for c in chars])
    subsetter.subset(font)
    out = '/tmp/wqy-subset-ttf.tmp'
    font.save(out)
    return out


def strip_frontmatter(text: str) -> str:
    return re.sub(r'^---.*?---', '', text, count=1, flags=re.DOTALL).lstrip()


def _strip_markdown_around_html(text: str) -> str:
    """Strip markdown emphasis markers around inline HTML tags.

    Patterns like **<span class="up">+0.39%</span>** cause the markdown
    parser to leave raw ** or * visible in the rendered PDF output. Since
    the HTML tag (e.g. <span class="up">) already provides visual styling
    via CSS, the surrounding emphasis is redundant and must be stripped
    before markdown parsing.
    """
    # Strip ** before opening HTML tag: **<span... -> <span...
    text = re.sub(r'\*\*(?=<)', '', text)
    # Strip ** after closing HTML tag: </span>** -> </span>
    text = re.sub(r'(?<=>)\*\*', '', text)
    # Strip single * before/after HTML tags too
    text = re.sub(r'(?<!\*)\*(?=<)', '', text)
    text = re.sub(r'(?<=>)\*(?!\*)', '', text)
    return text


def _weasyprint(md_content: str, output_path: str) -> None:
    import markdown
    from weasyprint import HTML

    # Pre-strip emphasis markers around HTML tags to avoid raw **/* leaking
    md_content = _strip_markdown_around_html(md_content)

    html_body = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'codehilite', 'nl2br'])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
@page {{
    size: A4;
    margin: 1.8cm 2cm;
}}
body {{
    font-family: 'WenQuanYi Micro Hei', 'DejaVu Sans', sans-serif;
    font-size: 10.5pt;
    line-height: 1.55;
    color: #1a1a1a;
}}
h1 {{
    font-size: 17pt; color: #1a3a5c; border-bottom: 2px solid #1a3a5c; padding-bottom: 5px; margin-top: 24px;
}}
h2 {{
    font-size: 14pt; color: #2a5a8c; margin-top: 20px; border-bottom: 1px solid #ccc; padding-bottom: 3px;
}}
h3 {{
    font-size: 12pt; color: #3a6a9c; margin-top: 16px;
}}
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 10px 0;
    font-size: 8pt;
    table-layout: fixed;
}}
th {{
    background-color: #1a3a5c;
    color: white;
    padding: 4px 5px;
    text-align: center;
    font-weight: bold;
    overflow-wrap: break-word;
}}
td {{
    border: 1px solid #ccc;
    padding: 3px 5px;
    text-align: center;
    overflow-wrap: break-word;
}}
tr:nth-child(even) {{
    background-color: #f5f8fc;
}}
strong {{ color: #c0392b; }}
span.up {{ color: #1a8a1a; font-weight: bold; }}
span.down {{ color: #c0392b; font-weight: bold; }}
span.num {{ color: #1a3a5c; font-weight: bold; }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

    HTML(string=html).write_pdf(output_path)
    sz = os.path.getsize(output_path)
    print(f"PDF generated: {output_path} ({sz/1024:.1f} KB)")


def _fpdf2_embed(md_content: str, output_path: str) -> None:
    import markdown
    from fpdf import FPDF

    # Pre-strip emphasis markers around HTML tags
    md_content = _strip_markdown_around_html(md_content)

    html_body = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'codehilite', 'nl2br'])

    raw_text = re.sub(r'[*`#>\-_|\\/(){}[\]\'\"<>:;,.!?@$%^&+=~]', '', md_content)
    raw_text += raw_text
    full_font = _find_cjk_font()
    subset_font = _subset_font(full_font, raw_text)

    styled_html = f"""<style>
body {{ font-family: 'CJK'; font-size: 11pt; line-height: 1.5; color: #1a1a1a; }}
h1 {{ font-size: 18pt; color: #1a3a5c; border-bottom: 2px solid #1a3a5c; }}
h2 {{ font-size: 15pt; color: #2a5a8c; border-bottom: 1px solid #ccc; }}
h3 {{ font-size: 13pt; color: #3a6a9c; }}
table {{ border-collapse: collapse; width: 100%; font-size: 9.5pt; }}
th {{ background-color: #1a3a5c; color: white; padding: 4px 8px; font-weight: normal; }}
td {{ border: 1px solid #ccc; padding: 4px 8px; }}
blockquote {{ color: #666; margin-left: 15px; padding-left: 10px; }}
</style>
{html_body}"""

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_font('CJK', '', subset_font)
    pdf.add_font('CJK', 'B', subset_font)
    pdf.add_font('CJK', 'I', subset_font)
    pdf.add_font('CJK', 'BI', subset_font)
    pdf.add_page()
    pdf.set_font('CJK', '', 11)
    pdf.write_html(styled_html)
    pdf.output(output_path)
    sz = os.path.getsize(output_path)
    print(f"PDF generated (embedded font): {output_path} ({sz/1024:.1f} KB, {pdf.pages_count} pages)")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    embed_font = '--embed-font' in sys.argv

    if len(args) < 1:
        print(__doc__.strip())
        sys.exit(1)

    input_path = args[0]
    output_path = args[1] if len(args) >= 2 else \
        os.path.splitext(input_path)[0] + '.pdf'

    with open(input_path, 'r') as f:
        md_content = f.read()
    md_content = strip_frontmatter(md_content)

    if embed_font:
        _fpdf2_embed(md_content, output_path)
    else:
        _weasyprint(md_content, output_path)


if __name__ == '__main__':
    main()