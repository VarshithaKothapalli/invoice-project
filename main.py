from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ocr import extract_text_from_bytes
from fraud import detect_fraud   # ✅ Import fraud detection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process_invoice/")
async def process_invoice(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        text = extract_text_from_bytes(image_bytes)

        if not text or len(text.strip()) < 10:
            return {"filename": file.filename, "error": "OCR failed or empty"}

        # ✅ Run fraud detection
        issues = detect_fraud(text)

        return {
            "filename": file.filename,
            "text": text[:300],   # Show first 300 chars
            "fraud_flags": issues # ✅ Add fraud flags to response
        }
    except Exception as e:
        print(f"❌ Error processing {file.filename}: {e}")
        return {"filename": file.filename, "error": "Processing failed"}
