import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Auto-select first available model that supports generateContent
try:
    MODEL_NAME = next(
        (m.name for m in genai.list_models() if "generateContent" in m.supported_generation_methods),
        "models/gemini-1.0-pro"  # fallback
    )
except Exception:
    MODEL_NAME = "models/gemini-1.0-pro"

def explain_flags_with_gemini(flags, invoice_text: str) -> str:
    """
    Returns a simple-language explanation of fraud flags using Gemini.
    If Gemini is unavailable, returns a rule-based fallback explanation.
    """
    if not flags:
        return "No fraud detected."

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"""
You are an auditor. Explain in simple language why the following fraud flags were raised.

Invoice text:
---
{invoice_text}
---

Fraud flags:
{flags}

Explain each flag clearly and briefly, focusing on practical reasons an auditor would care.
"""
        response = model.generate_content(prompt)
        return (response.text or "").strip() or "Explanation unavailable."

    except Exception as e:
        error_msg = str(e).lower()

        if "quota" in error_msg or "429" in error_msg:
            return rule_based_explanation(flags)
        elif "api_key" in error_msg or "no api key" in error_msg:
            return rule_based_explanation(flags)
        elif "not found" in error_msg or "404" in error_msg or "unsupported" in error_msg:
            return rule_based_explanation(flags)
        else:
            return rule_based_explanation(flags)

def rule_based_explanation(flags: list) -> str:
    """
    Generates a simple rule-based explanation for fraud flags.
    """
    explanations = {
        "missing_gstin": "GSTIN is missing, which is mandatory for tax compliance.",
        "duplicate_invoice": "This invoice appears to be a duplicate of a previously submitted one.",
        "amount_mismatch": "The total amount doesn't match the sum of line items.",
        "date_anomaly": "The invoice date is outside the expected billing cycle.",
        "vendor_not_registered": "The vendor is not listed in the approved vendor registry.",
        "invalid_format": "The invoice format doesn't match the expected template.",
    }

    output = ["Gemini is currently unavailable. Here's a rule-based explanation instead:\n"]
    for flag in flags:
        reason = explanations.get(flag, f"{flag.replace('_', ' ').capitalize()} may indicate irregularities.")
        output.append(f"- {reason}")
    return "\n".join(output)