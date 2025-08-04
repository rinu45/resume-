from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from parsers import ResumeParser
from job_analyzer import JobDescriptionAnalyzer
from ai_matcher import AIMatcher
import os
from typing import List
import uuid

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
resume_parser = ResumeParser()
job_analyzer = JobDescriptionAnalyzer()
ai_matcher = AIMatcher()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/analyze-job")
async def analyze_job_description(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, f"job_{uuid.uuid4()}.txt")
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Read file content
        with open(file_path, "r") as f:
            content = f.read()
        
        # Analyze job description
        requirements = job_analyzer.extract_requirements(content)
        
        return {
            "status": "success",
            "requirements": requirements
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        file_ext = os.path.splitext(file.filename)[1]
        file_path = os.path.join(UPLOAD_DIR, f"resume_{uuid.uuid4()}{file_ext}")
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Parse resume
        resume_data = resume_parser.parse_resume(file_path)
        
        return {
            "status": "success",
            "resume_data": resume_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/match")
async def match_resume_to_job(job_requirements: dict, resume_data: dict):
    try:
        # Calculate match score
        score = ai_matcher.calculate_match_score(resume_data, job_requirements)
        
        # Generate feedback
        feedback = ai_matcher.generate_feedback(resume_data, job_requirements)
        
        return {
            "status": "success",
            "match_score": score,
            "feedback": feedback
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)