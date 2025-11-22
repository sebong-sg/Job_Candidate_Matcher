# 🎯 JOB PARSER USING GROQ - Mirroring your working resume parser pattern
import os
import requests
import json
import re
from typing import Dict, Any

class JobDescriptionParser:
    def __init__(self):
        # SECURE API Configuration - using environment variable (same as your resume parser)
        self.groq_api_key = os.getenv("GROQ_API_KEY")  # No hardcoded key!
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        
        if not self.groq_api_key:
            print("⚠️ GROQ_API_KEY environment variable not set - Job parsing will use fallback")
        else:
            print("✅ Job Parser initialized with Groq API")

    def parse_job_description(self, text):
        """
        Parse job description using Groq API - follows same pattern as your resume parser
        """
        if not self.groq_api_key:
            print("🔍 DEBUG: No API key - using fallback")
            return self._fallback_parse(text)
            
        try:
            print("🔍 DEBUG: Attempting Groq API call...")
            prompt = self._create_job_parsing_prompt(text)
            response = self._call_groq_api(prompt)
            
            if response:
                print("🔍 DEBUG: Groq API call successful!")
                parsed_data = json.loads(response)
                # Add quality assessment
                parsed_data['quality_assessment'] = self._assess_quality(text, parsed_data)
                
                # NEW: Generate AI Job Profile
                ai_profile = self._generate_ai_job_profile(parsed_data, text)
                parsed_data['ai_job_profile'] = ai_profile
                
                return parsed_data
            else:
                print("🔍 DEBUG: Groq API exception - using fallback")
                return self._fallback_parse(text)
                
        except Exception as e:
            print(f"❌ Job parsing error: {e}")
            return self._fallback_parse(text)

    def _create_job_parsing_prompt(self, text):
        """Create the prompt for job parsing (similar to your resume parser pattern)"""
        return f"""
        Analyze this job description and extract clean, structured data. Remove all section headers and prefixes.
        CRITICAL: Extract ONLY the actual values, NOT the section headers.
    
        EXAMPLE:
        If you see "Job Description: Cloud Security Engineer", extract "Cloud Security Engineer"
        If you see "Company: Aegis Cyber Solutions", extract "Aegis Cyber Solutions" 
        If you see "Location: Remote (Global)", extract "Remote (Global)"
        
        JOB DESCRIPTION:
        {text}
        
        EXTRACTION RULES:
        - For title: Extract ONLY the job title, remove "Job Description:", "Title:", "Position:" prefixes
        - For company: Extract ONLY the company name, remove "Company:", "Organization:" prefixes  
        - For location: Extract ONLY the location, remove "Location:" prefix
        - For skills: Extract from "Required Skills", "Qualifications", or "Requirements" sections
        - For experience: Look for patterns like "X+ years", "X years experience"

        Extract these fields (CLEAN VALUES ONLY - NO SECTION HEADERS):
        - title: Extract ONLY the job title text, remove "Job Description:", "Title:", "Position:" prefixes
        - company: Extract ONLY the company name, remove "Company:", "Organization:" prefixes
        - location: Extract ONLY the location, remove "Location:" prefix
        - experience_required: Extract number of years from phrases like "X+ years"
        - employment_type: Extract from phrases like "Full-time", "Part-time", "Contract"
        - required_skills: List of technical skills mentioned in requirements
        - preferred_skills: List of bonus/nice-to-have skills
        - description: The full job description text
        - career_stage: early_career (0-3 yrs), mid_career (3-8 yrs), or executive (8+ yrs)
        - summary: Professional summary (2-3 sentences summarizing the role)
        - original_job_text: Complete original job description text
        
        Return ONLY valid JSON in this exact format:
        {{
            "title": "Extracted Job Title",
            "company": "Extracted Company Name",
            "location": "Extracted Location", 
            "experience_required": 0,
            "employment_type": "Full-time",
            "required_skills": ["skill1", "skill2"],
            "preferred_skills": ["skill1", "skill2"],
            "description": "Full description text...",
            "career_stage": "mid_career",
            "summary": "Professional summary of the role...",
            "original_job_text": "Complete original text..."
        }}
        """

    def _call_groq_api(self, prompt):
        """Call Groq API - same pattern as your resume parser"""
        try:
            headers = {
                'Authorization': f'Bearer {self.groq_api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "messages": [{"role": "user", "content": prompt}],
                "model": "llama-3.3-70b-versatile",
                "temperature": 0.1,
                "max_tokens": 2000,
                "response_format": {"type": "json_object"}
            }
            
            print(f"🔍 DEBUG: Sending request to Groq...")
            print(f"🔍 DEBUG: Prompt length: {len(prompt)}")
            print(f"🔍 DEBUG: Payload keys: {list(payload.keys())}")
            
            response = requests.post(self.groq_url, headers=headers, json=payload, timeout=30)

            print(f"🔍 DEBUG: Response status: {response.status_code}")
            print(f"🔍 DEBUG: Response headers: {dict(response.headers)}")
        
           # If we get an error, print the response body for debugging
            if response.status_code != 200:
                print(f"🔍 DEBUG: Error response: {response.text}")
                response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except Exception as e:
            print(f"❌ Groq API call failed: {e}")
            return None

    def _generate_ai_job_profile(self, parsed_data, original_text):
        """Generate AI Job Profile content using Groq API"""
        if not self.groq_api_key:
            return self._fallback_ai_profile(parsed_data)
            
        try:
            prompt = self._create_ai_profile_prompt(parsed_data, original_text)
            response = self._call_groq_api(prompt)
            
            if response:
                return json.loads(response)
            else:
                return self._fallback_ai_profile(parsed_data)
                
        except Exception as e:
            print(f"❌ AI Job Profile generation error: {e}")
            return self._fallback_ai_profile(parsed_data)

    def _create_ai_profile_prompt(self, parsed_data, original_text):
        """Create prompt for AI Job Profile generation"""
        return f"""
        Based on the job description analysis, create a comprehensive AI Job Profile that provides insights for recruiters.
        
        JOB DATA:
        - Title: {parsed_data.get('title', 'Unknown')}
        - Company: {parsed_data.get('company', 'Unknown')}
        - Location: {parsed_data.get('location', 'Unknown')}
        - Experience Required: {parsed_data.get('experience_required', 0)} years
        - Required Skills: {parsed_data.get('required_skills', [])}
        - Career Stage: {parsed_data.get('career_stage', 'mid_career')}
        
        ORIGINAL JOB DESCRIPTION:
        {original_text}
        
        Create an AI Job Profile with these sections:
        
        1. ROLE OVERVIEW: 2-3 sentence executive summary of the position
        2. IDEAL CANDIDATE PROFILE: Key characteristics of the perfect candidate
        3. KEY SUCCESS FACTORS: What will make someone successful in this role
        4. GROWTH POTENTIAL: Career progression and development opportunities
        5. CULTURAL FIT: Team dynamics and work environment expectations
        6. RECRUITING INSIGHTS: Tips for finding and attracting the right candidates
        
        Return ONLY valid JSON in this exact format:
        {{
            "role_overview": "Executive summary...",
            "ideal_candidate": "Candidate characteristics...", 
            "success_factors": "Key success elements...",
            "growth_potential": "Career progression...",
            "cultural_fit": "Team and environment...",
            "recruiting_insights": "Recruiting tips..."
        }}
        """

    def _fallback_ai_profile(self, parsed_data):
        """Fallback AI Job Profile when Groq is unavailable"""
        return {
            "role_overview": f"This {parsed_data.get('title', 'position')} role at {parsed_data.get('company', 'the company')} requires {parsed_data.get('experience_required', 0)}+ years of experience and focuses on {', '.join(parsed_data.get('required_skills', ['relevant skills']))}.",
            "ideal_candidate": f"An experienced professional with strong {', '.join(parsed_data.get('required_skills', ['technical skills']))} and {parsed_data.get('experience_required', 0)}+ years in the field. Someone who thrives in a collaborative environment and is looking for long-term growth.",
            "success_factors": "Technical proficiency, problem-solving abilities, teamwork, and adaptability to changing requirements. Strong communication skills and ability to work independently.",
            "growth_potential": "Opportunities for career advancement, skill development, and potential leadership roles. Exposure to new technologies and business domains.",
            "cultural_fit": "Team-oriented environment that values collaboration, innovation, and continuous learning. Fast-paced setting with opportunities for professional development.",
            "recruiting_insights": "Look for candidates with proven experience in required technologies. Consider both technical skills and cultural fit. Prioritize candidates with demonstrated growth and learning agility."
        }

    def _fallback_parse(self, text):
        """Fallback parsing when Groq is unavailable"""
        print("🔄 Using fallback job parsing")
        parsed_data = {
            'title': self._extract_title(text),
            'company': self._extract_company(text),
            'location': self._extract_location(text),
            'experience_required': self._extract_experience(text),
            'employment_type': 'Full-time',
            'required_skills': self._extract_skills(text),
            'preferred_skills': [],
            'description': text,
            'career_stage': 'mid_career',
            'summary': self._extract_summary(text),
            'original_job_text': text,
            'quality_assessment': {
                'quality_score': 0.5,
                'quality_level': 'medium',
                'quality_issues': ['Used fallback parsing']
            }
        }
        
        # Generate fallback AI Job Profile
        parsed_data['ai_job_profile'] = self._fallback_ai_profile(parsed_data)
        
        return parsed_data

    def _extract_title(self, text):
        """Simple title extraction"""
        lines = text.split('\n')
        for line in lines[:5]:
            line = line.strip()
            if line and len(line) < 100 and not line.lower().startswith(('company', 'location', 'about')):
                return line
        return "Job Title"

    def _extract_company(self, text):
        """Simple company extraction"""
        patterns = [
            r'at\s+([A-Z][A-Za-z0-9&\s]+?)(?:\s|\.|$|,)',
            r'[Cc]ompany:\s*([^\n,.]+)',
            r'([A-Z][A-Za-z0-9&\s]+)\s+is hiring',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                company = match.group(1).strip()
                if len(company) > 2 and len(company) < 50:
                    return company
        return "Company"

    def _extract_location(self, text):
        """Simple location extraction"""
        if 'remote' in text.lower():
            return 'Remote'
        elif 'hybrid' in text.lower():
            return 'Hybrid'
        return 'Location not specified'

    def _extract_experience(self, text):
        """Simple experience extraction"""
        match = re.search(r'(\d+)\+?\s*years', text, re.IGNORECASE)
        return int(match.group(1)) if match else 0

    def _extract_skills(self, text):
        """Simple skills extraction"""
        common_skills = ['python', 'java', 'javascript', 'aws', 'docker', 'kubernetes', 
                        'react', 'node', 'sql', 'nosql', 'machine learning', 'ai']
        found_skills = []
        for skill in common_skills:
            if skill in text.lower():
                found_skills.append(skill)
        return found_skills[:8]  # Return top 8 skills

    def _extract_summary(self, text):
        """Extract summary from text"""
        sentences = text.split('.')
        if len(sentences) >= 2:
            return '. '.join(sentences[:2]) + '.'
        return text[:200] + '...' if len(text) > 200 else text

    def _assess_quality(self, text, parsed_data):
        """Assess job description quality"""
        score = 0.5
        
        # Length assessment
        if len(text) > 500:
            score += 0.2
        elif len(text) < 200:
            score -= 0.2
            
        # Completeness assessment
        if parsed_data.get('title') and parsed_data['title'] != 'Job Title':
            score += 0.1
        if parsed_data.get('company') and parsed_data['company'] != 'Company':
            score += 0.1
        if parsed_data.get('required_skills') and len(parsed_data['required_skills']) > 2:
            score += 0.1
        
        # Cap the score at 1.0 (100%)
        score = min(score, 1.0)
    
        quality_level = 'high' if score >= 0.7 else 'medium' if score >= 0.5 else 'low'
            
        return {
            'quality_score': round(score, 2),
            'quality_level': 'high' if score >= 0.7 else 'medium' if score >= 0.5 else 'low',
            'quality_issues': [] if score >= 0.7 else ['Job description could be more detailed']
        }

# Test function
if __name__ == "__main__":
    print("🧪 Testing Job Parser with AI Job Profile...")
    parser = JobDescriptionParser()
    
    test_jd = """
    Senior Python Developer at TechCorp
    We are looking for a Senior Python Developer with 5+ years of experience.
    Required skills: Python, Django, Flask, PostgreSQL, AWS
    Location: Remote
    This is a full-time position with great growth opportunities.
    """
    
    result = parser.parse_job_description(test_jd)
    print(f"✅ Parsed: {result.get('title')} at {result.get('company')}")
    print(f"📊 Quality: {result.get('quality_assessment', {}).get('quality_level')}")
    print(f"🤖 AI Profile: {result.get('ai_job_profile', {}).get('role_overview', 'No AI profile')}")