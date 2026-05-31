import streamlit as st
import pandas as pd
import plotly.express as px

from utils.calculations import (
    calculate_days_left
)

from utils.health import (
    calculate_health_score,
    health_status
)

st.set_page_config(
    page_title="Inventory Health",
    page_icon="💚",
    layout="wide"
)

st.title("💚 Inventory Health Dashboard")

st.caption(
    "Global warehouse health monitoring"
)

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

status = health_status(
    health_score
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Inventory Health Score",
        f"{health_score}/100"
    )

with col2:

    st.metric(
        "Warehouse Status",
        status
    )

st.divider()

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

fig = px.pie(
    health_data,
    values="Count",
    names="Category",
    title="Inventory Health Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader(
    "Top 5 Products Requiring Attention"
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
            "Stock",
            "DailySales",
            "DaysLeft"
        ]
    ],
    use_container_width=True
)

st.divider()

st.subheader(
    "Operational Recommendations"
)

if critical_items > 0:

    st.error(
        f"""
        Immediate replenishment
        required for
        {critical_items}
        critical products.
        """
    )

if warning_items > 0:

    st.warning(
        f"""
        Review purchasing plans
        for
        {warning_items}
        products.
        """
    )

if critical_items == 0 and warning_items == 0:

    st.success(
        """
        Inventory levels are
        operating within
        acceptable limits.
        """
    )