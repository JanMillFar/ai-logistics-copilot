from groq import Groq
from utils.groq_config import get_groq_model, get_groq_setting, is_groq_enabled


def generate_ai_summary(df):
    if not is_groq_enabled():
        raise RuntimeError("Groq is disabled to prevent API charges.")

    client = Groq(
        api_key=get_groq_setting("GROQ_API_KEY")
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
        model=get_groq_model(),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
