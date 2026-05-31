import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Purchase Planner",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Purchase Planner")

st.caption(
    "Inventory replenishment simulator"
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

product = st.selectbox(
    "Select Product",
    df["Product"]
)

selected = df[
    df["Product"] == product
].iloc[0]

purchase_qty = st.number_input(
    "Purchase Quantity",
    min_value=0,
    value=100,
    step=10
)

if st.button(
    "Calculate Purchase Impact"
):

    new_stock = (
        selected["Stock"]
        + purchase_qty
    )

    current_days = round(
        selected["Stock"]
        / selected["DailySales"],
        1
    )

    new_days = round(
        new_stock
        / selected["DailySales"],
        1
    )

    added_value = round(
        purchase_qty
        * selected["Price"],
        2
    )

    st.success(
        f"New Stock: {new_stock}"
    )

    st.info(
        f"Coverage: {current_days} → {new_days} days"
    )

    st.warning(
        f"Inventory Value Increase: €{added_value:,.2f}"
    )