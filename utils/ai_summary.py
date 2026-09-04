from google import genai

from utils.gemini_config import (
    get_gemini_free_model,
    get_gemini_setting,
    is_gemini_free_enabled,
)


def generate_ai_summary(df):
    if not is_gemini_free_enabled():
        raise RuntimeError("Gemini Free is disabled to prevent unintended API charges.")

    api_key = get_gemini_setting("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=api_key)

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

    interaction = client.interactions.create(
        model=get_gemini_free_model(),
        input=prompt,
        store=False,
    )

    return interaction.output_text
