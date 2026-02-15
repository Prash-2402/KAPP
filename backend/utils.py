import io
import re
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from fastapi import UploadFile
import pypdf
import pdfplumber
import pypdfium2 as pdfium
from pdfminer.high_level import extract_text as pdfminer_extract
from skills import SKILLS_LIST


# 🔥 Hardcode Tesseract location (bypass PATH issues)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 🔥 Set local Poppler path (for pdf2image)
# POPPLER_PATH = Path(__file__).parent / "poppler" / "poppler-24.08.0" / "Library" / "bin"


def _clean_text(text: str) -> str:
    """Helper function to clean extracted text."""
    return text.lower().strip()


def extract_text(file: UploadFile) -> Optional[str]:
    """
    Extract text from uploaded PDF file using robust methods.
    Primary: PyPDF2 (fast, text-based)
    Secondary: pypdfium2 (reliable, handles complex layouts)
    
    Returns:
        Cleaned text string or None if extraction fails.
    """
    try:
        # Read file content
        content = file.file.read()
        file.file.seek(0)  # Reset pointer for subsequent reads
        
        text = ""
        
        # Method 1: PyPDF2 (Standard Text Extraction)
        try:
            pdf_reader = pypdf.PdfReader(io.BytesIO(content))
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            # If we got a good amount of text, return it
            if len(text.strip()) > 100:
                print("✅ Extracted text using PyPDF2")
                return _clean_text(text)
                
        except Exception as e:
            print(f"⚠️ PyPDF2 extraction failed: {e}")

        # Method 2: pypdfium2 (Robust Layout/Text Extraction)
        try:
            print("🔄 Attempting backup extraction with pypdfium2...")
            
            # Use pypdfium2 to render text
            pdf = pdfium.PdfDocument(io.BytesIO(content))
            text = ""
            for i in range(len(pdf)):
                page = pdf[i]
                textpage = page.get_textpage()
                text += textpage.get_text_bounded() + "\n"
            
            if len(text.strip()) > 50:
                print("✅ Extracted text using pypdfium2")
                return _clean_text(text)
                
        except Exception as e:
             print(f"⚠️ pypdfium2 extraction failed: {e}")

        # Final check
        if not text.strip():
             return None
             
        return _clean_text(text)

    except Exception as e:
        print(f"❌ Critical Error in text extraction: {e}")
        return None


def extract_skills(text):

    detected = set()
    frequency = {}

    for skill in SKILLS_LIST:
        count = text.count(skill.lower())
        if count > 0:
            detected.add(skill)
            frequency[skill] = count

    return list(detected), frequency
