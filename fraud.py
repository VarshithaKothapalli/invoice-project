import re

# In-memory duplicate tracking
_seen_invoice_numbers = set()

def reset_seen_invoices():
    _seen_invoice_numbers.clear()

def detect_fraud(text: str):
    """
    Returns a list of fraud flags based on regex/rule checks.
    """
    flags = []

    # Normalize
    content = text or ""
    content_lower = content.lower()

    # GSTIN (15 chars): 2 digits + 5 letters + 4 digits + 1 letter + 1 alphanum + 'Z' + 1 alphanum
    gstin_pattern = r"\b[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]\b"
    gstins = re.findall(gstin_pattern, content)
    if not gstins:
        flags.append("Missing or invalid GSTIN")

    # PAN (10 chars): 5 letters + 4 digits + 1 letter
    pan_pattern = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
    pans = re.findall(pan_pattern, content)
    if not pans:
        flags.append("Missing or invalid PAN")

    # Invoice number: look for label followed by alphanum/hyphen
    inv_label_pattern = r"\b(?:invoice\s*(?:no|number|#)?[:\-]?\s*)([A-Z0-9\-]+)\b"
    inv_matches = re.findall(inv_label_pattern, content, flags=re.IGNORECASE)
    invoice_number = inv_matches[0] if inv_matches else None

    if not invoice_number:
        flags.append("Missing invoice number")
    else:
        if invoice_number in _seen_invoice_numbers:
            flags.append(f"Duplicate invoice number detected: {invoice_number}")
        else:
            _seen_invoice_numbers.add(invoice_number)

    # Amounts: detect values like 1,234.56 or 12345 or ₹12,345.00
    amount_pattern = r"(?:₹|\$)?\s?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d+)"
    amounts_found = re.findall(amount_pattern, content)
    suspicious = False
    if not amounts_found:
        flags.append("No amount found")
    else:
        # Convert first sensible amount
        def parse_amt(x):
            try:
                return float(x.replace(",", ""))
            except:
                return None

        parsed = [parse_amt(a) for a in amounts_found]
        parsed = [p for p in parsed if p is not None]
        if parsed:
            amt = parsed[0]
            if amt == 0:
                suspicious = True
            if amt > 100000:
                suspicious = True
        else:
            flags.append("No parsable amount found")

        if suspicious:
            flags.append("Suspicious amount detected")

    return flags