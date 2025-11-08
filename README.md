# Invoice OCR + Fraud Detection Agent

## 🚀 Overview
This agentic AI system automates invoice auditing by extracting key fields from scanned invoices and flagging anomalies like duplicate invoice numbers, invalid GST/VAT IDs, and mismatched totals. It combines OCR, fraud detection logic, and Gemini-based explanations to support finance teams in preventing fraud.

## 🎯 Problem Statement
Companies process thousands of invoices monthly. Manual audits often miss duplicates, fake entries, or invalid tax IDs, leading to financial losses. This agent automates detection and explanation of such anomalies using a modular, explainable AI pipeline.

## 🧠 Features
- OCR extraction using Tesseract or Huggingface Donut
- Fraud detection via regex validation, duplicate checks, and amount mismatches
- Gemini-powered explanations with rule-based fallback
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
    ├── gemini_helper.py 
    ├── main.py 
    ├── app.py 
    ├── assets/ 
    │   ├── sample_invoices/ 
    │   └── synthetic_invoices.csv

## 📦 Dataset
Synthetic dataset created manually for testing:
- Fields: invoice number, vendor name, date, GST/VAT ID, amount
- Location: `assets/synthetic_invoices.csv`

## 🖼️ Sample Invoices
Scanned invoice images stored in `assets/sample_invoices/` for OCR testing.

## 🧠 Gemini Integration
- Uses Gemini API to explain fraud flags in natural language
- Handles quota errors, missing keys, and unsupported models gracefully
- Falls back to rule-based explanations when Gemini is unavailable

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/VarshithaKothapalli/invoice-project.git
cd invoice-fraud-agent