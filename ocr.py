# ocr.py
from PIL import Image, UnidentifiedImageError
import pytesseract
import io
import cv2
import numpy as np

# ✅ Set Tesseract path (required on Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_bytes):
    """
    Enhance image for better OCR accuracy using OpenCV adaptive thresholding.
    """
    # Convert PIL image to OpenCV format
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    open_cv_image = np.array(image)

    # Convert to grayscale
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)

    # Adaptive thresholding (better than fixed threshold)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    # Convert back to PIL for Tesseract
    return Image.fromarray(thresh)

def extract_text_from_bytes(image_bytes):
    """
    Extract text from image bytes using Tesseract OCR.
    Includes fallback configs if first attempt fails.
    """
    try:
        image = preprocess_image(image_bytes)

        # First attempt with PSM 6 (block of text)
        text = pytesseract.image_to_string(image, config="--psm 6")

        # Fallback if text is too short
        if len(text.strip()) < 10:
            text = pytesseract.image_to_string(image, config="--psm 4")  # multi-column
        if len(text.strip()) < 10:
            text = pytesseract.image_to_string(image, config="--psm 11") # sparse text

        print("🔍 OCR Output Preview:", text[:200])
        return text
    except UnidentifiedImageError:
        print("❌ Unrecognized image format")
        return None
    except Exception as e:
        print(f"❌ OCR failed: {e}")
        return None