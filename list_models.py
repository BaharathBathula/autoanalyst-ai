import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Models that support generateContent:")
for m in genai.list_models():
    # supported_generation_methods is available in this SDK
    methods = getattr(m, "supported_generation_methods", [])
    if "generateContent" in methods:
        print("-", m.name)
