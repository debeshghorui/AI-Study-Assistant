"""Gemini API client module.

Provides a reusable interface for interacting with the Google Gemini API.
All AI logic is encapsulated here, keeping it separate from the UI layer.
"""

import os
import logging

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_API_KEY: str | None = os.getenv("GEMINI_API_KEY")

if _API_KEY:
    genai.configure(api_key=_API_KEY)
else:
    logger.warning("GEMINI_API_KEY is not set. API calls will fail.")

_MODEL_NAME = "gemini-2.0-flash"

# ---------------------------------------------------------------------------
# Core helper
# ---------------------------------------------------------------------------


def generate_response(prompt: str) -> str:
    """Send a prompt to Gemini and return the generated text.

    Args:
        prompt: The full prompt string to send to the model.

    Returns:
        The model's text response, or a user-friendly error message
        if something goes wrong.
    """
    if not _API_KEY:
        return "⚠️ Gemini API key is not configured. Please set GEMINI_API_KEY."

    try:
        model = genai.GenerativeModel(_MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except genai.types.BlockedPromptException:
        logger.error("Prompt was blocked by safety filters.")
        return "⚠️ The request was blocked by content safety filters. Please revise your input."
    except genai.types.StopCandidateException:
        logger.error("Response generation was stopped early.")
        return "⚠️ The response was stopped early due to safety settings."
    except Exception as exc:  # noqa: BLE001
        logger.exception("Gemini API call failed.")
        return f"⚠️ An error occurred while contacting the AI service: {exc}"


# ---------------------------------------------------------------------------
# Feature-specific prompts
# ---------------------------------------------------------------------------


def summarize_notes(notes: str) -> str:
    """Return a concise bullet-point summary of the provided notes."""
    prompt = (
        "You are a helpful study assistant. "
        "Summarize the following notes into clear, concise bullet points. "
        "Focus on the key concepts and important details.\n\n"
        f"Notes:\n{notes}"
    )
    return generate_response(prompt)


def explain_simply(notes: str) -> str:
    """Return a beginner-friendly explanation of the provided notes."""
    prompt = (
        "You are a friendly tutor explaining concepts to a complete beginner. "
        "Explain the following notes in simple, easy-to-understand language. "
        "Use analogies and examples where helpful. Avoid jargon.\n\n"
        f"Notes:\n{notes}"
    )
    return generate_response(prompt)


def answer_question(notes: str, question: str) -> str:
    """Answer a user question based on the provided notes."""
    prompt = (
        "You are a knowledgeable study assistant. "
        "Answer the following question based ONLY on the provided notes. "
        "If the answer cannot be found in the notes, say so clearly.\n\n"
        f"Notes:\n{notes}\n\n"
        f"Question:\n{question}"
    )
    return generate_response(prompt)
