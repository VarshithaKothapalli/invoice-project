import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def explain_anomaly(anomaly_text):
    prompt = f"Explain why this invoice anomaly is risky: {anomaly_text}"
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text