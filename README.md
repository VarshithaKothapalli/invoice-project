# Invoice OCR + Fraud Detection Agent

## 🚀 Overview
This agentic AI system automates invoice auditing by extracting key fields from scanned invoices and flagging anomalies such as duplicate invoice numbers and invalid GST/VAT IDs. It combines OCR, fraud detection logic, and LLM-based explanations to support finance teams in preventing fraud.

## 🎯 Problem Statement
Companies process thousands of invoices monthly. Manual audits often miss duplicates, fake entries, or invalid tax IDs, leading to financial losses. This agent automates detection and explanation of such anomalies.

## 🧠 Features
- OCR extraction using Tesseract (or Huggingface Donut)
- Fraud detection via regex validation and duplicate checks
- RAG agent using Gemini for anomaly explanations
- Streamlit UI for uploading invoices and viewing fraud reports
- Risk scoring (Low, Medium, High)
- Modular FastAPI backend

## 🧰 Tech Stack
- Python
- Tesseract OCR / Huggingface Donut
- Gemini API
- FastAPI
- Streamlit
- pandas
- dotenv

## 📁 Project Structure
invoice-fraud-agent/ 
    ├── .env 
    ├── requirements.txt 
    ├── input.json 
    ├── output.json 
    ├── ocr.py 
    ├── fraud.py 
    ├── rag.py 
    ├── main.py 
    ├── app.py 
    ├── assets/ 
    │   └── sample_invoices/


## 📦 Dataset
Synthetic dataset created manually for testing:
- Fields: invoice number, vendor name, date, GST/VAT ID, amount
- Located at: `assets/synthetic_invoices.csv`

## 🖼️ Sample Invoices
Scanned invoice images stored in `assets/sample_invoices/` for OCR testing.

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/invoice-fraud-agent.git
cd invoice-fraud-agent