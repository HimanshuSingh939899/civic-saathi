"""Session-state helpers for the Streamlit interface."""

from typing import Any, Dict, List

import streamlit as st


DEFAULT_MESSAGES: List[Dict[str, Any]] = [
    {
        "role": "assistant",
        "content": (
            "Namaste 👋 I’m Civic Saathi. I can help you understand "
            "government services, required documents, eligibility, and "
            "application steps in simple language."
        ),
    }
]


def initialize_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = list(DEFAULT_MESSAGES)

    if "draft_question" not in st.session_state:
        st.session_state.draft_question = ""

    if "last_lookup" not in st.session_state:
        st.session_state.last_lookup = None

    if "last_lookup_type" not in st.session_state:
        st.session_state.last_lookup_type = None

    if "selected_service" not in st.session_state:
        st.session_state.selected_service = None


def add_message(
    role: str,
    content: str,
    sources: List[Dict[str, Any]] | None = None,
) -> None:
    st.session_state.messages.append(
        {
            "role": role,
            "content": content,
            "sources": sources or [],
        }
    )


def clear_conversation() -> None:
    st.session_state.messages = list(DEFAULT_MESSAGES)
    st.session_state.draft_question = ""
    st.session_state.last_lookup = None
    st.session_state.last_lookup_type = None
    st.session_state.selected_service = None


def conversation_history() -> List[Dict[str, Any]]:
    return st.session_state.messages[1:]
