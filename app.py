import streamlit as st
import requests

st.title("Invoice Fraud Detection Agent")

uploaded_files = st.file_uploader(
    "Upload Invoice Images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        st.subheader(f"📄 {file.name}")
        response = requests.post(
            "http://localhost:8000/process_invoice/",
            files={"file": (file.name, file.getvalue(), file.type)}
        )
        result = response.json()

        if "error" in result:
            st.error(f"❌ {result['error']}")
        else:
            st.success("✅ Processed successfully")
            st.text_area("Extracted Text", result["text"], height=200)

            # ✅ Show fraud detection flags
            if result.get("fraud_flags"):
                st.warning("⚠️ Fraud Flags:")
                for issue in result["fraud_flags"]:
                    st.write(f"- {issue}")