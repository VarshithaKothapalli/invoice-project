import streamlit as st
import pandas as pd
from fraud import detect_fraud, reset_seen_invoices
from ocr import extract_text_from_bytes

st.title("Invoice Fraud Detection Agent")

# ✅ Reset button
if st.button("Reset Duplicate Tracking"):
    reset_seen_invoices()
    st.success("Duplicate invoice memory cleared!")

# Store results across multiple uploads
if "results" not in st.session_state:
    st.session_state["results"] = []

# ✅ Multi-file uploader
uploaded_files = st.file_uploader(
    "Upload invoice images", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        text = extract_text_from_bytes(uploaded_file.read())
        st.text_area(f"Extracted Text - {uploaded_file.name}", text, height=200)

        fraud_flags = detect_fraud(text)
        if fraud_flags:
            st.error(f"⚠️ Fraud Flags for {uploaded_file.name}:\n" + "\n".join(fraud_flags))
        else:
            st.success(f"✅ No fraud detected in {uploaded_file.name}")

        # Save result in session
        st.session_state["results"].append({
            "filename": uploaded_file.name,
            "fraud_flags": ", ".join(fraud_flags) if fraud_flags else "None"
        })

# ✅ Export results as CSV
if st.session_state["results"]:
    df = pd.DataFrame(st.session_state["results"])
    st.download_button(
        label="Download Fraud Report (CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="fraud_report.csv",
        mime="text/csv"
    )
