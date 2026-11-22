"""
Documentation Compiler Script.
Converts markdown project documentation into publication-grade downloadable formats:
1. Formatted Academic PDF (via ReportLab)
2. Microsoft Word Document (via python-docx)
"""

import sys
from pathlib import Path
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Paths
BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
OUTPUT_DIR = BASE_DIR / "output"
MD_FILE = DOCS_DIR / "comprehensive_project_documentation.md"
PDF_FILE = DOCS_DIR / "AI_Code_Complexity_Bug_Risk_Predictor_Documentation.pdf"
DOCX_FILE = DOCS_DIR / "AI_Code_Complexity_Bug_Risk_Predictor_Documentation.docx"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_docx():
    """Generates a Microsoft Word document (.docx) from markdown documentation."""
    import docx
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    doc = docx.Document()

    # Page Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Read markdown
    text = MD_FILE.read_text(encoding="utf-8")
    lines = text.splitlines()

    in_code_block = False
    code_lines = []
    in_table = False
    table_rows = []

    for line in lines:
        stripped = line.strip()

        # Handle Code Blocks
        if stripped.startswith("```"):
            if in_code_block:
                # Flush code block
                code_text = "\n".join(code_lines)
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Inches(0.3)
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(4)
                run = p.add_run(code_text)
                run.font.name = "Consolas"
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(30, 41, 59)
                in_code_block = False
                code_lines = []
            else:
                in_code_block = True
                code_lines = []
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        # Handle Tables
        if "|" in stripped and not stripped.startswith("#"):
            parts = [c.strip() for c in stripped.split("|")[1:-1]]
            if all(set(c).issubset({"-", ":", " "}) for c in parts):
                continue  # Divider line
            table_rows.append(parts)
            in_table = True
            continue
        else:
            if in_table and table_rows:
                # Flush table to document
                cols_count = max(len(r) for r in table_rows)
                tbl = doc.add_table(rows=len(table_rows), cols=cols_count)
                tbl.style = "Table Grid"
                for r_idx, row in enumerate(table_rows):
                    for c_idx, val in enumerate(row):
                        if c_idx < cols_count:
                            cell = tbl.cell(r_idx, c_idx)
                            cell.text = val
                            # Bold headers
                            if r_idx == 0:
                                for p in cell.paragraphs:
                                    for run in p.runs:
                                        run.font.bold = True
                                        run.font.size = Pt(9.5)
                            else:
                                for p in cell.paragraphs:
                                    for run in p.runs:
                                        run.font.size = Pt(9)
                doc.add_paragraph()  # spacer
                table_rows = []
                in_table = False

        if not stripped:
            continue

        # Headings
        if stripped.startswith("# "):
            h = doc.add_heading(level=0)
            run = h.add_run(stripped[2:])
            run.font.name = "Segoe UI"
            run.font.size = Pt(22)
            run.font.bold = True
            run.font.color.rgb = RGBColor(15, 23, 42)
        elif stripped.startswith("## "):
            h = doc.add_heading(level=1)
            run = h.add_run(stripped[3:])
            run.font.name = "Segoe UI"
            run.font.size = Pt(16)
            run.font.bold = True
            run.font.color.rgb = RGBColor(30, 58, 138)
        elif stripped.startswith("### "):
            h = doc.add_heading(level=2)
            run = h.add_run(stripped[4:])
            run.font.name = "Segoe UI"
            run.font.size = Pt(13)
            run.font.bold = True
            run.font.color.rgb = RGBColor(51, 65, 85)
        elif stripped.startswith("#### "):
            h = doc.add_heading(level=3)
            run = h.add_run(stripped[5:])
            run.font.name = "Segoe UI"
            run.font.size = Pt(11.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(71, 85, 105)
        elif stripped.startswith("- ") or stripped.startswith("* "):
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(2)
            _add_formatted_runs(p, stripped[2:])
        elif re.match(r"^\d+\.\s", stripped):
            match = re.match(r"^(\d+)\.\s+(.*)", stripped)
            p = doc.add_paragraph(style="List Number")
            p.paragraph_format.space_after = Pt(2)
            _add_formatted_runs(p, match.group(2))
        elif stripped.startswith("> "):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.3)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(stripped[2:])
            run.font.italic = True
            run.font.color.rgb = RGBColor(71, 85, 105)
        elif stripped == "---":
            continue
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            _add_formatted_runs(p, stripped)

    doc.save(DOCX_FILE)
    print(f"Generated Word Document: {DOCX_FILE}")


