import os
import requests
import google.generativeai as genai

# Load environment flags
USE_DEEPSEEK = os.getenv("USE_DEEPSEEK", "false").lower() == "true"
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Gemini setup
if GEMINI_API_KEY and not USE_DEEPSEEK:
    genai.configure(api_key=GEMINI_API_KEY)
    SUPPORTED_MODELS = [
        "gemini-pro",
        "models/gemini-pro",
        "models/gemini-1.5-pro-latest"
    ]

def explain_flags_with_gemini(fraud_flags: list, text: str) -> str:
    """
    Unified explanation function that routes to Gemini, DeepSeek, or fallback.
    Accepts fraud flags and invoice text separately.
    """
    prompt = build_prompt(fraud_flags, text)
    return get_explanation(prompt)

def get_explanation(prompt: str) -> str:
    try:
        if USE_DEEPSEEK:
            return call_deepseek(prompt)
        else:
            return call_gemini(prompt)
    except Exception as e:
        print(f"[LLM fallback] Error: {e}")
        return rule_based_explanation(prompt)

def call_gemini(prompt: str) -> str:
    for model in SUPPORTED_MODELS:
        try:
            llm = genai.GenerativeModel(model)
            response = llm.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"[Gemini error] Model {model} failed: {e}")
    raise RuntimeError("Gemini is currently unavailable.")

def call_deepseek(prompt: str) -> str:
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def rule_based_explanation(prompt: str) -> str:
    prompt_upper = prompt.upper()
    if "PAN" in prompt_upper:
        return "Missing or invalid PAN may indicate irregularities in tax compliance or vendor identity."
    elif "GSTIN" in prompt_upper:
        return "Invalid GSTIN format may suggest fake or unregistered tax IDs, which can trigger audit flags."
    elif "DUPLICATE" in prompt_upper:
        return "Duplicate invoice numbers may indicate accidental reprocessing or intentional fraud."
    elif "TOTAL MISMATCH" in prompt_upper:
        return "Mismatch between subtotal, taxes, and total may indicate calculation errors or manipulation."
    else:
        return "Anomaly detected. Please verify the invoice details manually."

def build_prompt(fraud_flags: list, text: str) -> str:
    flags_str = ", ".join(fraud_flags)
    return f"""You are an invoice fraud detection assistant.

Explain the following fraud flags in simple terms for a human reviewer:
- Flags: {flags_str}

Here is the invoice text:
{text}
"""