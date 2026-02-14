from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from utils import extract_text, extract_skills
from orchestrator import run_orchestrator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Career Intelligence Engine Running"}

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):

    text = extract_text(file)

    if not text:
        return {"error": "Unable to extract text from resume."}

    skills, frequency = extract_skills(text)

    ai_result = run_orchestrator(skills, frequency)

    return {
        "detected_skills": skills,
        "analysis": ai_result
    }
