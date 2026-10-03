"""Reusable visual components for Civic Saathi."""

from html import escape
from typing import Dict, Iterable, Optional

import streamlit as st

from ui.services import SERVICE_CATALOG


def render_header() -> None:
    st.markdown(
        """
        <section class="civic-hero">
            <div class="hero-orb hero-orb-one"></div>
            <div class="hero-orb hero-orb-two"></div>
            <div class="hero-content">
                <div class="civic-badge">
                    <span class="civic-badge-dot"></span>
                    AI-POWERED CITIZEN ASSISTANT
                </div>
                <h1>Civic Saathi</h1>
                <p class="civic-hero-tagline">Government services, made simple.</p>
                <p class="civic-hero-copy">
                    Ask about government services, documents, eligibility and
                    application steps in clear, simple language.
                </p>
                <div class="hero-pills">
                    <span>📚 Document grounded</span>
                    <span>💬 Simple answers</span>
                    <span>🎙️ Voice enabled</span>
                </div>
            </div>
            <div class="hero-emblem">CS</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_sources(sources: Iterable[Dict]) -> None:
    sources = list(sources)
    if not sources:
        return

    with st.expander(f"📚 Official sources ({len(sources)})", expanded=False):
        seen = set()

        for source in sources:
            source_name = str(source.get("source", "Official document"))
            if source_name in seen:
                continue

            seen.add(source_name)
            category = source.get("category", "")
            label = source_name.replace("\\", "/").split("/")[-1]

            st.markdown(
                f"""
                <div class="source-card">
                    <div class="source-icon">DOC</div>
                    <div>
                        <div class="source-kicker">Official document</div>
                        <strong>{escape(label)}</strong>
                        {f'<span>Category: {escape(str(category))}</span>' if category else ''}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_conversation(messages: Iterable[Dict]) -> None:
    for message in messages:
        with st.chat_message(message.get("role", "assistant")):
            st.markdown(message.get("content", ""))
            render_sources(message.get("sources", []))


def render_sidebar() -> Optional[str]:
    """Render clickable service buttons and return the selected service name."""
    selected = None

    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-logo">CS</div>
                <div>
                    <div class="sidebar-title">Civic Saathi</div>
                    <div class="sidebar-subtitle">Your AI guide to government services</div>
                </div>
            </div>
            <div class="sidebar-rule"></div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("＋  New Chat", use_container_width=True, type="secondary"):
            selected = "__new_chat__"

        st.markdown('<div class="sidebar-section-title">SERVICES</div>', unsafe_allow_html=True)

        for index, service in enumerate(SERVICE_CATALOG):
            if st.button(
                f'{service["icon"]}  {service["name"]}',
                key=f"service_{index}",
                use_container_width=True,
            ):
                selected = service["name"]

        st.markdown(
            """
            <div class="sidebar-status">
                <div class="status-dot"></div>
                <div>
                    <strong>Document grounded</strong>
                    <span>Answers are generated using documents available to Civic Saathi.</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return selected
