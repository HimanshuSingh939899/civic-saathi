"""Civic Saathi Streamlit interface."""

import streamlit as st

from llm.response_generator import generate_response
from rag.retriever import get_retriever
from services.application_steps import get_application_steps
from services.document_checker import get_required_documents
from services.eligibility import check_eligibility

from ui.chat import render_chat
from ui.components import render_header, render_sidebar
from ui.services import get_service_prompt, service_names
from ui.state import clear_conversation, initialize_state
from ui.styles import apply_styles


st.set_page_config(
    page_title="Civic Saathi",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_styles()
initialize_state()


@st.cache_resource
def load_retriever():
    return get_retriever()


retriever = load_retriever()


selected_service = render_sidebar()

if selected_service == "__new_chat__":
    clear_conversation()
    st.rerun()

elif selected_service:
    st.session_state.selected_service = selected_service
    st.session_state.draft_question = get_service_prompt(selected_service)
    st.rerun()


render_header()

render_chat(retriever, generate_response)

st.markdown("---")

st.markdown(
    """
    <div class="section-heading">
        <div>
            <span class="section-kicker">QUICK LOOKUPS</span>
            <h2>Get focused information</h2>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Choose a service when you want a focused answer about steps, documents, or eligibility."
)

scheme_name = st.selectbox(
    "Scheme or service",
    service_names(),
)

steps_tab, documents_tab, eligibility_tab = st.tabs(
    ["Application steps", "Required documents", "Eligibility"]
)

with steps_tab:
    if st.button("Show application steps", key="steps_btn"):
        with st.spinner("Preparing the steps..."):
            st.session_state.last_lookup = get_application_steps(scheme_name)
            st.session_state.last_lookup_type = "steps"

    if (
        st.session_state.last_lookup
        and st.session_state.get("last_lookup_type") == "steps"
    ):
        st.markdown(st.session_state.last_lookup)

with documents_tab:
    if st.button("Show required documents", key="docs_btn"):
        with st.spinner("Preparing the document list..."):
            st.session_state.last_lookup = get_required_documents(scheme_name)
            st.session_state.last_lookup_type = "documents"

    if (
        st.session_state.last_lookup
        and st.session_state.get("last_lookup_type") == "documents"
    ):
        st.markdown(st.session_state.last_lookup)

with eligibility_tab:
    st.caption(
        "Describe the applicant in plain language for a quick document-based check."
    )

    applicant_text = st.text_area(
        "Applicant details",
        placeholder=(
            "For example: owns agricultural land, is not an income tax payer, "
            "and is not a government employee."
        ),
        label_visibility="collapsed",
    )

    if st.button("Check eligibility", key="elig_btn"):
        with st.spinner("Checking the available criteria..."):
            result = check_eligibility(
                scheme_name,
                applicant_details=applicant_text,
            )

        if isinstance(result, bool):
            st.success("Eligible" if result else "Not eligible")
        else:
            st.markdown(result)



