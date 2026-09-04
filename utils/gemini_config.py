import os

import streamlit as st


# This allowlist is intentionally narrow: it prevents a secret or environment
# variable from switching the app to a billed model by accident.
FREE_GEMINI_MODELS = {"gemini-3.8-flash"}
DEFAULT_GEMINI_MODEL = "gemini-3.8-flash"


def get_gemini_setting(name, default=None):
    """Read Streamlit Secrets first, then fall back to environment variables."""
    try:
        value = st.secrets.get(name)
    except Exception:
        value = None
    return value or os.getenv(name, default)


def is_gemini_free_enabled():
    value = str(get_gemini_setting("GEMINI_FREE_ENABLED", "false")).strip().lower()
    return value in {"1", "true", "yes", "on"}


def get_gemini_free_model():
    model = get_gemini_setting("GEMINI_FREE_MODEL", DEFAULT_GEMINI_MODEL)
    if model not in FREE_GEMINI_MODELS:
        raise RuntimeError(
            "Only the approved Gemini Free model is allowed. "
            "Review GEMINI_FREE_MODEL before enabling AI."
        )
    return model
