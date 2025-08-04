import streamlit as st
import requests
import os
from typing import List
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API endpoint
API_URL = "http://localhost:8000"

st.title("AI-Powered Resume Screening System")

# Initialize session state
if 'resumes' not in st.session_state:
    st.session_state.resumes = []
if 'job_reqs' not in st.session_state:
    st.session_state.job_reqs = None

# Job Description Section
st.header("1. Upload Job Description")
job_file = st.file_uploader("Upload Job Description (TXT)", type=["txt"])

if job_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        tmp.write(job_file.read())
        tmp_path = tmp.name
    
    try:
        response = requests.post(
            f"{API_URL}/analyze-job",
            files={"file": open(tmp_path, "rb")}
        )
        if response.status_code == 200:
            st.session_state.job_reqs = response.json()["requirements"]
            st.success("Job description analyzed successfully!")
            st.json(st.session_state.job_reqs)
        else:
            st.error(f"Error analyzing job description: {response.text}")
    except Exception as e:
        st.error(f"Failed to connect to API: {str(e)}")
    finally:
        os.unlink(tmp_path)

# Resume Upload Section
st.header("2. Upload Resumes")
resume_files = st.file_uploader(
    "Upload Resumes (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if resume_files and st.button("Analyze Resumes"):
    st.session_state.resumes = []
    for resume_file in resume_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume_file.name)[1]) as tmp:
            tmp.write(resume_file.read())
            tmp_path = tmp.name
        
        try:
            response = requests.post(
                f"{API_URL}/analyze-resume",
                files={"file": open(tmp_path, "rb")}
            )
            if response.status_code == 200:
                resume_data = response.json()["resume_data"]
                st.session_state.resumes.append(resume_data)
                st.success(f"Analyzed: {resume_file.name}")
            else:
                st.error(f"Error analyzing {resume_file.name}: {response.text}")
        except Exception as e:
            st.error(f"Failed to analyze {resume_file.name}: {str(e)}")
        finally:
            os.unlink(tmp_path)

# Matching Section
if st.session_state.job_reqs and st.session_state.resumes:
    st.header("3. Match Results")
    
    results = []
    for i, resume in enumerate(st.session_state.resumes):
        try:
            response = requests.post(
                f"{API_URL}/match",
                json={
                    "job_requirements": st.session_state.job_reqs,
                    "resume_data": resume
                }
            )
            if response.status_code == 200:
                result = response.json()
                results.append({
                    "score": result["match_score"],
                    "feedback": result["feedback"],
                    "resume_data": resume
                })
            else:
                st.error(f"Error matching resume {i+1}: {response.text}")
        except Exception as e:
            st.error(f"Failed to match resume {i+1}: {str(e)}")
    
    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Display results
    for i, result in enumerate(results):
        with st.expander(f"Resume {i+1} - Score: {result['score']:.1f}"):
            st.subheader("Resume Details")
            st.json(result["resume_data"])
            
            st.subheader("Feedback")
            st.write(result["feedback"])