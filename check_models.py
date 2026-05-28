import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("\nAvailable Gemini Models:\n")

for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(f"Model Name: {model.name}")
        print(f"Description: {model.description}")
        print("-" * 50)