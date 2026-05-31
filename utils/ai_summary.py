from groq import Groq
import streamlit as st


def generate_ai_summary(df):

    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )

    inventory_snapshot = df[
        [
            "Product",
            "Category",
            "Stock",
            "DailySales",
            "DaysLeft"
        ]
    ].head(20)

    prompt = f"""
You are a Senior Supply Chain Consultant.

Analyze this inventory dataset and provide:

1. Executive Summary
2. Key Risks
3. Inventory Concerns
4. Recommended Actions

Inventory Data:

{inventory_snapshot.to_string()}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content