"""
pdf_generator.py – ResumeForge Pro
Generates professional resumes with all user data.
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas

# ── Themes ────────────────────────────────────────────────────────────────────
THEMES = {
    "Classic Green": {"primary": "#1D9E75", "light": "#E1F5EE", "dark": "#085041"},
    "Corporate Blue": {"primary": "#185FA5", "light": "#E6F1FB", "dark": "#042C53"},
    "Creative Purple": {"primary": "#533AB7", "light": "#EEEDFE", "dark": "#26215C"},
}

def _hex(h):
    h = h.lstrip("#")
    return colors.Color(int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255)

PAGE_W, PAGE_H = A4
LM, RM, TM, BM = 15*mm, 15*mm, 10*mm, 15*mm
BODY_W = PAGE_W - LM - RM

def _style(name, font="Helvetica", size=10, color="#111111", leading=None, align=TA_LEFT, sb=0, sa=0):
    return ParagraphStyle(
        name,
        fontName=font,
        fontSize=size,
        textColor=_hex(color) if isinstance(color, str) else color,
        leading=leading or size * 1.4,
        alignment=align,
        spaceBefore=sb,
        spaceAfter=sa,
    )

# ── RESUME GENERATOR ─────────────────────────────────────────────────────────
def generate_resume_pdf(data):
    buf = io.BytesIO()
    theme = THEMES.get(data.get("theme", "Classic Green"), THEMES["Classic Green"])
    PRIMARY = _hex(theme["primary"])
    LIGHT = _hex(theme["light"])
    DARK = _hex(theme["dark"])

    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=LM, rightMargin=RM,
        topMargin=TM, bottomMargin=BM,
    )

    story = []

    # ── Header ──
    name = data.get("name", "Your Name").strip() or "Your Name"
    title = data.get("title", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    location = data.get("location", "").strip()
    linkedin = data.get("linkedin", "").strip()

    contact_parts = [p for p in [email, phone, location, linkedin] if p]
    contact = " · ".join(contact_parts)

    hdr_data = [[Paragraph(name, _style("Name", "Helvetica-Bold", 22, colors.white, 28))]]
    if title:
        hdr_data.append([Paragraph(title, _style("Title", size=12, color=colors.white, leading=16))])
    if contact:
        hdr_data.append([Paragraph(contact, _style("Contact", size=8.5, color=colors.white, leading=12))])

    hdr = Table(hdr_data, colWidths=[BODY_W])
    hdr.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), PRIMARY),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING", (0,0), (-1,-1), 16),
        ("RIGHTPADDING", (0,0), (-1,-1), 16),
    ]))
    story.append(hdr)
    story.append(Spacer(1, 6*mm))

    # ── Professional Summary ──
    summary = data.get("summary", "").strip()
    if summary:
        story.append(Paragraph("PROFESSIONAL SUMMARY", _style("Sec", "Helvetica-Bold", 10, PRIMARY, 12, sb=6, sa=2)))
        story.append(Paragraph(summary, _style("Summary", size=9.5, color="#333333", leading=14, sa=8)))
        story.append(Spacer(1, 3*mm))

    # ── Two Column Layout ──
    left_w = 55 * mm
    right_w = BODY_W - left_w - 8 * mm

    left_items = []
    right_items = []

    # ── Left Column ──
    # Skills
    skills = [s.strip() for s in (data.get("skills") or []) if s and s.strip()]
    if skills:
        left_items.append(("SEC", "SKILLS"))
        for sk in skills:
            left_items.append(("SKILL", sk.title()))
            left_items.append(("SPACER", 2))

    # Education
    degree = (data.get("degree", "") or "").strip()
    institution = (data.get("institution", "") or "").strip()
    year = (data.get("year", "") or "").strip()
    if degree or institution or year:
        left_items.append(("SPACER", 10))
        left_items.append(("SEC", "EDUCATION"))
        if degree:
            left_items.append(("BOLD", degree))
        inst_line = " · ".join(filter(None, [institution, year]))
        if inst_line:
            left_items.append(("MUTED", inst_line))

    # Languages
    languages = (data.get("languages", "") or "").strip()
    if languages:
        left_items.append(("SPACER", 10))
        left_items.append(("SEC", "LANGUAGES"))
        left_items.append(("MUTED", languages))

    # ── Right Column ──
    # Work Experience
    role = (data.get("role", "") or "").strip()
    company = (data.get("company", "") or "").strip()
    duration = (data.get("duration", "") or "").strip()
    exp_desc = (data.get("exp_desc", "") or "").strip()

    if role or company or duration or exp_desc:
        right_items.append(("SEC", "EXPERIENCE"))
        if role:
            right_items.append(("BOLD", role))
        co_line = " · ".join(filter(None, [company, duration]))
        if co_line:
            right_items.append(("MUTED", co_line))
        if exp_desc:
            right_items.append(("SPACER", 3))
            for line in exp_desc.split('\n'):
                if line.strip():
                    right_items.append(("BODY", line.strip()))

    # Projects
    projects = (data.get("projects", "") or "").strip()
    if projects:
        right_items.append(("SPACER", 10))
        right_items.append(("SEC", "PROJECTS"))
        for line in projects.split('\n'):
            if line.strip():
                right_items.append(("BODY", line.strip()))

    # Additional Experience (if any)
    add_exp = (data.get("add_exp", "") or "").strip()
    if add_exp:
        right_items.append(("SPACER", 10))
        right_items.append(("SEC", "ADDITIONAL EXPERIENCE"))
        for line in add_exp.split('\n'):
            if line.strip():
                right_items.append(("BODY", line.strip()))

    # ── Convert items to flowables ──
    def to_flowable(kind, val, col_w):
        if kind == "SPACER":
            return Spacer(1, float(val))
        elif kind == "SEC":
            return Paragraph(val.upper(), _style("Sec", "Helvetica-Bold", 8.5, PRIMARY, 11, sb=4, sa=2))
        elif kind == "BOLD":
            return Paragraph(val, _style("Bold", "Helvetica-Bold", 10, "#0f0f0f", 13))
        elif kind == "MUTED":
            return Paragraph(val, _style("Muted", size=8.5, color="#666666", leading=11))
        elif kind == "BODY":
            return Paragraph(f"• {val}", _style("Body", size=9.5, color="#333333", leading=13))
        elif kind == "SKILL":
            # Skill pill
            skill_style = _style("Skill", size=8.5, color=DARK, leading=11, align=TA_CENTER)
            pill = Table([[Paragraph(val, skill_style)]], colWidths=[col_w - 12])
            pill.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,-1), LIGHT),
                ("TOPPADDING", (0,0), (-1,-1), 4),
                ("BOTTOMPADDING", (0,0), (-1,-1), 4),
                ("LEFTPADDING", (0,0), (-1,-1), 8),
                ("RIGHTPADDING", (0,0), (-1,-1), 8),
            ]))
            return pill
        return Spacer(1, 1)

    left_flows = [to_flowable(k, v, left_w) for k, v in left_items]
    right_flows = [to_flowable(k, v, right_w) for k, v in right_items]

    # Pad to equal length
    n = max(len(left_flows), len(right_flows), 1)
    left_flows += [Spacer(1, 1)] * (n - len(left_flows))
    right_flows += [Spacer(1, 1)] * (n - len(right_flows))

    rows = [[l, r] for l, r in zip(left_flows, right_flows)]

    body = Table(rows, colWidths=[left_w, right_w], hAlign="LEFT")
    body.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING", (0,0), (-1,-1), 2),
        ("RIGHTPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING", (1,0), (1,-1), 12),
        ("LINEAFTER", (0,0), (0,-1), 0.5, _hex("#e0e0e0")),
    ]))
    story.append(body)

    doc.build(story)
    return buf.getvalue()
