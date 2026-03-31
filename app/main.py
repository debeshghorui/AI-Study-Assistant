"""AI Study Assistant – Streamlit UI.

A clean, minimal interface that lets students paste their notes and use
AI-powered tools to summarize, simplify, or ask questions about them.
"""

import streamlit as st

from app.gemini_client import answer_question, explain_simply, summarize_notes

# Keep track of whether the user is in "Ask a Question" mode so the input
# remains visible across reruns while they type.
if "ask_mode" not in st.session_state:
    st.session_state.ask_mode = False

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------

st.markdown(
    """
    <style>
    .block-container { max-width: 820px; padding-top: 2rem; }
    .stTextArea textarea { font-size: 0.95rem; }
    div[data-testid="stMarkdownContainer"] h1 { text-align: center; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.title("📚 AI Study Assistant")
st.caption("Paste your notes below, then choose a tool to study smarter.")

st.divider()

# ---------------------------------------------------------------------------
# Notes input
# ---------------------------------------------------------------------------

notes = st.text_area(
    "Your Notes",
    height=220,
    placeholder="Paste or type your study notes here…",
)

st.divider()

# ---------------------------------------------------------------------------
# Feature buttons
# ---------------------------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    btn_summarize = st.button("📝 Summarize", use_container_width=True)

with col2:
    btn_explain = st.button("💡 Explain Simply", use_container_width=True)

with col3:
    btn_ask = st.button("❓ Ask a Question", use_container_width=True)

# Enter question mode when the button is pressed and keep it active for typing.
if btn_ask:
    st.session_state.ask_mode = True

# ---------------------------------------------------------------------------
# Question input (shown conditionally)
# ---------------------------------------------------------------------------

question = ""
btn_submit_question = False

if st.session_state.ask_mode:
    question = st.text_input(
        "Enter your question",
        placeholder="What would you like to know about your notes?",
    )
    btn_submit_question = st.button("Get Answer", use_container_width=True)

# ---------------------------------------------------------------------------
# Processing
# ---------------------------------------------------------------------------


def _validate_notes() -> bool:
    """Check that notes are not empty and show a warning if they are."""
    if not notes or not notes.strip():
        st.warning("Please enter your notes first.")
        return False
    return True


def _exit_ask_mode() -> None:
    """Hide the question input when another action is chosen."""
    st.session_state.ask_mode = False


if btn_summarize:
    _exit_ask_mode()
    if _validate_notes():
        with st.spinner("Summarizing your notes…"):
            result = summarize_notes(notes)
        st.subheader("📝 Summary")
        st.markdown(result)

if btn_explain:
    _exit_ask_mode()
    if _validate_notes():
        with st.spinner("Generating a simple explanation…"):
            result = explain_simply(notes)
        st.subheader("💡 Simple Explanation")
        st.markdown(result)

if btn_submit_question:
    if _validate_notes():
        if not question or not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Finding your answer…"):
                result = answer_question(notes, question)
            st.subheader("❓ Answer")
            st.markdown(result)
