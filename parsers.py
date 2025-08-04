import re
import PyPDF2
from docx import Document
from typing import Union

class ResumeParser:
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text

    @staticmethod
    def extract_text_from_docx(docx_path: str) -> str:
        doc = Document(docx_path)
        return "\n".join([para.text for para in doc.paragraphs])

    @staticmethod
    def extract_skills(text: str) -> list:
        # Common skills to look for (can be expanded)
        common_skills = [
            'python', 'java', 'javascript', 'c++', 'sql', 'machine learning',
            'deep learning', 'data analysis', 'project management', 'agile',
            'scrum', 'aws', 'azure', 'docker', 'kubernetes', 'tensorflow',
            'pytorch', 'flask', 'django', 'react', 'angular', 'vue', 'git'
        ]
        
        found_skills = []
        for skill in common_skills:
            if re.search(rf'\b{skill}\b', text, re.IGNORECASE):
                found_skills.append(skill.title())
        
        return found_skills

    @staticmethod
    def extract_experience(text: str) -> list:
        # Simple regex to find experience patterns
        experience_pattern = r'(\d+\+?\s*(years?|yrs?)\s*of?\s*experience)'
        matches = re.finditer(experience_pattern, text, re.IGNORECASE)
        return [match.group() for match in matches]

    @staticmethod
    def extract_education(text: str) -> list:
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'diploma']
        lines = text.split('\n')
        education = []
        for line in lines:
            if any(keyword in line.lower() for keyword in education_keywords):
                education.append(line.strip())
        return education

    def parse_resume(self, file_path: str) -> dict:
        if file_path.endswith('.pdf'):
            text = self.extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            text = self.extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format")

        return {
            'skills': self.extract_skills(text),
            'experience': self.extract_experience(text),
            'education': self.extract_education(text),
            'raw_text': text
        }