def _add_formatted_runs(paragraph, text: str):
    """Helper to parse bold markdown syntax into Word runs."""
    tokens = re.split(r"(\*\*.*?\*\*)", text)
    for tok in tokens:
        if tok.startswith("**") and tok.endswith("**"):
            r = paragraph.add_run(tok[2:-2])
            r.font.bold = True
            r.font.name = "Segoe UI"
            r.font.size = Pt(10)
        else:
            # Inline code check
            subtokens = re.split(r"(`.*?`)", tok)
            for subtok in subtokens:
                if subtok.startswith("`") and subtok.endswith("`"):
                    r = paragraph.add_run(subtok[1:-1])
                    r.font.name = "Consolas"
                    r.font.size = Pt(9.5)
                    r.font.color.rgb = RGBColor(30, 41, 59)
                else:
                    r = paragraph.add_run(subtok)
                    r.font.name = "Segoe UI"
                    r.font.size = Pt(10)


def generate_pdf():
    """Generates publication-grade PDF from markdown documentation using ReportLab."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
        Preformatted,
        HRFlowable,
        KeepTogether,
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    doc = SimpleDocTemplate(
        str(PDF_FILE),
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    # Typography styles
    doc_title_style = ParagraphStyle(
        "DocMainTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=6,
    )
    doc_subtitle_style = ParagraphStyle(
        "DocSubtitleStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569"),
        spaceAfter=12,
    )
    h1_style = ParagraphStyle(
        "Heading1Style",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13.5,
        leading=18,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True,
    )
    h2_style = ParagraphStyle(
        "Heading2Style",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )
    body_style = ParagraphStyle(
        "BodyTextStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4,
    )
    bullet_style = ParagraphStyle(
        "BulletTextStyle",
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3,
    )
    code_block_style = ParagraphStyle(
        "CodeStyle",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=3,
        spaceAfter=5,
    )
    table_cell = ParagraphStyle(
        "TCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0f172a"),
    )
    table_header = ParagraphStyle(
        "THeader",
        parent=table_cell,
        fontName="Helvetica-Bold",
        textColor=colors.white,
    )

    story = []

    text = MD_FILE.read_text(encoding="utf-8")
    lines = text.splitlines()

    in_code_block = False
    code_lines = []
    in_table = False
    table_rows = []

    for line in lines:
        stripped = line.strip()

        # Handle Code Blocks
        if stripped.startswith("```"):
            if in_code_block:
                code_text = "\n".join(code_lines)
                story.append(
                    Preformatted(
                        code_text,
                        code_block_style,
                        maxLineLength=90,
                    )
                )
                story.append(Spacer(1, 4))
                in_code_block = False
                code_lines = []
            else:
                in_code_block = True
                code_lines = []
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        # Handle Tables
        if "|" in stripped and not stripped.startswith("#"):
            parts = [c.strip() for c in stripped.split("|")[1:-1]]
            if all(set(c).issubset({"-", ":", " "}) for c in parts):
                continue
            table_rows.append(parts)
            in_table = True
            continue
        else:
            if in_table and table_rows:
                # Render table
                cols_count = max(len(r) for r in table_rows)
                formatted_rows = []
                for r_idx, row in enumerate(table_rows):
                    f_row = []
                    for c_idx, val in enumerate(row):
                        clean_val = val.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                        clean_val = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", clean_val)
                        clean_val = re.sub(r"`(.*?)`", r"<font face='Courier'>\1</font>", clean_val)
                        p_style = table_header if r_idx == 0 else table_cell
                        f_row.append(Paragraph(clean_val, p_style))
                    formatted_rows.append(f_row)

                # Available width = 612 - 80 = 532
                col_width = 532 / max(1, cols_count)
                t = Table(formatted_rows, colWidths=[col_width] * cols_count)
                t.setStyle(
                    TableStyle([
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                        ("TOPPADDING", (0, 0), (-1, -1), 3),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ])
                )
                story.append(t)
                story.append(Spacer(1, 6))
                table_rows = []
                in_table = False

        if not stripped:
            continue

        # Clean markdown formatting for reportlab XML
        clean_text = stripped.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        clean_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", clean_text)
        clean_text = re.sub(r"`(.*?)`", r"<font face='Courier'>\1</font>", clean_text)

        if stripped.startswith("# "):
            story.append(Paragraph(clean_text[2:], doc_title_style))
            story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=10))
        elif stripped.startswith("## "):
            story.append(Paragraph(clean_text[3:], h1_style))
        elif stripped.startswith("### "):
            story.append(Paragraph(clean_text[4:], h2_style))
        elif stripped.startswith("- ") or stripped.startswith("* "):
            story.append(Paragraph(f"• {clean_text[2:]}", bullet_style))
        elif re.match(r"^\d+\.\s", stripped):
            story.append(Paragraph(clean_text, bullet_style))
        elif stripped == "---":
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceAfter=6, spaceBefore=4))
        else:
            story.append(Paragraph(clean_text, body_style))

    doc.build(story)
    print(f"Generated PDF Document: {PDF_FILE}")

    # Copy to output/ directory as well
    import shutil
    shutil.copy(PDF_FILE, OUTPUT_DIR / PDF_FILE.name)
    shutil.copy(DOCX_FILE, OUTPUT_DIR / DOCX_FILE.name)
    print(f"Copied downloadable files to {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_docx()
    generate_pdf()
