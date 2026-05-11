"""Small wrapper around Google's GenAI client.

This file encapsulates creating the client and starting a chat session.
It prefers `GOOGLE_API_KEY` but will fall back to application-default
credentials if available (e.g., via `GOOGLE_APPLICATION_CREDENTIALS`).
"""
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)

try:
    from google import genai
except Exception:
    genai = None


def create_client():
    """Return a configured genai.Client.

    Raises RuntimeError if the `google-genai` package is not installed or
    if client creation fails.
    """
    if genai is None:
        logger.error("google.genai package not available")
        raise RuntimeError("google.genai package not available. Install 'google-genai'.")

    api_key = os.getenv("GOOGLE_API_KEY")
    try:
        if api_key:
            logger.debug("Creating genai client using API key from env")
            return genai.Client(api_key=api_key)

        logger.debug("Creating genai client using application default credentials")
        return genai.Client()
    except Exception as e:
        logger.exception("Failed to create genai client: %s", e)
        raise RuntimeError("Failed to create Google GenAI client: %s" % e)


def create_chat(client, model="gemini-3-flash-preview", system_instruction=None):
    config = {}
    if system_instruction:
        config["system_instruction"] = system_instruction
    try:
        return client.chats.create(model=model, config=config)
    except Exception as e:
        logger.exception("Failed to create chat: %s", e)
        raise


def send_message_stream(chat, message):
    try:
        return chat.send_message_stream(message)
    except Exception as e:
        logger.exception("Failed to send message stream: %s", e)
        raise
