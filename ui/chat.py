"""Chat interface for Civic Saathi."""

import streamlit as st

from ui.state import add_message, conversation_history
from voice.speech_to_text import get_last_error, listen


def render_chat(retriever, generate_response) -> None:
    st.markdown(
        """
        <div class="section-heading">
            <div>
                <span class="section-kicker">CIVIC ASSISTANT</span>
                <h2>How can I help you today?</h2>
            </div>
            <span class="online-pill"><span></span> Online</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for message in st.session_state.messages:
        with st.chat_message(message.get("role", "assistant")):
            st.markdown(message.get("content", ""))
            _render_sources(message.get("sources", []))

    input_col, voice_col = st.columns([7, 1])

    with input_col:
        question = st.text_input(
            "Your question",
            value=st.session_state.draft_question,
            placeholder="Ask about Aadhaar, PAN, schemes, documents, eligibility...",
            label_visibility="collapsed",
            key="chat_question",
        )

    with voice_col:
        speak_clicked = st.button("🎙️", use_container_width=True, help="Speak your question")

    if speak_clicked:
        with st.spinner("Listening..."):
            spoken_text = listen()

        if spoken_text:
            st.session_state.draft_question = spoken_text
            st.rerun()
        else:
            st.warning(
                get_last_error()
                or "Voice input was not captured. Please try again or type your question."
            )

    ask_clicked = st.button(
        "Ask Civic Saathi  →",
        type="primary",
        use_container_width=True,
    )

    if ask_clicked:
        question = question.strip()

        if not question:
            st.warning("Please enter a question first.")
            return

        st.session_state.draft_question = question
        add_message("user", question)

        with st.spinner("Checking the available official documents..."):
            try:
                results = retriever.retrieve(question, k=5, min_score=0.3)
                answer = generate_response(
                    question,
                    results,
                    conversation_history=conversation_history(),
                )
            except Exception:
                st.error("The assistant is temporarily unavailable. Please try again.")
                return

        add_message("assistant", answer, results)
        st.rerun()


def _render_sources(sources) -> None:
    if not sources:
        return

    with st.expander(f"📚 Official sources ({len(sources)})", expanded=False):
        seen = set()

        for source in sources:
            source_name = str(source.get("source", "Official document"))
            if source_name in seen:
                continue

            seen.add(source_name)
            label = source_name.replace("\\", "/").split("/")[-1]
            category = source.get("category", "")

            st.markdown(f"**{label}**")
            if category:
                st.caption(f"Category: {category}")