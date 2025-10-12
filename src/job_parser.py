# 🎯 JOB DESCRIPTION PARSER - Enhanced with Real Confidence Scoring
# Improved field extraction with dynamic confidence calculation

from resume_parser import ResumeParser
import re

class JobDescriptionParser:
    def __init__(self):
        self.resume_parser = ResumeParser()
        print("✅ Job Description Parser initialized")
    
    def parse_job_description(self, text):
        """
        Parse job description with real confidence scoring based on extraction quality
        """
        # Get base extraction using resume parser
        base_data = self.resume_parser.parse_resume_to_candidate(text)
        
        # Enhanced extraction with real confidence calculation
        title, title_confidence = self._extract_job_title(text)
        company, company_confidence = self._extract_company(text)
        location, location_confidence = self._extract_location(text)
        experience, exp_confidence = self._extract_experience(text)
        employment_type, type_confidence = self._extract_employment_type(text)
        
        job_data = {
            'title': title,
            'company': company,
            'location': location,
            'description': text,
            'required_skills': base_data.get('skills', []),
            'preferred_skills': [],
            'experience_required': experience,
            'employment_type': employment_type,
            'confidence_scores': {
                'title': title_confidence,
                'company': company_confidence,
                'location': location_confidence,
                'experience': exp_confidence,
                'skills': 0.80,  # Based on resume parser performance
                'employment_type': type_confidence
            }
        }
        return job_data
    
    def _extract_job_title(self, text):
        """Extract job title with confidence based on pattern matching"""
        lines = text.split('\n')
        
        # Look for title patterns in first few lines
        title_patterns = [
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+[Dd]eveloper)',
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+[Ee]ngineer)',
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+[Mm]anager)',
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+[Aa]nalyst)',
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+[Dd]esigner)',
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+[Ss]pecialist)'
        ]
        
        for i, line in enumerate(lines[:10]):  # Check first 10 lines
            line = line.strip()
            if not line:
                continue
                
            for pattern in title_patterns:
                match = re.search(pattern, line)
                if match:
                    title = match.group(1).strip()
                    # Higher confidence if found in first 3 lines
                    confidence = 0.95 if i < 3 else 0.85
                    return title, confidence
        
        # Fallback: look for any line with common title keywords
        for line in lines[:5]:
            if any(keyword in line.lower() for keyword in ['developer', 'engineer', 'manager', 'analyst', 'specialist', 'designer']):
                return line.strip()[:80], 0.75
                
        return "Job Title", 0.50
    
    def _extract_company(self, text):
        """Extract company name with confidence scoring"""
        # Common company patterns
        company_patterns = [
            r'at\s+([A-Z][A-Za-z0-9&\s]+?)(?:\s|\.|$|,)',
            r'[Cc]ompany:\s*([^\n,.]+)',
            r'[Oo]rganization:\s*([^\n,.]+)',
            r'([A-Z][A-Za-z0-9&\s]+)\s+is hiring',
            r'join\s+([A-Z][A-Za-z0-9&\s]+)'
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                company = match.group(1).strip()
                # Clean up common issues
                company = re.sub(r'\s*(?:is|looking|seeking|hiring).*$', '', company, flags=re.IGNORECASE)
                if len(company) > 3 and len(company) < 50:  # Reasonable length
                    return company, 0.85
        
        # Look for company-like words in first paragraph
        first_para = text.split('\n\n')[0] if '\n\n' in text else text.split('\n')[0]
        words = first_para.split()
        for i, word in enumerate(words):
            if word.istitle() and len(word) > 2:
                # Check if it looks like a company name (not a common word)
                if not word.lower() in ['the', 'and', 'for', 'with', 'this', 'that']:
                    return word, 0.65
                    
        return "Company", 0.40
    
    def _extract_location(self, text):
        """Extract location with confidence"""
        location_patterns = [
            r'[Ll]ocation:\s*([^\n,.]+)',
            r'[Bb]ased in\s+([^\n,.]+)',
            r'[Rr]emote',
            r'[Hh]ybrid',
            r'[Oo]nsite',
            r'in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)(?:\s|\.|$)'
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                location = matches[0] if isinstance(matches[0], str) else 'Remote'
                if location.lower() in ['remote', 'hybrid', 'onsite']:
                    return location.title(), 0.90
                else:
                    return location, 0.80
        
        # Check for common location keywords
        text_lower = text.lower()
        if 'remote' in text_lower:
            return 'Remote', 0.95
        elif 'hybrid' in text_lower:
            return 'Hybrid', 0.90
        elif 'onsite' in text_lower:
            return 'Onsite', 0.85
            
        return "Location not specified", 0.30
    
    def _extract_experience(self, text):
        """Extract years of experience with confidence"""
        experience_patterns = [
            r'(\d+)\+?\s*years',
            r'(\d+)\+?\s*yrs',
            r'(\d+)\+?\s+years',
            r'experience.*?(\d+)\+?',
            r'(\d+).*years.*experience'
        ]
        
        for pattern in experience_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                years = int(match.group(1))
                if 1 <= years <= 30:  # Reasonable range
                    return years, 0.90
        
        # Look for experience ranges
        range_pattern = r'(\d+)\s*-\s*(\d+)\s*years'
        range_match = re.search(range_pattern, text, re.IGNORECASE)
        if range_match:
            min_years = int(range_match.group(1))
            return min_years, 0.85
            
        return 3, 0.50  # Default with low confidence
    
    def _extract_employment_type(self, text):
        """Extract employment type with confidence"""
        text_lower = text.lower()
        
        type_mappings = {
            'full-time': ('Full-time', 0.95),
            'full time': ('Full-time', 0.90),
            'part-time': ('Part-time', 0.95),
            'part time': ('Part-time', 0.90),
            'contract': ('Contract', 0.95),
            'freelance': ('Contract', 0.85),
            'remote': ('Remote', 0.80),
            'hybrid': ('Hybrid', 0.80)
        }
        
        for keyword, (employment_type, confidence) in type_mappings.items():
            if keyword in text_lower:
                return employment_type, confidence
                
        return "Full-time", 0.60  # Default assumption
