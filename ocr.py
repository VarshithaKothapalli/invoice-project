import cv2
import pytesseract
from PIL import Image
import numpy as np
import io

def preprocess_image_bytes(image_bytes: bytes):
    # Read bytes into numpy array
    img_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if img is None:
        # Fallback via Pillow
        pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Resize up to help OCR on small text
    scale = 1.5
    resized = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    # Threshold (adaptive)
    thr = cv2.adaptiveThreshold(resized, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 31, 10)
    return thr

def extract_text_from_bytes(image_bytes: bytes) -> str:
    img_proc = preprocess_image_bytes(image_bytes)
    # Tesseract OCR
    config = "--oem 3 --psm 6"
    text = pytesseract.image_to_string(img_proc, config=config)
    return text.strip()