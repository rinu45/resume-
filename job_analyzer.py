import re
from typing import List, Dict

class JobDescriptionAnalyzer:
    @staticmethod
    def extract_requirements(text: str) -> Dict:
        requirements = {
            'skills': [],
            'experience': None,
            'education': []
        }
        
        # Extract skills
        common_skills = [
            'python', 'java', 'javascript', 'c++', 'sql', 'machine learning',
            'deep learning', 'data analysis', 'project management', 'agile',
            'scrum', 'aws', 'azure', 'docker', 'kubernetes', 'tensorflow',
            'pytorch', 'flask', 'django', 'react', 'angular', 'vue', 'git'
        ]
        
        for skill in common_skills:
            if re.search(rf'\b{skill}\b', text, re.IGNORECASE):
                requirements['skills'].append(skill.title())
        
        # Extract experience requirements
        exp_pattern = r'(\d+\+?\s*(years?|yrs?)\s*of?\s*experience)'
        exp_match = re.search(exp_pattern, text, re.IGNORECASE)
        if exp_match:
            requirements['experience'] = exp_match.group()
        
        # Extract education requirements
        edu_keywords = ['bachelor', 'master', 'phd', 'degree', 'diploma']
        lines = text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in edu_keywords):
                requirements['education'].append(line.strip())
        
        return requirements