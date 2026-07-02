from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch

import io
from datetime import datetime


def create_pdf(text):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch
    )

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER
    title_style.textColor = HexColor("#1f4e79")

    heading_style = styles["Heading2"]
    heading_style.spaceBefore = 18
    heading_style.spaceAfter = 8
    heading_style.textColor = HexColor("#0B5CAD")
    heading_style.textColor = HexColor("#1f4e79")

    body_style = styles["BodyText"]

    story = []

    story.append(Paragraph("AI Meeting Notes Report", title_style))

    story.append(
        Paragraph(
            datetime.now().strftime("Generated on %d %B %Y %H:%M"),
            body_style
        )
    )

    story.append(Spacer(1, 20))

    current_section = ""

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):

            current_section = line.replace("#", "").strip()

            story.append(Spacer(1, 12))

            story.append(
                Paragraph(current_section, heading_style)
            )

            story.append(Spacer(1, 6))

        else:

            line = (
    line.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("**", "")
        .replace("__", "")
        .replace("*", "")
        .replace("`", "")
)

            if line.startswith("*"):

                line = "• " + line[1:].strip()

            story.append(
                Paragraph(line, body_style)
            )

    doc.build(story)

    buffer.seek(0)

    return buffer