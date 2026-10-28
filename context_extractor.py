import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

EXTRACTION_PROMPT = """
You are an entity extraction system for a movie chatbot.

Extract movie-related entities explicitly mentioned
in the latest user message.

Return only these fields:
- current_movie
- current_director
- current_actor

Rules:
1. Only extract names explicitly mentioned by the user.
2. Do not infer missing names from movie knowledge.
3. Do not extract entities from previous messages.
4. Use null when an entity is not mentioned.
5. Return valid JSON only.
"""

def extract_context(user_message):
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY tidak ditemukan.")
    client = genai.Client(api_key=API_KEY)
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=EXTRACTION_PROMPT,
                response_mime_type="application/json",
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "current_movie": {
                            "type": "STRING",
                            "nullable": True
                        },
                        "current_director": {
                            "type": "STRING",
                            "nullable": True
                        },
                        "current_actor": {
                            "type": "STRING",
                            "nullable": True
                        }
                    },
                    "required": [
                        "current_movie",
                        "current_director",
                        "current_actor"
                    ]
                }
            )
        )
        if not response.text:
            raise ValueError("Gemini tidak menghasilkan JSON.")
        return json.loads(response.text)
    finally:
        client.close()