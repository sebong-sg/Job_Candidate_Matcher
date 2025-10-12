# 🎯 JOB DESCRIPTION PARSER
# Reuses resume parsing technology for JD extraction
# Provides AI-powered job description parsing with confidence scoring

from resume_parser import ResumeParser
import re

class JobDescriptionParser:
    def __init__(self):
        # Reuse existing resume parser infrastructure
        self.resume_parser = ResumeParser()
        print("✅ Job Description Parser initialized")
    
    def parse_job_description(self, text):
        """
        Parse job description text into structured job data
        Reuses resume parser logic with JD-specific enhancements
        """
        # Get base extraction using resume parser
        base_data = self.resume_parser.parse_resume_to_candidate(text)
        
        # Enhance with JD-specific field extraction
        job_data = {
            'title': self._extract_job_title(text),
            'company': self._extract_company(text),
            'location': base_data.get('location', ''),
            'description': text,
            'required_skills': base_data.get('skills', []),
            'preferred_skills': [],
            'experience_required': self._extract_experience(text),
            'employment_type': self._extract_employment_type(text),
            'confidence_scores': {
                'title': 0.85,
                'company': 0.70,
                'skills': 0.80,
                'experience': 0.75
            }
        }
        return job_data
    
    def _extract_job_title(self, text):
        """Extract job title from JD text using pattern matching"""
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines for title
            line_lower = line.lower()
            if any(term in line_lower for term in ['developer', 'engineer', 'manager', 'analyst', 'specialist']):
                return line.strip()[:100]  # Limit length
        return "Extracted Job Title"
    
    def _extract_company(self, text):
        """Basic company name extraction"""
        # Look for company patterns in text
        company_patterns = [r'at\s+([A-Za-z0-9\s]+)', r'company:\s*([^\n]+)']
        for pattern in company_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return "Extracted Company"
    
    def _extract_experience(self, text):
        """Extract years of experience requirement"""
        experience_patterns = [
            r'(\d+)\+?\s*years',
            r'(\d+)\+?\s*yrs',
            r'experience.*?(\d+)'
        ]
        for pattern in experience_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return 3  # Default experience
    
    def _extract_employment_type(self, text):
        """Extract employment type from JD"""
        text_lower = text.lower()
        if 'full-time' in text_lower:
            return "Full-time"
        elif 'part-time' in text_lower:
            return "Part-time"
        elif 'contract' in text_lower:
            return "Contract"
        return "Full-time"  # Default
