import streamlit as st
import pandas as pd
import plotly.express as px
import io

from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

from google import genai

from utils.calculations import (
    calculate_inventory_value,
    calculate_days_left
)

from utils.health import (
    calculate_health_score,
    health_status
)
from utils.gemini_config import (
    get_gemini_free_model,
    get_gemini_setting,
    is_gemini_free_enabled,
)

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Logistics Copilot",
    page_icon="📦",
    layout="wide"
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Filters")

st.sidebar.header("Upload Data")

inventory_file = st.sidebar.file_uploader(
    "Inventory CSV",
    type=["csv"]
)

sales_file = st.sidebar.file_uploader(
    "Sales CSV",
    type=["csv"]
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:

    if inventory_file and sales_file:

        inventory = pd.read_csv(
            inventory_file
        )

        sales = pd.read_csv(
            sales_file
        )

    else:

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

    df["DaysLeft"] = calculate_days_left(
        df
    )

except Exception as e:

    st.error(
        f"Error loading data: {e}"
    )

    st.stop()

# --------------------------------------------------
# FILTERS
# --------------------------------------------------

categories = ["All"] + sorted(
    df["Category"].unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "Category",
    categories
)

if selected_category != "All":

    df = df[
        df["Category"]
        == selected_category
    ]

# --------------------------------------------------
# CALCULATIONS
# --------------------------------------------------

inventory_value = calculate_inventory_value(
    df
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

health_score = calculate_health_score(
    healthy_items,
    warning_items,
    critical_items
)

warehouse_status = health_status(
    health_score
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📦 AI Logistics Copilot")

st.markdown(
    """
### Operations Command Center

Monitor inventory performance,
detect operational risks,
forecast stock depletion,
and support purchasing decisions.
"""
)

st.divider()

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Inventory Value",
        f"€{inventory_value:,.0f}"
    )

with col2:

    st.metric(
        "Health Score",
        f"{health_score}/100"
    )

with col3:

    st.metric(
        "Critical Items",
        critical_items
    )

with col4:

    st.metric(
        "Warehouse Status",
        warehouse_status
    )

st.divider()

# --------------------------------------------------
# CHARTS
# --------------------------------------------------

left_col, right_col = st.columns([2, 1])

with left_col:

    fig_stock = px.bar(
        df.sort_values(
            "Stock",
            ascending=False
        ),
        x="Product",
        y="Stock",
        title="Current Inventory Levels"
    )

    st.plotly_chart(
        fig_stock,
        use_container_width=True
    )

with right_col:

    health_data = pd.DataFrame(
        {
            "Category": [
                "Healthy",
                "Warning",
                "Critical"
            ],
            "Count": [
                healthy_items,
                warning_items,
                critical_items
            ]
        }
    )

    fig_health = px.pie(
        health_data,
        values="Count",
        names="Category",
        title="Inventory Health"
    )

    st.plotly_chart(
        fig_health,
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# TOP RISKS
# --------------------------------------------------

st.subheader(
    "🚨 Top Inventory Risks"
)

top_risk = (
    df.sort_values(
        by="DaysLeft"
    )
    .head(5)
)

st.dataframe(
    top_risk[
        [
            "Product",
            "Category",
            "Stock",
            "DailySales",
            "DaysLeft"
        ]
    ],
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# FORECAST ALERTS
# --------------------------------------------------

st.subheader(
    "📈 Forecast Alerts"
)

forecast_alerts = df[
    df["DaysLeft"] < 21
]

if len(forecast_alerts) > 0:

    for _, row in (
        forecast_alerts
        .sort_values("DaysLeft")
        .iterrows()
    ):

        st.warning(
            f"""
{row['Product']}

Stock: {row['Stock']}

Daily Sales: {row['DailySales']}

Coverage Remaining:
{row['DaysLeft']} days
"""
        )

else:

    st.success(
        """
No forecast alerts detected.
Inventory coverage is healthy.
"""
    )

st.divider()

# --------------------------------------------------
# PDF REPORT
# --------------------------------------------------

st.subheader(
    "📄 Export Executive Report"
)

if st.button(
    "Generate PDF Report"
):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "AI Logistics Copilot Report",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 12)
    )

    story.append(
        Paragraph(
            f"Inventory Value: €{inventory_value:,.0f}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Health Score: {health_score}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Warehouse Status: {warehouse_status}",
            styles["BodyText"]
        )
    )

    doc.build(story)

    pdf = buffer.getvalue()

    st.download_button(
        "⬇ Download PDF",
        pdf,
        file_name="inventory_report.pdf",
        mime="application/pdf"
    )

st.divider()

# --------------------------------------------------
# GEMINI FREE AI ANALYSIS
# --------------------------------------------------

st.subheader(
    "🤖 AI Inventory Analysis"
)

gemini_key = get_gemini_setting("GEMINI_API_KEY")

if not is_gemini_free_enabled():

    st.info(
        "AI analysis is disabled until Gemini Free is explicitly enabled."
    )

elif gemini_key:

    if st.button(
        "Generate AI Analysis"
    ):

        client = genai.Client(api_key=gemini_key)

        summary = f"""
Inventory Value: {inventory_value}
Health Score: {health_score}
Critical Items: {critical_items}
Warning Items: {warning_items}
"""

        try:
            interaction = client.interactions.create(
                model=get_gemini_free_model(),
                input=("You are a logistics analyst.\n\n" + summary),
                store=False,
            )

            st.success(
                interaction.output_text
            )
        except Exception:
            st.error(
                "The AI analysis is temporarily unavailable. "
                "Check the Gemini Free configuration and try again."
            )

else:

    st.info(
        "Add GEMINI_API_KEY to Streamlit Secrets."
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.caption(
    "AI Logistics Copilot • Inventory Analytics Platform"
)
