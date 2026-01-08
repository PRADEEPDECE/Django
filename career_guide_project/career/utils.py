from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import re

def clean_markdown(text):
    text = re.sub(r"\*\*", "", text)
    text = re.sub(r"###", "", text)
    text = re.sub(r"---", "", text)
    return text

def generate_report_pdf(response, report):
    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="TitleStyle",
        fontSize=18,
        spaceAfter=20,
        alignment=1  # center
    ))
    styles.add(ParagraphStyle(
        name="HeaderStyle",
        fontSize=13,
        spaceBefore=14,
        spaceAfter=8,
        fontName="Helvetica-Bold"
    ))
    styles.add(ParagraphStyle(
        name="BodyStyle",
        fontSize=11,
        spaceAfter=8,
        leading=15
    ))

    story = []

    # Title
    story.append(Paragraph("Career Recommendation Report", styles["TitleStyle"]))

    # Meta
    story.append(Paragraph(
        f"<b>User:</b> {report.user.username}<br/>"
        f"<b>Date:</b> {report.created_at.strftime('%d-%m-%Y %H:%M')}",
        styles["BodyStyle"]
    ))

    # Input
    story.append(Paragraph("Input Details", styles["HeaderStyle"]))
    story.append(Paragraph(report.input_data, styles["BodyStyle"]))

    # Recommendation
    story.append(Paragraph("AI Career Recommendation", styles["HeaderStyle"]))

    cleaned = clean_markdown(report.recommendation)
    for para in cleaned.split("\n\n"):
        story.append(Paragraph(para, styles["BodyStyle"]))

    # Build PDF
    doc.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

def add_page_number(canvas, doc):
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(
        A4[0] - 50,
        30,
        f"Page {doc.page}"
    )
