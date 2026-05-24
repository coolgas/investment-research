#!/usr/bin/env python3
"""Convert market-brief.md (with custom <span> tags) to a color-styled PDF."""

import re
import sys
from fpdf import FPDF
from bs4 import BeautifulSoup

# Color scheme
NAVY = (25, 35, 75)      # Key values / numbers
GREEN = (16, 128, 64)     # Positive / up
RED = (200, 40, 40)       # Negative / down
BLACK = (30, 30, 30)
GRAY = (100, 100, 100)
LIGHT_BG = (240, 242, 248)

def parse_spans_to_runs(text):
    """Parse HTML spans in text and return list of (text, color, bold) tuples."""
    soup = BeautifulSoup(f"<p>{text}</p>", 'html.parser')
    runs = []
    for el in soup.p.children:
        if isinstance(el, str):
            runs.append((str(el), None, False))
        elif el.name == 'span':
            cls = el.get('class', [''])[0]
            txt = el.get_text()
            if cls == 'num':
                runs.append((txt, NAVY, True))
            elif cls == 'up':
                runs.append((txt, GREEN, True))
            elif cls == 'down':
                runs.append((txt, RED, True))
            else:
                runs.append((txt, None, False))
    return runs


FONT_DIR = '/usr/share/fonts/truetype/liberation/'

class MarketBriefPDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.set_auto_page_break(auto=True, margin=20)
        # Register Unicode TTF fonts (Liberation Sans = metric-compatible Helvetica)
        self.add_font('LibSans', '', FONT_DIR + 'LiberationSans-Regular.ttf')
        self.add_font('LibSans', 'B', FONT_DIR + 'LiberationSans-Bold.ttf')
        self.add_font('LibSans', 'I', FONT_DIR + 'LiberationSans-Italic.ttf')
        self.add_font('LibSans', 'BI', FONT_DIR + 'LiberationSans-BoldItalic.ttf')

    def header(self):
        if self.page_no() > 1:
            self.set_font('LibSans', 'I', 8)
            self.set_text_color(*GRAY)
            self.cell(0, 5, 'Market Brief  |  April 2026 FOMC  |  Page %s' % self.page_no(), align='R', new_x='LMARGIN', new_y='NEXT')
            self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font('LibSans', 'I', 7)
        self.set_text_color(*GRAY)
        self.cell(0, 10, 'For informational purposes only. Not investment advice.', align='C')

    def section_title(self, title, level=1):
        self.ln(3)
        if level == 1:
            self.set_font('LibSans', 'B', 16)
            self.set_text_color(*NAVY)
            self.cell(0, 10, title, new_x='LMARGIN', new_y='NEXT')
        elif level == 2:
            self.set_font('LibSans', 'B', 13)
            self.set_text_color(*NAVY)
            self.cell(0, 8, title, new_x='LMARGIN', new_y='NEXT')
        elif level == 3:
            self.set_font('LibSans', 'B', 11)
            self.set_text_color(*NAVY)
            self.cell(0, 7, title, new_x='LMARGIN', new_y='NEXT')
        self.ln(1)

    def add_hr(self):
        self.set_draw_color(200, 200, 210)
        self.set_line_width(0.3)
        y = self.get_y()
        self.line(10, y, 200, y)
        self.ln(3)

    def write_colored_text(self, text):
        """Write a paragraph handling inline <span> tags."""
        runs = parse_spans_to_runs(text)
        self.set_font('LibSans', '', 9)
        for txt, color, bold in runs:
            if not txt.strip():
                continue
            style = 'B' if bold else ''
            self.set_font('LibSans', style, 9)
            if color:
                self.set_text_color(*color)
            else:
                self.set_text_color(*BLACK)
            w = self.get_string_width(txt)
            if self.get_x() + w > 190:
                self.ln()
            self.cell(w, 5.2, txt)
        self.ln(5)

    def write_plain_line(self, text):
        """Write a single plain line (for list items, plain text)."""
        self.set_font('LibSans', '', 9)
        self.set_text_color(*BLACK)
        # Strip any remaining span tags
        clean = re.sub(r'<[^>]+>', '', text)
        self.multi_cell(0, 5.2, clean)
        self.ln(1)

    def write_table(self, header_row, data_rows):
        """Write a table with colored cells."""
        col_count = len(header_row)
        col_w = 180 / max(col_count, 1)

        # Header
        self.set_font('LibSans', 'B', 8)
        self.set_fill_color(*NAVY)
        self.set_text_color(255, 255, 255)
        for h in header_row:
            self.cell(col_w, 6.5, h, border=1, fill=True, align='C')
        self.ln()

        # Data rows
        self.set_font('LibSans', '', 7.5)
        for row in data_rows:
            max_h = 6
            cells = []
            for cell in row:
                runs = parse_spans_to_runs(cell)
                cells.append(runs)
                h = 6
                for txt, _, _ in runs:
                    w = self.get_string_width(txt)
                    lines = max(1, -(-len(txt) * 7 // int(col_w - 2)))  # rough line count
                    h = max(h, 5.5 * lines)
                max_h = max(max_h, h)

            y_before = self.get_y()
            x_start = self.get_x()

            if y_before + max_h > 270:
                self.add_page()
                y_before = self.get_y()
                # Redraw header
                self.set_font('LibSans', 'B', 8)
                self.set_fill_color(*NAVY)
                self.set_text_color(255, 255, 255)
                for h in header_row:
                    self.cell(col_w, 6.5, h, border=1, fill=True, align='C')
                self.ln()
                y_before = self.get_y()
                self.set_font('LibSans', '', 7.5)

            self.set_fill_color(248, 249, 252)
            fill = False

            for i, runs in enumerate(cells):
                self.set_xy(x_start + i * col_w, y_before)
                # Draw cell background
                self.rect(x_start + i * col_w, y_before, col_w, max_h, style='D' if not fill else 'DF')
                self.set_fill_color(248, 249, 252)

                x_off = x_start + i * col_w + 1
                y_off = y_before + 0.5
                for txt, color, bold in runs:
                    style = 'B' if bold else ''
                    self.set_font('LibSans', style, 7.5)
                    if color:
                        self.set_text_color(*color)
                    else:
                        self.set_text_color(*BLACK)
                    w = self.get_string_width(txt)
                    if x_off + w > x_start + (i + 1) * col_w - 1:
                        y_off += 5
                        x_off = x_start + i * col_w + 1
                    self.set_xy(x_off, y_off)
                    self.cell(w, 5, txt)
                    x_off += w
                self.set_text_color(*BLACK)

            self.set_xy(x_start, y_before + max_h)
        self.ln(2)

    def add_disclaimer(self, text):
        self.set_font('LibSans', 'I', 7)
        self.set_text_color(*GRAY)
        clean = re.sub(r'<[^>]+>', '', text)
        self.multi_cell(0, 4, clean)


def convert_md_to_pdf(md_path, pdf_path):
    pdf = MarketBriefPDF()

    with open(md_path, 'r') as f:
        lines = f.readlines()

    # Skip YAML frontmatter
    content_lines = []
    in_frontmatter = False
    for line in lines:
        if line.strip() == '---':
            in_frontmatter = not in_frontmatter
            continue
        if not in_frontmatter:
            content_lines.append(line)

    content = ''.join(content_lines)
    paragraphs = content.strip().split('\n')

    pdf.add_page()

    # Title from first H1
    title_written = False

    i = 0
    while i < len(paragraphs):
        line = paragraphs[i]
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            i += 1
            continue

        # Horizontal rule
        if stripped == '---':
            pdf.add_hr()
            i += 1
            continue

        # Headings
        if stripped.startswith('## ') and not stripped.startswith('### '):
            pdf.section_title(stripped[3:], level=2)
            i += 1
            continue
        if stripped.startswith('### '):
            pdf.section_title(stripped[4:], level=3)
            i += 1
            continue
        if stripped.startswith('# ') and not title_written:
            pdf.section_title(stripped[2:], level=1)
            pdf.add_hr()
            title_written = True
            i += 1
            continue

        # Tables — detect by pipe character
        if '|' in stripped and stripped.startswith('|'):
            rows = []
            in_table = True
            while i < len(paragraphs) and paragraphs[i].strip().startswith('|'):
                rows.append(paragraphs[i].strip())
                i += 1
            if len(rows) >= 2:
                # Skip separator row (the |---| line)
                header = [c.strip() for c in rows[0].split('|') if c.strip()]
                data = []
                for r in rows[2:]:
                    cells = [c.strip() for c in r.split('|')]
                    # Remove first/last if empty (leading/trailing |)
                    if cells and cells[0] == '':
                        cells = cells[1:]
                    if cells and cells[-1] == '':
                        cells = cells[:-1]
                    data.append(cells)
                pdf.write_table(header, data)
            continue

        # Bullet points
        if stripped.startswith('- '):
            text = stripped[2:]
            pdf.write_colored_text('  \u2022 ' + text)
            i += 1
            continue

        if stripped.startswith('**') and stripped.endswith('**') and len(stripped) > 4:
            pdf.section_title(stripped.strip('*').strip(), level=3)
            i += 1
            continue

        # Numbered list
        if re.match(r'^\d+\.', stripped):
            pdf.write_colored_text(stripped)
            i += 1
            continue

        # Regular paragraph
        if '<span' in stripped or any(c in stripped for c in ['$', '%', '|']):
            pdf.write_colored_text(stripped)
        else:
            pdf.write_plain_line(stripped)
        i += 1

    pdf.output(pdf_path)
    return True


if __name__ == '__main__':
    md = sys.argv[1] if len(sys.argv) > 1 else 'market-brief.md'
    pdf_out = sys.argv[2] if len(sys.argv) > 2 else 'market-brief.pdf'
    convert_md_to_pdf(md, pdf_out)
    print(f"PDF generated: {pdf_out}")