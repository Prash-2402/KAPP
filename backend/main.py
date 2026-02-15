from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from utils import extract_text, extract_skills
from orchestrator import run_orchestrator
from section_extractor import extract_resume_sections
from agents.project_agent import analyze_projects
from agents.capability_agent import assess_capabilities
from agents.ai_grading_agent import grade_resume_with_ai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "KAPP Career Intelligence Engine v3.0 - AI-Powered Analysis 🤖"}

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
    
    # Step 1: Extract text from PDF
    text = extract_text(file)
    
    if not text:
        return {"error": "Unable to extract text from resume."}
    
    # Step 2: Extract structured sections
    print("📄 Extracting resume sections...")
    sections = extract_resume_sections(text)
    
    # Step 3: Extract skills
    print("🔍 Detecting skills...")
    skills, frequency = extract_skills(text)
    
    # Step 4: Analyze projects
    print("🚀 Analyzing projects...")
    project_analysis = analyze_projects(sections['projects'], text)
    
    # Step 5: Assess capabilities
    print("💪 Assessing skill capabilities...")
    capability_analysis = assess_capabilities(project_analysis, frequency)
    
    # Step 6: AI-POWERED GRADING 🤖
    print("🤖 AI-Powered Resume Grading...")
    resume_grade = grade_resume_with_ai(
        resume_text=text,
        detected_skills=skills,
        project_analysis=project_analysis,
        capability_analysis=capability_analysis
    )
    
    # Step 7: Run original orchestrator (enhanced with new data)
    print("🧠 Running career analysis orchestrator...")
    ai_result = run_orchestrator(skills, frequency)
    
    # Step 8: Combine all analyses
    print("✅ Analysis complete!")
    
    return {
        "detected_skills": skills,
        "analysis": ai_result,
        "project_analysis": project_analysis,
        "capability_analysis": capability_analysis,
        "resume_grade": resume_grade,
        "sections_analyzed": {
            "objective": sections['objective']['text'][:200] if sections['objective']['text'] else None,
            "projects_count": len(sections['projects']),
            "experience_count": len(sections['experience']),
            "education": sections['education']
        }
    }
