import streamlit as st
import pandas as pd
from fraud import detect_fraud, reset_seen_invoices
from ocr import extract_text_from_bytes
from gemini_helper import explain_flags_with_gemini

st.set_page_config(page_title="Invoice Fraud Detection Agent", layout="wide")
st.title("Invoice Fraud Detection Agent")

# Sidebar controls
with st.sidebar:
    st.markdown("### Controls")
    if st.button("Reset duplicate tracking"):
        reset_seen_invoices()
        st.success("Duplicate invoice memory cleared.")

    st.markdown("### Export")
    st.caption("Download CSV after processing files from the main panel.")

# Session storage
if "results" not in st.session_state:
    st.session_state["results"] = []

uploaded_files = st.file_uploader(
    "Upload invoice images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

def categorize_flags(flags):
    categories = {
        "GSTIN Issues": [],
        "PAN Issues": [],
        "Invoice Issues": [],
        "Amount Issues": [],
        "Other Issues": []
    }
    for flag in flags:
        if "GSTIN" in flag:
            categories["GSTIN Issues"].append(flag)
        elif "PAN" in flag:
            categories["PAN Issues"].append(flag)
        elif "invoice" in flag.lower():
            categories["Invoice Issues"].append(flag)
        elif "amount" in flag.lower():
            categories["Amount Issues"].append(flag)
        else:
            categories["Other Issues"].append(flag)
    return categories

# Main processing loop
if uploaded_files:
    for uploaded_file in uploaded_files:
        st.subheader(f"File: {uploaded_file.name}")
        text = extract_text_from_bytes(uploaded_file.read())

        col1, col2 = st.columns(2)
        with col1:
            st.text_area("Extracted text", text, height=220)
        fraud_flags = detect_fraud(text)

        with col2:
            if fraud_flags:
                st.error("Fraud flags:\n" + "\n".join(f"- {f}" for f in fraud_flags))
            else:
                st.success("No fraud detected")

            # Gemini explanation
            explanation = explain_flags_with_gemini(fraud_flags, text)
            st.info(f"Gemini explanation:\n{explanation}")

        # Categorize flags for structured CSV
        categories = categorize_flags(fraud_flags)
        st.session_state["results"].append({
            "filename": uploaded_file.name,
            "GSTIN Issues": ", ".join(categories["GSTIN Issues"]) or "None",
            "PAN Issues": ", ".join(categories["PAN Issues"]) or "None",
            "Invoice Issues": ", ".join(categories["Invoice Issues"]) or "None",
            "Amount Issues": ", ".join(categories["Amount Issues"]) or "None",
            "Other Issues": ", ".join(categories["Other Issues"]) or "None",
            "Gemini Explanation": explanation
        })

# Export + Analytics
if st.session_state["results"]:
    df = pd.DataFrame(st.session_state["results"])

    st.markdown("---")
    st.subheader("Download report")
    st.download_button(
        label="Download Fraud Report (CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="fraud_report.csv",
        mime="text/csv"
    )

    st.subheader("Analytics summary")
    issue_counts = {
        "GSTIN Issues": (df["GSTIN Issues"] != "None").sum(),
        "PAN Issues": (df["PAN Issues"] != "None").sum(),
        "Invoice Issues": (df["Invoice Issues"] != "None").sum(),
        "Amount Issues": (df["Amount Issues"] != "None").sum(),
        "Other Issues": (df["Other Issues"] != "None").sum(),
    }

    colA, colB = st.columns(2)
    with colA:
        st.write(f"Total invoices processed: {len(df)}")
        flagged_rows = (df[["GSTIN Issues","PAN Issues","Invoice Issues","Amount Issues","Other Issues"]] != "None").any(axis=1).sum()
        st.write(f"Invoices with at least one issue: {flagged_rows}")
        st.write(f"Clean invoices: {len(df) - flagged_rows}")

    with colB:
        st.bar_chart(issue_counts)