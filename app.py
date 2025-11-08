import streamlit as st
from fraud import detect_fraud, reset_seen_invoices
from ocr import extract_text_from_bytes

st.title("Invoice Fraud Detection Agent")

# ✅ Reset button
if st.button("Reset Duplicate Tracking"):
    reset_seen_invoices()
    st.success("Duplicate invoice memory cleared!")

uploaded_file = st.file_uploader("Upload an invoice image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    text = extract_text_from_bytes(uploaded_file.read())
    st.text_area("Extracted Text", text, height=200)

    fraud_flags = detect_fraud(text)
    if fraud_flags:
        st.error("⚠️ Fraud Flags:\n" + "\n".join(fraud_flags))
    else:
        st.success("✅ No fraud detected")