import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# List models
models = genai.list_models()
print("Available models:")
for m in models:
    # Only print the name and description
    print(f"- {m.name} — {getattr(m, 'description', 'No description')}")
