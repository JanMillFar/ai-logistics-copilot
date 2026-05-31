import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Demand Forecast",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Demand Forecast Engine")

st.caption(
    "Inventory depletion prediction and replenishment planning"
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
    df["Stock"] /
    df["DailySales"]
)

def forecast_status(days):

    if days < 7:
        return "🔴 Critical"

    elif days < 21:
        return "🟡 Warning"

    return "🟢 Healthy"

df["ForecastStatus"] = (
    df["DaysLeft"]
    .apply(forecast_status)
)

st.subheader(
    "Stock Depletion Forecast"
)

st.dataframe(
    df[
        [
            "Product",
            "Stock",
            "DailySales",
            "DaysLeft",
            "ForecastStatus"
        ]
    ],
    use_container_width=True
)

st.divider()

highest_risk = (
    df.sort_values(
        by="DaysLeft"
    )
    .iloc[0]
)

st.metric(
    "Most Urgent Replenishment",
    highest_risk["Product"],
    f"{highest_risk['DaysLeft']:.1f} days left"
)

st.divider()

fig = px.bar(
    df.sort_values("DaysLeft"),
    x="Product",
    y="DaysLeft",
    title="Days Remaining Until Stock Depletion"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader(
    "Recommended Purchases"
)

recommendations = df[
    df["DaysLeft"] < 21
]

for _, row in recommendations.iterrows():

    suggested_qty = (
        row["DailySales"] * 30
    ) - row["Stock"]

    if suggested_qty > 0:

        st.warning(
            f"""
            {row['Product']}

            Current Stock: {row['Stock']}

            Estimated Days Left:
            {row['DaysLeft']:.1f}

            Suggested Purchase:
            {int(suggested_qty)} units
            """
        )