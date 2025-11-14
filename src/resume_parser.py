# 📄 RESUME PARSER
# Extracts skills and information from resume text

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class ResumeParser:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.skill_keywords = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust'],
            'web': ['html', 'css', 'react', 'angular', 'vue', 'django', 'flask', 'node.js', 'express', 'spring'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd'],
            'data_science': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'statistics'],
            'soft_skills': ['leadership', 'communication', 'teamwork', 'problem solving', 'analytical', 'agile', 'scrum']
        }
            # NEW: Cultural attribute keywords
        self.cultural_keywords = {
            'teamwork': ['team', 'collaborat', 'partner', 'work together', 'group project', 'cross-functional'],
            'innovation': ['innovati', 'creativ', 'initiative', 'think outside', 'new ideas', 'problem solv'],
            'work_environment': ['remote', 'work from home', 'wfh', 'office', 'on-site', 'hybrid', 'flexible work'],
            'work_pace': ['fast-paced', 'dynamic', 'rapid', 'startup', 'agile', 'stable', 'methodical', 'structured'],
            'customer_focus': ['customer', 'client focus', 'user experience', 'stakeholder', 'end user']
        }

        print("✅ Resume parser initialized!")
    
    def parse_resume_text(self, resume_text):
        """Parse resume text and extract structured information"""
        print(f"🔍 Parsing resume text ({len(resume_text)} characters)...")
        
        # Extract basic information
        extracted_info = {
            'name': self.extract_name(resume_text),
            'email': self.extract_email(resume_text),
            'phone': self.extract_phone(resume_text),
            'skills': self.extract_skills(resume_text),
            'experience': self.extract_experience(resume_text),
            'education': self.extract_education(resume_text),
            'summary': self.generate_summary(resume_text),
                   # NEW: Add cultural attributes
            'cultural_attributes': self.extract_cultural_attributes(resume_text)            
        }
        
        print(f"✅ Extracted: {extracted_info['name']} | {len(extracted_info['skills'])} skills | {extracted_info['experience']} years experience")
        
        return extracted_info
    
    def extract_name(self, text):
        """Extract candidate name (simple heuristic)"""
        # Look for patterns like "Name: John Smith" or at the beginning
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and not any(keyword in line.lower() for keyword in ['resume', 'cv', 'curriculum', 'vitae']):
                # Simple name pattern (2-3 words, title case)
                words = line.split()
                if 2 <= len(words) <= 3 and all(word[0].isupper() for word in words if word):
                    return line
        return "Unknown Candidate"
    
    def extract_email(self, text):
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group() if match else "email@example.com"
    
    def extract_phone(self, text):
        """Extract phone number"""
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        match = re.search(phone_pattern, text)
        return match.group() if match else "Phone not found"
    
    def extract_skills(self, text):
        """Extract skills from resume text"""
        text_lower = text.lower()
        found_skills = []
        
        # Check each skill category
        for category, skills in self.skill_keywords.items():
            for skill in skills:
                if skill in text_lower:
                    found_skills.append(skill)
        
        # Remove duplicates and return
        return list(set(found_skills))
    
    def extract_experience(self, text):
        """Extract years of experience (simple heuristic)"""
        # Look for patterns like "5 years", "3+ years", etc.
        experience_patterns = [
            r'(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yr',
            r'experience.*?(\d+)\+?\s*years?'
        ]
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                return max(int(match) for match in matches)
        
        return 2  # Default assumption
    
    def extract_education(self, text):
        """Extract education information"""
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college', 'b.sc', 'm.sc']
        lines = text.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in education_keywords):
                return line.strip()
        
        return "Education information not specified"
    
    def generate_summary(self, text):
        """Generate a candidate summary"""
        skills = self.extract_skills(text)
        experience = self.extract_experience(text)
        
        if skills:
            top_skills = skills[:4]  # Take top 4 skills
            summary = f"Professional with {experience} years of experience. Skilled in {', '.join(top_skills)}."
        else:
            summary = f"Experienced professional with {experience} years in the industry."
        
        return summary

    # New extract cultural attributes
    def extract_cultural_attributes(self, text):
        """Extract cultural fit attributes from resume text"""
        text_lower = text.lower()
        cultural_attributes = {}
    
        # Check each cultural category
        for attribute, keywords in self.cultural_keywords.items():
            matches = []
            for keyword in keywords:
                if keyword in text_lower:
                    matches.append(keyword)
        
            # Calculate score based on percentage of keywords found
            if matches:
                score = len(matches) / len(keywords)
            else:
                score = 0.0  # No matches found
            
            cultural_attributes[attribute] = score

        return cultural_attributes

    def parse_resume_to_candidate(self, resume_text, candidate_name=None):
        """Convert parsed resume into candidate format for database"""
        parsed_data = self.parse_resume_text(resume_text)
        
        candidate_data = {
            "name": candidate_name or parsed_data['name'],
            "profile": parsed_data['summary'],
            "skills": parsed_data['skills'],
            "experience_years": parsed_data['experience'],
            "location": "Location not specified",  # Could extract from text
            "email": parsed_data['email'],
            "phone": parsed_data['phone'],
            "education": parsed_data['education'],
            "cultural_attributes": parsed_data['cultural_attributes']  # NEW       }
        }
        return candidate_data

def main():
    """Test the resume parser"""
    parser = ResumeParser()
    
    # Sample resume text
    sample_resume = """
    JOHN SMITH
    Email: john.smith@email.com
    Phone: (555) 123-4567
    
    EXPERIENCE:
    Senior Python Developer - TechCorp Inc (2018-Present)
    - Developed web applications using Django and Flask
    - Built REST APIs and managed PostgreSQL databases
    - Led a team of 3 developers using Agile methodology
    
    Python Developer - StartupXYZ (2015-2018)
    - Created data analysis tools with pandas and numpy
    - Implemented machine learning models with scikit-learn
    
    SKILLS:
    Python, Django, Flask, JavaScript, React, SQL, AWS, Docker, Machine Learning
    
    EDUCATION:
    Bachelor of Science in Computer Science - University of Technology
    """
    
    print("🧪 TESTING RESUME PARSER")
    print("=" * 50)
    
    parsed = parser.parse_resume_text(sample_resume)
    
    print("\n📄 PARSED RESUME DATA:")
    print(json.dumps(parsed, indent=2))

if __name__ == "__main__":
    main()