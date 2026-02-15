import io
from pathlib import Path
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
from pdfminer.high_level import extract_text as pdfminer_extract
from skills import SKILLS_LIST


# 🔥 Hardcode Tesseract location (bypass PATH issues)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 🔥 Set local Poppler path (for pdf2image)
POPPLER_PATH = Path(__file__).parent / "poppler" / "poppler-24.08.0" / "Library" / "bin"


def extract_text(file):

    text = ""
    file_bytes = file.file.read()

    # ---------------------------
    # 1️⃣ Try Native PDF Extraction (pdfplumber)
    # ---------------------------
    try:
        file.file.seek(0)
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
        print(f"✓ pdfplumber extracted {len(text)} characters")
    except Exception as e:
        print("✗ pdfplumber failed:", e)

    # ---------------------------
    # 2️⃣ Fallback → pdfminer
    # ---------------------------
    if len(text.strip()) < 100:
        try:
            file.file.seek(0)
            pdfminer_text = pdfminer_extract(io.BytesIO(file_bytes))
            if len(pdfminer_text.strip()) > len(text.strip()):
                text = pdfminer_text
                print(f"✓ pdfminer extracted {len(text)} characters")
        except Exception as e:
            print("✗ pdfminer failed:", e)

    # ---------------------------
    # 3️⃣ Final Fallback → OCR (for image-based PDFs)
    # ---------------------------
    if len(text.strip()) < 100:
        print("⚠ Minimal text detected. Attempting OCR extraction...")
        try:
            images = convert_from_bytes(file_bytes, poppler_path=str(POPPLER_PATH))
            ocr_text = ""
            for i, img in enumerate(images):
                page_text = pytesseract.image_to_string(img)
                ocr_text += page_text
                print(f"  → OCR page {i+1}: {len(page_text)} characters")
            
            if len(ocr_text.strip()) > len(text.strip()):
                text = ocr_text
                print(f"✓ OCR extraction successful! Total: {len(text)} characters")
        except FileNotFoundError as e:
            print("✗ OCR failed: Poppler not found!")
            print("  Install Poppler from: https://github.com/oschwartz10612/poppler-windows/releases")
            print("  Or set poppler_path in convert_from_bytes()")
        except Exception as e:
            print(f"✗ OCR failed: {e}")

    return text.lower().strip()


def extract_skills(text):

    detected = set()
    frequency = {}

    for skill in SKILLS_LIST:
        count = text.count(skill.lower())
        if count > 0:
            detected.add(skill)
            frequency[skill] = count

    return list(detected), frequency
