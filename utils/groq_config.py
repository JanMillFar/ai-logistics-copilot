import os

import streamlit as st


DEFAULT_GROQ_MODEL = "openai/gpt-oss-20b"


def get_groq_setting(name, default=None):
    """Read Streamlit Secrets first, then fall back to environment variables."""
    try:
        value = st.secrets.get(name)
    except Exception:
        value = None
    return value or os.getenv(name, default)


def get_groq_model():
    return get_groq_setting("GROQ_MODEL", DEFAULT_GROQ_MODEL)


def is_groq_enabled():
    value = str(get_groq_setting("GROQ_ENABLED", "false")).strip().lower()
    return value in {"1", "true", "yes", "on"}
