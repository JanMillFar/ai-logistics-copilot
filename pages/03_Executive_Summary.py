import streamlit as st
import pandas as pd

from utils.calculations import (
    calculate_inventory_value,
    calculate_days_left
)

st.set_page_config(
    page_title="Executive Summary",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Executive Summary")

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

inventory_value = (
    calculate_inventory_value(df)
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

health_score = round(
    (
        healthy_items
        / len(df)
    ) * 100,
    1
)

if st.button(
    "Generate Executive Summary"
):

    summary = f"""
# Warehouse Executive Report

## Inventory Overview

Total inventory value:
€{inventory_value:,.2f}

## Operational Status

Critical products:
{critical_items}

Warning products:
{warning_items}

Healthy products:
{healthy_items}

Inventory health score:
{health_score}%

## Main Recommendation

Prioritize replenishment of products
with less than 7 days of coverage.

## Conclusion

Warehouse operations remain stable,
but critical inventory items require
immediate attention.
"""

    st.markdown(summary)