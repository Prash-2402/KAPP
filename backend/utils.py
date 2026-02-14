import io
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
from pdfminer.high_level import extract_text as pdfminer_extract
from skills import SKILLS_LIST


# 🔥 Hardcode Tesseract location (bypass PATH issues)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


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
    except Exception as e:
        print("pdfplumber failed:", e)

    # ---------------------------
    # 2️⃣ Fallback → pdfminer
    # ---------------------------
    if not text.strip():
        try:
            file.file.seek(0)
            text = pdfminer_extract(io.BytesIO(file_bytes))
        except Exception as e:
            print("pdfminer failed:", e)

    # ---------------------------
    # 3️⃣ Final Fallback → OCR
    # ---------------------------
    if not text.strip():
        try:
            images = convert_from_bytes(file_bytes)
            for img in images:
                text += pytesseract.image_to_string(img)
        except Exception as e:
            print("OCR failed:", e)

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
