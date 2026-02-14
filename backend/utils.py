import pdfplumber
from skills import SKILLS_LIST


def extract_text(file):
    text = ""
    try:
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
    except:
        pass
    return text.lower()


def extract_skills(text):

    detected = set()
    frequency = {}

    for skill in SKILLS_LIST:
        count = text.count(skill.lower())
        if count > 0:
            detected.add(skill)
            frequency[skill] = count

    return list(detected), frequency
