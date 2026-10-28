
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API Key tidak ditemukan!")

client = genai.Client(api_key=api_key)

try:
    print("Daftar model Gemini:")

    for model in client.models.list():
        if "gemini" in model.name.lower():
            print(model.name)

finally:
    client.close()
