import re

def detect_fraud(text: str):
    issues = []

    # Check for GSTIN
    gstin_match = re.search(r'\b[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}\b', text)
    if not gstin_match:
        issues.append("Missing or invalid GSTIN")

    # Check for PAN
    pan_match = re.search(r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b', text)
    if not pan_match:
        issues.append("Missing or invalid PAN")

    # Check for invoice number
    if "Invoice No" not in text and "Invoice #" not in text:
        issues.append("Missing invoice number")

    # Check for suspicious amounts
    amount_match = re.findall(r'\₹?\$?\s?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', text)
    if amount_match:
        amounts = [float(a.replace(",", "")) for a in amount_match]
        if any(a == 0 or a > 100000 for a in amounts):
            issues.append("Suspicious amount detected")
    else:
        issues.append("No amount found")

    return issues
