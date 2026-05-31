import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Risk Engine",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Inventory Risk Engine")

st.caption(
    "Automatic inventory risk assessment"
)

# Carregar dades
df = pd.read_csv("data/inventory.csv")

# Risk Score
df["RiskScore"] = (
    ((df["MinStock"] - df["Stock"])
     / df["MinStock"]) * 100
).clip(lower=0)

# Estat
def classify_risk(score):

    if score > 50:
        return "🔴 Critical"

    elif score > 20:
        return "🟡 Warning"

    return "🟢 Healthy"

df["Status"] = df["RiskScore"].apply(
    classify_risk
)

st.subheader("Inventory Risk Analysis")

st.dataframe(
    df[
        [
            "Product",
            "Stock",
            "MinStock",
            "RiskScore",
            "Status"
        ]
    ],
    use_container_width=True
)

st.divider()

highest_risk = df.sort_values(
    by="RiskScore",
    ascending=False
).iloc[0]

st.metric(
    "Highest Risk Item",
    highest_risk["Product"],
    f"{highest_risk['RiskScore']:.1f}%"
)

critical_count = len(
    df[df["RiskScore"] > 50]
)

warning_count = len(
    df[
        (df["RiskScore"] > 20)
        &
        (df["RiskScore"] <= 50)
    ]
)

healthy_count = len(
    df[df["RiskScore"] <= 20]
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "🔴 Critical",
    critical_count
)

col2.metric(
    "🟡 Warning",
    warning_count
)

col3.metric(
    "🟢 Healthy",
    healthy_count
)