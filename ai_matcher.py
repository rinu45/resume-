import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class AIMatcher:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    def calculate_match_score(self, resume_data: dict, job_requirements: dict) -> float:
        prompt = f"""
        Analyze how well this resume matches the job requirements and provide a compatibility score from 0-100.
        
        Resume Details:
        - Skills: {', '.join(resume_data['skills'])}
        - Experience: {', '.join(resume_data['experience'])}
        - Education: {', '.join(resume_data['education'])}
        
        Job Requirements:
        - Required Skills: {', '.join(job_requirements['skills'])}
        - Required Experience: {job_requirements['experience']}
        - Required Education: {', '.join(job_requirements['education'])}
        
        Provide just the numerical score (0-100) and nothing else.
        """
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mixtral-8x7b-32768"
        )
        
        try:
            score = float(response.choices[0].message.content.strip())
            return min(max(score, 0), 100)  # Ensure score is between 0-100
        except:
            return 50  # Default score if parsing fails
    
    def generate_feedback(self, resume_data: dict, job_requirements: dict) -> str:
        prompt = f"""
        Analyze this resume against the job requirements and provide specific feedback:
        1. List the skills that match
        2. List the missing skills
        3. Compare experience levels
        4. Compare education requirements
        5. Provide 3 specific suggestions for improvement
        
        Resume Details:
        - Skills: {', '.join(resume_data['skills'])}
        - Experience: {', '.join(resume_data['experience'])}
        - Education: {', '.join(resume_data['education'])}
        
        Job Requirements:
        - Required Skills: {', '.join(job_requirements['skills'])}
        - Required Experience: {job_requirements['experience']}
        - Required Education: {', '.join(job_requirements['education'])}
        """
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mixtral-8x7b-32768"
        )
        
        return response.choices[0].message.content