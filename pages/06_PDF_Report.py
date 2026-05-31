import streamlit as st
import pandas as pd

from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from utils.calculations import (
    calculate_inventory_value,
    calculate_days_left
)

from utils.health import (
    calculate_health_score
)

st.set_page_config(
    page_title="PDF Report",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Executive PDF Report")

inventory = pd.read_csv(
    "data/inventory.csv"
)

sales = pd.read_csv(
    "data/sales_history.csv"
)

df = inventory.merge(
    sales,
    on="Product"
)

df["DaysLeft"] = (
    calculate_days_left(df)
)

inventory_value = (
    calculate_inventory_value(df)
)

critical_items = len(
    df[df["DaysLeft"] < 7]
)

warning_items = len(
    df[
        (df["DaysLeft"] >= 7)
        &
        (df["DaysLeft"] < 21)
    ]
)

healthy_items = len(
    df[df["DaysLeft"] >= 21]
)

health_score = (
    calculate_health_score(
        healthy_items,
        warning_items,
        critical_items
    )
)

top_risks = (
    df.sort_values(
        by="DaysLeft"
    )
    .head(10)
)

if st.button(
    "Generate Executive Report"
):

    pdf_path = (
        "reports/executive_report.pdf"
    )

    doc = SimpleDocTemplate(
        pdf_path
    )

    styles = (
        getSampleStyleSheet()
    )

    content = []

    # ------------------------------------------------
    # COVER PAGE
    # ------------------------------------------------

    content.append(
        Paragraph(
            "AI Logistics Copilot",
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            "Executive Operations Report",
            styles["Heading1"]
        )
    )

    content.append(
        Spacer(1, 40)
    )

    content.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            styles["BodyText"]
        )
    )

    content.append(
        PageBreak()
    )

    # ------------------------------------------------
    # KPI SECTION
    # ------------------------------------------------

    content.append(
        Paragraph(
            "Inventory Overview",
            styles["Heading1"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            f"Inventory Value: €{inventory_value:,.2f}",
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
            f"Critical Products: {critical_items}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Warning Products: {warning_items}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Healthy Products: {healthy_items}",
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # ------------------------------------------------
    # TOP RISKS
    # ------------------------------------------------

    content.append(
        Paragraph(
            "Top Risk Products",
            styles["Heading1"]
        )
    )

    content.append(
        Spacer(1, 10)
    )

    for _, row in top_risks.iterrows():

        content.append(
            Paragraph(
                f"""
                {row['Product']}
                |
                Stock: {row['Stock']}
                |
                Daily Sales: {row['DailySales']}
                |
                Days Left: {row['DaysLeft']}
                """,
                styles["BodyText"]
            )
        )

    content.append(
        Spacer(1, 20)
    )

    # ------------------------------------------------
    # RECOMMENDATIONS
    # ------------------------------------------------

    content.append(
        Paragraph(
            "Purchase Recommendations",
            styles["Heading1"]
        )
    )

    content.append(
        Spacer(1, 10)
    )

    recommendations = df[
        df["DaysLeft"] < 21
    ]

    for _, row in recommendations.iterrows():

        suggested_qty = (
            row["DailySales"] * 30
        ) - row["Stock"]

        if suggested_qty > 0:

            content.append(
                Paragraph(
                    f"""
                    {row['Product']}
                    :
                    Suggested purchase
                    {int(suggested_qty)}
                    units.
                    """,
                    styles["BodyText"]
                )
            )

    content.append(
        Spacer(1, 20)
    )

    # ------------------------------------------------
    # CONCLUSION
    # ------------------------------------------------

    content.append(
        Paragraph(
            "Operational Assessment",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            f"""
            Current warehouse health score
            stands at {health_score}/100.

            Inventory monitoring identifies
            {critical_items} critical products
            requiring immediate attention.

            Purchasing actions should focus
            on products with less than
            21 days of coverage.

            Overall operational visibility
            remains strong through the
            AI Logistics Copilot platform.
            """,
            styles["BodyText"]
        )
    )

    doc.build(content)

    st.success(
        "Executive Report Generated"
    )

    with open(
        pdf_path,
        "rb"
    ) as file:

        st.download_button(
            label="📥 Download Executive Report",
            data=file,
            file_name="executive_report.pdf",
            mime="application/pdf"
        )