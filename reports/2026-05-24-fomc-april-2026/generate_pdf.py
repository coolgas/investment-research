#!/usr/bin/env python3
"""Convert the market-brief markdown to a clean PDF using fpdf2."""

import re
import sys
from pathlib import Path

from fpdf import FPDF


def strip_span_tags(text: str) -> str:
    """Remove <span> tags but keep their content."""
    text = re.sub(r'<span[^>]*>', '', text)
    text = re.sub(r'</span>', '', text)
    return text


def parse_table_row(line: str) -> list[str]:
    """Parse a markdown table row into cells."""
    cells = []
    for cell in line.strip().strip('|').split('|'):
        cell = strip_span_tags(cell.strip())
        cells.append(cell)
    return cells


def render_markdown_table(pdf, lines, start_idx):
    """Render a markdown table from line start_idx (header row). Returns next line index."""
    # Collect all table rows
    rows = []
    i = start_idx
    while i < len(lines):
        line = lines[i].rstrip()
        if not line or not line.startswith('|'):
            break
        if re.match(r'^\|[\s\-:|]+\|$', line):  # separator row
            i += 1
            continue
        cells = parse_table_row(line)
        rows.append(cells)
        i += 1

    if not rows:
        return i

    # Style the table
    col_count = max(len(r) for r in rows) if rows else 0
    if col_count == 0:
        return i

    # Calculate column widths
    avail_w = pdf.w - pdf.l_margin - pdf.r_margin
    col_w = avail_w / col_count

    # Header
    pdf.set_fill_color(30, 60, 114)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('DejaVu', 'B', 6)

    header = rows[0]
    x_start = pdf.get_x()
    y_start = pdf.get_y()

    # Check if we need a new page
    if y_start + 8 > pdf.h - pdf.b_margin:
        pdf.add_page()
        y_start = pdf.get_y()

    max_h = 0
    for ci, cell in enumerate(header):
        pdf.set_xy(x_start + ci * col_w, y_start)
        # Calculate needed height
        lines_needed = max(1, len(cell) // max(1, int(col_w / 2.2)) + 1)
        cell_h = max(6, lines_needed * 4)
        max_h = max(max_h, cell_h)
        pdf.cell(col_w, cell_h, cell, border=0, align='C', fill=True)
    pdf.set_fill_color(245, 245, 245)
    pdf.set_text_color(30, 30, 30)

    # Data rows
    pdf.set_font('DejaVu', '', 5.5)
    for ri in range(1, len(rows)):
        row = rows[ri]
        y_row = y_start + ri * max_h

        if y_row + 6 > pdf.h - pdf.b_margin:
            pdf.add_page()
            y_start = pdf.get_y()
            y_row = y_start
            # Redraw header
            pdf.set_fill_color(30, 60, 114)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font('DejaVu', 'B', 6)
            for ci, cell in enumerate(header):
                pdf.set_xy(x_start + ci * col_w, y_row)
                pdf.cell(col_w, max_h, cell, border=0, align='C', fill=True)
            pdf.set_fill_color(245, 245, 245)
            pdf.set_text_color(30, 30, 30)
            pdf.set_font('DejaVu', '', 6.5)
            y_start = pdf.get_y()
            y_row = y_start + max_h

        fill = ri % 2 == 0
        for ci, cell in enumerate(row):
            align = 'C' if ci > 0 else 'L'
            if ci == 0 and cell.startswith('**') and cell.endswith('**'):
                cell = cell.strip('*')
                pdf.set_font('DejaVu', 'B', 6.5)
            elif cell.startswith('**') and cell.endswith('**'):
                cell = cell.strip('*')
                pdf.set_font('DejaVu', 'B', 6.5)
            else:
                pdf.set_font('DejaVu', '', 6.5)

            pdf.set_xy(x_start + ci * col_w, y_row)
            pdf.cell(col_w, max_h, cell[:int(col_w / 2)], border=0, align=align, fill=fill)

    pdf.set_y(y_start + len(rows) * max_h + 2)
    return i


def markdown_to_pdf(input_path: Path | str, output_path: Path | str):
    """Convert a markdown file to a PDF."""
    input_path = Path(input_path) if isinstance(input_path, str) else input_path
    output_path = Path(output_path) if isinstance(output_path, str) else output_path
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Title block
    pdf.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    pdf.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')

    pdf.set_font('DejaVu', 'B', 16)
    pdf.set_text_color(30, 60, 114)
    pdf.cell(0, 12, 'Market Brief: April 2026 FOMC', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('DejaVu', '', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, 'Post-Meeting Landscape  |  May 24, 2026  |  Data as of May 22 Close', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(4)

    # Divider
    pdf.set_draw_color(30, 60, 114)
    pdf.set_line_width(0.5)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(4)

    lines = input_path.read_text(encoding='utf-8').split('\n')

    # Skip frontmatter (--- ... ---)
    content_start = 0
    in_frontmatter = False
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped == '---' and not in_frontmatter:
            in_frontmatter = True
            continue
        if stripped == '---' and in_frontmatter:
            content_start = idx + 1
            break

    i = content_start
    while i < len(lines):
        line = lines[i].rstrip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Check for page break
        if line.strip() == '---' and i > content_start:
            # Check if it's a horizontal rule separator
            # Check context: if previous line is a section header, use as section break
            prev_line = lines[i-1].rstrip() if i > 0 else ''
            if prev_line.startswith('## '):
                pdf.ln(3)
                pdf.set_draw_color(180, 180, 180)
                pdf.set_line_width(0.3)
                pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
                pdf.ln(3)
            else:
                pdf.ln(2)
            i += 1
            continue

        # Section headings (##)
        h_match = re.match(r'^(#{1,3})\s+(.+)$', line)
        if h_match:
            level = len(h_match.group(1))
            text = strip_span_tags(h_match.group(2))

            if level == 2:
                pdf.set_font('DejaVu', 'B', 13)
                pdf.set_text_color(30, 60, 114)
                pdf.ln(2)
                pdf.cell(0, 8, text, new_x='LMARGIN', new_y='NEXT')
                pdf.set_draw_color(30, 60, 114)
                pdf.set_line_width(0.3)
                pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + 40, pdf.get_y())
                pdf.ln(2)
            elif level == 3:
                pdf.set_font('DejaVu', 'B', 10)
                pdf.set_text_color(50, 80, 140)
                pdf.ln(1)
                pdf.cell(0, 6, text, new_x='LMARGIN', new_y='NEXT')
                pdf.ln(1)

            i += 1
            continue

        # Tables
        if line.startswith('|'):
            i = render_markdown_table(pdf, lines, i)
            continue

        # Bullet / numbered lists
        list_match = re.match(r'^(\s*[\-\*]|\s*\d+\.)\s+(.+)$', line)
        if list_match:
            text = strip_span_tags(list_match.group(2))
            pdf.set_font('DejaVu', '', 8)
            pdf.set_text_color(40, 40, 40)
            indent = list_match.group(0).index(list_match.group(1))
            bullet = list_match.group(1).strip()
            pdf.set_x(pdf.l_margin + min(indent * 2, 10))
            # Replace em dash
            text = text.replace('\u2014', '--').replace('\u2013', '-')
            # Truncate long lines
            while len(text) > 100:
                chunk = text[:100]
                last_space = chunk.rfind(' ')
                if last_space > 50:
                    chunk = chunk[:last_space]
                pdf.cell(0, 4.5, f'{bullet} {chunk}', new_x='LMARGIN', new_y='NEXT')
                pdf.set_x(pdf.l_margin + min(indent * 2 + 6, 12))
                text = text[len(chunk):].strip()
                bullet = ''
            pdf.cell(0, 4.5, f'{bullet} {text}', new_x='LMARGIN', new_y='NEXT')
            i += 1
            continue

        # Regular paragraph
        text = strip_span_tags(line)
        text = text.replace('\u2014', '--').replace('\u2013', '-')

        # Bold detection
        is_bold = text.startswith('**') and text.endswith('**')
        if is_bold:
            text = text.strip('*')

        pdf.set_font('DejaVu', 'B' if is_bold else '', 8)
        pdf.set_text_color(40, 40, 40)

        # Check if we should start a new paragraph
        prev_line = lines[i-1].rstrip() if i > 0 else ''
        if prev_line == '' and not is_bold:
            pdf.ln(1)

        pdf.multi_cell(0, 4.5, text)
        i += 1

    pdf.output(str(output_path))
    print(f'PDF generated: {output_path}')
    print(f'Size: {output_path.stat().st_size} bytes')
    return output_path


if __name__ == '__main__':
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('market-brief.md')
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else input_path.with_suffix('.pdf')
    markdown_to_pdf(input_path, output_path)