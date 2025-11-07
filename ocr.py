# ocr.py
from PIL import Image, UnidentifiedImageError, ImageFilter, ImageOps
import pytesseract
import io

# ✅ Set Tesseract path (required on Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image):
    """
    Enhance image for better OCR accuracy.
    - Convert to grayscale
    - Invert colors (optional)
    - Apply median filter to reduce noise
    - Binarize (thresholding)
    """
    image = image.convert("L")  # Grayscale
    image = ImageOps.invert(image)  # Invert colors
    image = image.filter(ImageFilter.MedianFilter())  # Denoise
    image = image.point(lambda x: 0 if x < 140 else 255)  # Binarize
    return image

def extract_text_from_bytes(image_bytes):
    """
    Extract text from image bytes using Tesseract OCR.
    Returns None if OCR fails or image is unreadable.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image = preprocess_image(image)
        # Optional: save for debugging
        # image.save("debug_image.png")
        text = pytesseract.image_to_string(image, config="--psm 6")
        print("🔍 OCR Output Preview:", text[:200])
        return text
    except UnidentifiedImageError:
        print("❌ Unrecognized image format")
        return None
    except Exception as e:
        print(f"❌ OCR failed: {e}")
        return None