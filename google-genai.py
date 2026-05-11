import os

from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")

# Create client
client = genai.Client(api_key=api_key)

# Gemini model
MODEL = "gemini-3-flash-preview"

# System instruction
SYSTEM_INSTRUCTION = (
    "You are a medieval knight who speaks in Old English."
)


def main():

    # Create a chat session with memory
    chat = client.chats.create(
        model=MODEL,
        config={
            'system_instruction': SYSTEM_INSTRUCTION
        }
    )

    print("Type 'quit' to exit.\n")

    while True:

        # User input
        user_input = input("You: ")

        if user_input.lower() == "quit":
            break

        print("\nAI: ", end="")

        # Send message to chat
        response = chat.send_message_stream(user_input)

        # Stream response
        for chunk in response:
            print(chunk.text, end='', flush=True)

        print("\n")


if __name__ == "__main__":
    main()