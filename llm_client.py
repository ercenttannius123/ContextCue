
import os
import time
import random

from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

from context_tracker import format_context
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)

SYSTEM_PROMPT = """
You are ContextCue, a helpful movie discussion assistant.

Your task is to answer questions about movies,
directors, actors, plots, and related film topics.

Use the conversation history to understand
follow-up questions and contextual references.

For example:
User: Tell me about Interstellar.
User: Who directed it?

Understand that "it" refers to Interstellar.

Use the provided conversation context when relevant.

If the conversation context conflicts with newer
messages, prioritize the newer messages.

If the reference is ambiguous, ask for clarification.

If you are unsure about a movie fact,
do not invent information.

Provide clear, natural, and helpful responses.
"""
def generate_response(messages, context=None):
    if not API_KEY:
        raise ValueError(
            "GEMINI_API_KEY tidak ditemukan di file .env"
        )
    client = genai.Client(
        api_key=API_KEY,
        http_options=types.HttpOptions(
            timeout=30000,
            retry_options=types.HttpRetryOptions(
                attempts=1
            )
        )
    )
    try:
        contents = []
        for message in messages:
            role = (
                "model"
                if message["role"] == "assistant"
                else "user"
            )
            contents.append(
                types.Content(
                    role=role,
                    parts=[
                        types.Part.from_text(
                            text=message["content"]
                        )
                    ]
                )
            )
        context_instruction = (
            format_context(context)
            if context is not None
            else ""
        )
        full_system_prompt = (
            SYSTEM_PROMPT
            + "\n"
            + context_instruction
        )

        max_retries = 3
        response = None
        start_time = time.perf_counter()
        try:
            for attempt in range(max_retries):
                try:
                    print(
                        f"Gemini request attempt "
                        f"{attempt + 1}/{max_retries}",
                        flush=True
                    )
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=full_system_prompt
                        )
                    )
                    break
                except errors.ServerError as error:
                    if error.code not in (500, 502, 503, 504):
                        raise
                    if attempt == max_retries - 1:
                        raise
                    wait_time = (
                        (2 ** attempt)
                        + random.uniform(0, 0.5)
                    )
                    print(
                        f"Server error {error.code}. "
                        f"Retry dalam {wait_time:.2f} detik...",
                        flush=True
                    )
                    time.sleep(wait_time)
            if response is None or not response.text:
                raise ValueError(
                    "Gemini tidak menghasilkan respons teks."
                )
            return response.text
        finally:
            elapsed = time.perf_counter() - start_time
            print(
                f"Total request time: {elapsed:.2f} detik",
                flush=True
            )
    finally:
        client.close()