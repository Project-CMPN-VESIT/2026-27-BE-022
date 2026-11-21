from pathlib import Path
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(r'E:\web\IntelliTender')
SOURCE = ROOT / 'PROJECT_VIVA_PREP.md'
OUTPUT = ROOT / 'IntelliTender_Deep_Viva_Preparation.docx'

doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(.72)
sec.bottom_margin = Inches(.7)
sec.left_margin = Inches(.82)
sec.right_margin = Inches(.82)

styles = doc.styles
normal = styles['Normal']
normal.font.name = 'Aptos'
normal.font.size = Pt(10)
normal.font.color.rgb = RGBColor(42, 50, 61)
normal.paragraph_format.space_after = Pt(5)
normal.paragraph_format.line_spacing = 1.08

for name, size, color in [
    ('Title', 25, '16324F'),
    ('Heading 1', 19, '16324F'),
    ('Heading 2', 14, '087E8B'),
    ('Heading 3', 11, '16324F'),
]:
    st = styles[name]
    st.font.name = 'Aptos Display'
    st.font.size = Pt(size)
    st.font.bold = True
    st.font.color.rgb = RGBColor.from_string(color)
    st.paragraph_format.space_before = Pt(12 if name != 'Title' else 0)
    st.paragraph_format.space_after = Pt(5)
    st.paragraph_format.keep_with_next = True

styles['Title'].paragraph_format.space_after = Pt(7)
styles['Heading 1'].paragraph_format.page_break_before = False

footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
run = footer.add_run('IntelliTender Viva Preparation  |  ')
run.font.name = 'Aptos'
run.font.size = Pt(8)
run.font.color.rgb = RGBColor(100, 111, 124)
field = OxmlElement('w:fldSimple')
field.set(qn('w:instr'), 'PAGE')
footer._p.append(field)

def add_inline(p, text):
    parts = re.split(r'(\*\*.*?\*\*|\*.*?\*)', text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            r = p.add_run(part[2:-2]); r.bold = True
        elif part.startswith('*') and part.endswith('*'):
            r = p.add_run(part[1:-1]); r.italic = True
        else:
            p.add_run(part)

lines = SOURCE.read_text(encoding='utf-8').splitlines()
in_code = False
code_lines = []
first_title = True
i = 0
while i < len(lines):
    raw = lines[i]
    line = raw.strip()
    if line.startswith('```'):
        if not in_code:
            in_code = True; code_lines = []
        else:
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(.18)
            p.paragraph_format.right_indent = Inches(.12)
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(7)
            r = p.add_run('\n'.join(code_lines))
            r.font.name = 'Consolas'; r.font.size = Pt(8)
            r.font.color.rgb = RGBColor(55, 67, 78)
            in_code = False
        i += 1; continue
    if in_code:
        code_lines.append(raw); i += 1; continue
    if not line or line == '---':
        i += 1; continue
    if line.startswith('# '):
        title = line[2:].strip()
        if first_title:
            p = doc.add_paragraph(style='Title'); add_inline(p, title); first_title = False
        else:
            doc.add_heading(title, level=1)
        i += 1; continue
    if line.startswith('## '):
        doc.add_heading(line[3:].strip(), level=1); i += 1; continue
    if line.startswith('### '):
        qtitle = line[4:].strip()
        p = doc.add_paragraph(style='Heading 3')
        p.paragraph_format.keep_with_next = True
        add_inline(p, qtitle)
        i += 1; continue
    if line.startswith('> '):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(.22)
        add_inline(p, line[2:]); i += 1; continue
    if line.startswith('- '):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Inches(.28)
        p.paragraph_format.first_line_indent = Inches(-.15)
        add_inline(p, line[2:]); i += 1; continue
    if re.match(r'^\d+\.\s', line):
        p = doc.add_paragraph(style='List Number')
        p.paragraph_format.left_indent = Inches(.3)
        p.paragraph_format.first_line_indent = Inches(-.18)
        add_inline(p, re.sub(r'^\d+\.\s*', '', line)); i += 1; continue
    p = doc.add_paragraph()
    add_inline(p, line)
    i += 1

doc.core_properties.title = 'IntelliTender Deep Viva Preparation'
doc.core_properties.subject = 'Project architecture, AI integration, retrieval, document processing, scoring, limitations, and viva questions'
doc.core_properties.author = 'IntelliTender Project Team'
doc.save(OUTPUT)
print(OUTPUT)
