"""
Interactive dialog using Google's Generative AI.

Usage:
- copy `.env.example` to `.env` and set `GOOGLE_API_KEY` or
  set `GOOGLE_APPLICATION_CREDENTIALS` to a service account JSON path.
- run: `python main.py`
"""

import logging

from google_client import create_client, create_chat, send_message_stream

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = "You are a helpful assistant."
MODEL = "gemini-3-flash-preview"


def main():
    try:
        client = create_client()
    except RuntimeError as e:
        logger.error("Client initialization error: %s", e)
        print("Error: could not initialize Google client. Check credentials.")
        return

    try:
        chat = create_chat(
            client,
            model=MODEL,
            system_instruction=SYSTEM_INSTRUCTION
        )
    except Exception as e:
        logger.error("Failed to start chat: %s", e)
        print("Error: failed to start chat session.")
        return

    print("Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if user_input.strip().lower() == "quit":
            break

        print("\nAI: ", end="", flush=True)

        try:
            response_stream = send_message_stream(chat, user_input)

            for chunk in response_stream:
                text = getattr(chunk, "text", None)
                if text:
                    print(text, end="", flush=True)
                else:
                    print(str(chunk), end="", flush=True)

        except Exception as e:
            logger.exception("Error during request: %s", e)
            print("\nError: request failed. See logs for details.")

        print("\n")


if __name__ == "__main__":
    main()