from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(
    inventory_value,
    health_score,
    critical_items,
    warehouse_status
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "AI Logistics Copilot - Executive Report",
        styles["Title"]
    )

    content.append(title)
    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"Inventory Value: €{inventory_value:,.0f}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Health Score: {health_score}/100",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Critical Items: {critical_items}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Warehouse Status: {warehouse_status}",
            styles["BodyText"]
        )
    )

    doc.build(content)

    buffer.seek(0)

    return buffer