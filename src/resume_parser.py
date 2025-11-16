# 📄 RESUME PARSER - ENHANCED VERSION WITH AI CAREER ASSESSMENT
# Extracts skills and information from resume text using hybrid pattern + transformer approach

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import requests
import os  
from typing import Dict, List, Any

import torch
from sentence_transformers import SentenceTransformer, util

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Add after existing imports
try:
    from enhanced_cultural_extractor import EnhancedCulturalExtractor
    ENHANCED_CULTURAL_AVAILABLE = True
except ImportError:
    ENHANCED_CULTURAL_AVAILABLE = False
    print("⚠️ Enhanced cultural extractor not available, using basic method")

class ResumeParser:
    def __init__(self, extraction_method='pattern'):  # Back to pattern as default for reliability
        self.stop_words = set(stopwords.words('english'))
        # FORCE PATTERN METHOD - COMPLETELY DISABLE TRANSFORMER
        self.extraction_method = 'pattern'
        self.transformer_model = None  # Never load transformer
        
        # SECURE API Configuration - using environment variable
        self.groq_api_key = os.getenv("GROQ_API_KEY")  # No hardcoded key!
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        
        if not self.groq_api_key:
            print("⚠️  GROQ_API_KEY environment variable not set - AI features will use fallback")
        
        # Enhanced role scope levels
        self.SCOPE_LEVELS = {
            'individual_contributor': 1,
            'team_lead': 2, 
            'department_head': 3,
            'organization_lead': 4
        }
        
        print("✅ Resume parser initialized with PATTERN METHOD ONLY")
        
        self.skill_keywords = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust'],
            'web': ['html', 'css', 'react', 'angular', 'vue', 'django', 'flask', 'node.js', 'express', 'spring'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd'],
            'data_science': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'statistics'],
            'soft_skills': ['leadership', 'communication', 'teamwork', 'problem solving', 'analytical', 'agile', 'scrum']
        }
        
        # Cultural attribute keywords
        self.cultural_keywords = {
            'teamwork': ['team', 'collaborat', 'partner', 'work together', 'group project', 'cross-functional'],
            'innovation': ['innovati', 'creativ', 'initiative', 'think outside', 'new ideas', 'problem solv'],
            'work_environment': ['remote', 'work from home', 'wfh', 'office', 'on-site', 'hybrid', 'flexible work'],
            'work_pace': ['fast-paced', 'dynamic', 'rapid', 'startup', 'agile', 'stable', 'methodical', 'structured'],
            'customer_focus': ['customer', 'client focus', 'user experience', 'stakeholder', 'end user']
        }

        # Initialize enhanced cultural extractor
        if ENHANCED_CULTURAL_AVAILABLE:
            self.enhanced_extractor = EnhancedCulturalExtractor()
        else:
            self.enhanced_extractor = None

        print(f"✅ Resume parser initialized with {extraction_method} method!")
    
    def parse_resume_text(self, resume_text):
        """Parse resume text and extract structured information"""
        print(f"🔍 Parsing resume text ({len(resume_text)} characters)...")
        print(f"🔧 Using extraction method: {self.extraction_method}")
        
        # Extract basic information
        extracted_info = {
            'name': self.extract_name(resume_text),
            'email': self.extract_email(resume_text),
            'phone': self.extract_phone(resume_text),
            'skills': self.extract_skills(resume_text),
            'experience': self.extract_experience_enhanced(resume_text),  # ENHANCED
            'education': self.extract_education_enhanced(resume_text),    # ENHANCED
            'summary': self.generate_summary(resume_text),
            'work_experience': self.extract_work_experience(resume_text),
            'cultural_attributes': self.extract_cultural_attributes(resume_text),
            'extraction_method_used': self.extraction_method
        }
        
        # ENHANCEMENT: Calculate growth metrics from parsed work experience
        print("📈 CALCULATING GROWTH METRICS...")
        extracted_info['growth_metrics'] = self._calculate_growth_metrics(extracted_info['work_experience'])
        extracted_info['career_metrics'] = self._calculate_career_metrics(extracted_info['work_experience'])
        extracted_info['learning_velocity'] = self._calculate_learning_velocity(extracted_info)
    
        # DEBUG: Print all calculated metrics
        print("🎯 GROWTH METRICS CALCULATED:")
        print(f"   📊 Growth Metrics: {json.dumps(extracted_info['growth_metrics'], indent=6)}")
        print(f"   💼 Career Metrics: {json.dumps(extracted_info['career_metrics'], indent=6)}")
        print(f"   🚀 Learning Velocity: {extracted_info['learning_velocity']}")

        print(f"✅ Extracted: {extracted_info['name']} | {len(extracted_info['skills'])} skills | {extracted_info['experience']} years experience")
        print(f"✅ Work Experience: {len(extracted_info['work_experience'])} roles extracted")

        return extracted_info
    
    def extract_name(self, text):
        """Extract candidate name (simple heuristic)"""
        lines = text.split('\n')
        for line in lines[:5]:
            line = line.strip()
            if line and not any(keyword in line.lower() for keyword in ['resume', 'cv', 'curriculum', 'vitae']):
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
        
        for category, skills in self.skill_keywords.items():
            for skill in skills:
                if skill in text_lower:
                    found_skills.append(skill)
        
        return list(set(found_skills))
    
    def extract_experience_enhanced(self, text):
        """ENHANCED: Extract years of experience from work history"""
        # Method 1: Look for explicit experience statements
        experience_patterns = [
            r'(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yr',
            r'experience.*?(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?.*?experience'
        ]
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                years = max(int(match) for match in matches)
                print(f"📅 Found explicit experience: {years} years")
                return years
        
        # Method 2: Calculate from work experience dates
        work_experience = self.extract_work_experience(text)
        if work_experience and len(work_experience) > 0:
            total_years = self._calculate_experience_from_dates(work_experience)
            if total_years > 0:
                print(f"📅 Calculated experience from work history: {total_years} years")
                return total_years
        
        # Method 3: Estimate from role levels and career progression
        estimated_years = self._estimate_experience_from_career(work_experience)
        print(f"📅 Estimated experience from career: {estimated_years} years")
        return estimated_years
    
    def _calculate_experience_from_dates(self, work_experience):
        """Calculate total years from work experience dates"""
        total_years = 0
        current_year = 2025  # Update as needed
        
        for exp in work_experience:
            duration = exp.get('duration', '')
            # Parse duration like "2018 – Present" or "2014-2018"
            year_matches = re.findall(r'(\d{4})', duration)
            if year_matches:
                years = [int(year) for year in year_matches]
                if len(years) == 2:
                    period_years = years[1] - years[0]
                elif len(years) == 1:
                    period_years = current_year - years[0]
                else:
                    period_years = 3  # Default assumption
                
                total_years += max(1, period_years)  # At least 1 year per role
        
        return min(total_years, 30)  # Cap at 30 years
    
    def _estimate_experience_from_career(self, work_experience):
        """Estimate experience based on role levels and progression"""
        if not work_experience:
            return 2
        
        role_levels = [exp.get('role_level', 1) for exp in work_experience]
        max_level = max(role_levels) if role_levels else 1
        
        # Map role levels to experience estimates
        level_to_experience = {
            1: 2,   # Junior: 1-3 years
            2: 5,   # Mid-level: 4-6 years  
            3: 8,   # Senior: 7-10 years
            4: 12   # Executive: 10+ years
        }
        
        return level_to_experience.get(max_level, 5)
    
    def extract_education_enhanced(self, text):
        """ENHANCED: Extract education information with better accuracy"""
        # Look for education section specifically
        lines = text.split('\n')
        in_education_section = False
        education_lines = []
        
        education_headers = ['education', 'academic', 'qualifications', 'certifications', 'degree']
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            line_lower = line_lower = line_stripped.lower()
            
            # Detect education section header
            if any(header in line_lower for header in education_headers) and len(line_stripped.split()) < 4:
                in_education_section = True
                continue
            
            if in_education_section:
                # Skip empty lines and section endings
                if not line_stripped:
                    continue
                if any(header in line_lower for header in ['experience', 'work', 'skills', 'projects']):
                    break
                    
                # Collect education-related lines
                education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college', 'b.sc', 'm.sc', 'bs', 'ms', 'ba', 'ma']
                if any(keyword in line_lower for keyword in education_keywords):
                    education_lines.append(line_stripped)
        
        # Return the most relevant education line
        if education_lines:
            return education_lines[0]  # Return first education entry found
        
        # Fallback: search entire text for education patterns
        education_patterns = [
            r'(?:bachelor|b\.?sc?|b\.?a)\s*(?:in|of)?\s*[A-Za-z\s]+(?:university|college|institute)',
            r'(?:master|m\.?sc?|m\.?a)\s*(?:in|of)?\s*[A-Za-z\s]+(?:university|college|institute)',
            r'(?:phd|doctorate)\s*(?:in|of)?\s*[A-Za-z\s]+(?:university|college|institute)'
        ]
        
        for pattern in education_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group().strip()
        
        return "Education information not specified"
    
    def generate_summary(self, text):
        """Generate a candidate summary"""
        skills = self.extract_skills(text)
        experience = self.extract_experience_enhanced(text)
        
        if skills:
            top_skills = skills[:4]
            summary = f"Professional with {experience} years of experience. Skilled in {', '.join(top_skills)}."
        else:
            summary = f"Experienced professional with {experience} years in the industry."
        
        return summary

    def extract_cultural_attributes(self, text):
        """Extract cultural fit attributes with enhanced semantic analysis"""
        if self.enhanced_extractor and self.enhanced_extractor.semantic_enabled:
            return self.enhanced_extractor.extract_cultural_attributes_enhanced(text)
    
        text_lower = text.lower()
        cultural_attributes = {}
    
        for attribute, keywords in self.cultural_keywords.items():
            matches = []
            for keyword in keywords:
                if keyword in text_lower:
                    matches.append(keyword)
        
            score = len(matches) / len(keywords) if matches else 0.0
            cultural_attributes[attribute] = score
   
        return cultural_attributes

    def extract_work_experience(self, text):
        """
        Work experience extraction - PATTERN METHOD ONLY
        """
        print("🔧 Using PATTERN METHOD ONLY - Transformer disabled")
        results = self._extract_pattern_based(text)
        return self._apply_smart_filtering(results)

    def _apply_smart_filtering(self, work_experience):
        """Apply smart filtering to any extraction method results"""
        filtered = []
        seen = set()
        
        for result in work_experience:
            # Skip entries with empty or invalid data
            if not result.get('role_title') or not result.get('company'):
                continue
                
            # Skip entries where role_title is too short (likely invalid)
            if len(result['role_title'].strip()) < 2:
                continue
                
            # Skip entries where role_title looks like a bullet point or achievement
            role_lower = result['role_title'].lower()
            if any(indicator in role_lower for indicator in ['•', '- ', 'built ', 'developed ', 'led ', 'managed ', 'oversee', 'drive ', 'published ']):
                continue
                
            # Skip entries where company name looks like a role title (single word, title case)
            company_words = result['company'].split()
            if len(company_words) == 1 and result['company'][0].isupper() and len(result['company']) > 3:
                # This might be a role title mis-parsed as company
                continue
                
            # Skip entries with empty role titles
            if not result['role_title'].strip():
                continue
                
            # Create unique key for deduplication
            key = (result['role_title'].lower().strip(), result['company'].lower().strip())
            if key not in seen:
                seen.add(key)
                filtered.append(result)
        
        print(f"   🔄 Filtered {len(work_experience)} results → {len(filtered)} clean entries")
        return filtered

    def _extract_pattern_based(self, text):
        """
        PATTERN-BASED WORK EXPERIENCE EXTRACTION
        ========================================
        ADD NEW PATTERNS HERE WHEN ENCOUNTERING NEW CV FORMATS
        """
        work_experience = []
        
        # =========================================================================
        # PATTERN 4: Amy Wong's Format - Role\nCompany | Location | Duration
        # Example: "Director of AI Engineering\nTechNova Solutions | San Francisco | 2023-Present"
        # =========================================================================
        pattern4 = r'^(.+?)\n(.+?)\s*\|\s*(.+?)\s*\|\s*(\d{4}\s*[-–]\s*(?:Present|\d{4}))'
        matches4 = re.finditer(pattern4, text, re.MULTILINE | re.IGNORECASE)
        for match in matches4:
            role_title = match.group(1).strip()
            company = match.group(2).strip()
            duration = match.group(4).strip()
            
            if self._is_valid_company_role(role_title, company):
                work_experience.append({
                    'role_title': role_title,
                    'company': company,
                    'duration': duration,
                    'confidence': 0.85,
                    'method': 'pattern'
                })
                print(f"   ✅ Pattern4 matched: {role_title} at {company}")
        
        # =========================================================================
        # PATTERN 5: David Kim's Format - Role | Company | Location | Duration  
        # Example: "Full Stack Developer | TechInnovate Solutions | New York, NY | 2020-Present"
        # =========================================================================
        pattern5 = r'^(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(\d{4}\s*[-–]\s*(?:Present|\d{4}))'
        matches5 = re.finditer(pattern5, text, re.MULTILINE | re.IGNORECASE)
        for match in matches5:
            role_title = match.group(1).strip()
            company = match.group(2).strip()
            duration = match.group(4).strip()
            
            if self._is_valid_company_role(role_title, company):
                work_experience.append({
                    'role_title': role_title,
                    'company': company,
                    'duration': duration,
                    'confidence': 0.85,
                    'method': 'pattern'
                })
                print(f"   ✅ Pattern5 matched: {role_title} at {company}")
        
        # =========================================================================
        # PATTERN 1: Douglas Lim's Format - Role (Duration)\nCompany
        # Example: "Chief Technology Officer (2018 – Present)\nGlobal Fintech Solutions"
        # =========================================================================
        pattern1 = r'^(.+?)\s*\((\d{4}\s*[–-]\s*(?:Present|\d{4}))\)\s*\n(.+?)(?=\n•|\n\d|\n[A-Z]|$)'
        matches1 = re.finditer(pattern1, text, re.MULTILINE | re.IGNORECASE)
        for match in matches1:
            role_title = match.group(1).strip()
            duration = match.group(2).strip()
            company = match.group(3).strip()
            
            if self._is_valid_company_role(role_title, company):
                work_experience.append({
                    'role_title': role_title,
                    'company': company,
                    'duration': duration,
                    'confidence': 0.9,
                    'method': 'pattern'
                })
                print(f"   ✅ Pattern1 matched: {role_title} at {company}")
        
        # =========================================================================
        # PATTERN 2: Generic Format - Role\nCompany, Location Duration
        # Example: "Senior Developer\nGoogle, Mountain View 2015-2020"
        # =========================================================================
        pattern2 = r'^(.+?)\n(.+?),\s*(.+?)\s*(\d{4}\s*[–-]\s*(?:Present|\d{4}))'
        matches2 = re.finditer(pattern2, text, re.MULTILINE | re.IGNORECASE)
        for match in matches2:
            role_title = match.group(1).strip()
            company = match.group(2).strip()
            duration = match.group(4).strip()
            
            if self._is_valid_company_role(role_title, company):
                work_experience.append({
                    'role_title': role_title,
                    'company': company, 
                    'duration': duration,
                    'confidence': 0.7,
                    'method': 'pattern'
                })
                print(f"   ✅ Pattern2 matched: {role_title} at {company}")
        
        # =========================================================================
        # PATTERN 3: Original Pipe/Dash Format - Company | Role | Duration
        # Example: "Google | Senior Software Engineer | 2018-2022"
        # =========================================================================
        pattern3 = r'^([A-Za-z\s&]+)\s*[|-]\s*([A-Za-z\s]+)\s*[|-]\s*(\d{4}\s*[-–]\s*(?:Present|\d{4}))'
        matches3 = re.finditer(pattern3, text, re.MULTILINE | re.IGNORECASE)
        for match in matches3:
            company = match.group(1).strip()
            role_title = match.group(2).strip()
            duration = match.group(3).strip()
            
            if self._is_valid_company_role(role_title, company):
                work_experience.append({
                    'role_title': role_title,
                    'company': company,
                    'duration': duration,
                    'confidence': 0.6,
                    'method': 'pattern'
                })
                print(f"   ✅ Pattern3 matched: {role_title} at {company}")
        
        # =========================================================================
        # ADD NEW PATTERNS ABOVE THIS LINE
        # =========================================================================
        
        return self._finalize_experience_data(work_experience)

    def _merge_extraction_results(self, pattern_results, transformer_results):
        """
        SMART MERGING: Combine results from both methods with quality filtering
        """
        all_results = pattern_results + transformer_results
        return self._apply_smart_filtering(all_results)

    def _finalize_experience_data(self, work_experience):
        """Add role level and scope to experience data"""
        # Only add fallback if NO valid experience was found
        if not work_experience or all(exp.get('role_title') == 'Extracted role' for exp in work_experience):
            return [{
                'role_title': 'Extracted role',
                'company': 'Extracted company', 
                'duration': 'Extracted duration',
                'role_level': 2,
                'scope': 'individual_contributor'
            }]
        
        for exp in work_experience:
            exp['role_level'] = self._infer_role_level(exp['role_title'])
            exp['scope'] = self._infer_role_scope(exp['role_title'])
            # Remove method field from final output
            if 'method' in exp:
                del exp['method']
        
        return work_experience

    def _is_valid_company_role(self, role_title, company):
        """Validate that extracted role/company are not actually skills"""
        skill_indicators = ['python', 'java', 'kubernetes', 'docker', 'aws', 'machine learning', 
                           'deep learning', 'pytorch', 'tensorflow', 'go', 'react', 'angular',
                           'sql', 'javascript', 'html', 'css', 'node.js', 'express']
        
        role_lower = role_title.lower()
        company_lower = company.lower()
        
        if any(skill in role_lower for skill in skill_indicators):
            return False
        if any(skill in company_lower for skill in skill_indicators):
            return False
            
        return True

    def _infer_role_level(self, role_title):
        """Infer role level from title"""
        role_lower = role_title.lower()
        
        if any(level in role_lower for level in ['cto', 'chief', 'director', 'head of', 'vp', 'vice president']):
            return 4
        elif any(level in role_lower for level in ['senior', 'sr.', 'lead', 'principal']):
            return 3
        elif any(level in role_lower for level in ['manager', 'team lead', 'supervisor']):
            return 2
        else:
            return 1

    def _infer_role_scope(self, role_title):
        """Infer role scope from title"""
        role_lower = role_title.lower()
        
        if any(scope in role_lower for scope in ['cto', 'chief', 'director', 'head', 'vp', 'manager', 'lead', 'supervisor']):
            return 'team_leadership'
        else:
            return 'individual_contributor'

    def parse_resume_to_candidate(self, resume_text, candidate_name=None, include_extensions=None):
        """Convert parsed resume into candidate format for database"""
        parsed_data = self.parse_resume_text(resume_text)
        
        candidate_data = {
            "name": candidate_name or parsed_data['name'],
            "profile": parsed_data['summary'],
            "skills": parsed_data['skills'],
            "experience_years": parsed_data['experience'],
            "location": "Location not specified",
            "email": parsed_data['email'],
            "phone": parsed_data['phone'],
            "education": parsed_data['education'],
            "work_experience": parsed_data['work_experience'],
            "cultural_attributes": parsed_data['cultural_attributes'],
            "extraction_method": parsed_data.get('extraction_method_used', 'unknown'),
            # ADD THESE GROWTH DATA FIELDS:
            "growth_metrics": parsed_data.get('growth_metrics', {}),
            "career_metrics": parsed_data.get('career_metrics', {}),
            "learning_velocity": parsed_data.get('learning_velocity', 0.0)            
        }
        
        # 🐛 DEBUG: Check if ID field exists (it shouldn't!)
        print("🐛 DEBUG Candidate Data Structure:")
        print(f"   Keys: {list(candidate_data.keys())}")
        if 'id' in candidate_data:
            print(f"   ❌ FOUND ID FIELD: {candidate_data['id']} - THIS CAUSES OVERWRITE!")
        else:
            print("   ✅ No ID field - correct behavior")
        print("📦 Full candidate data:", json.dumps(candidate_data, indent=2))
        
        return candidate_data

    # =========================================================================
    # AI CAREER ASSESSMENT METHODS
    # =========================================================================

    def analyze_career_with_ai(self, work_experience):
        """AI assessment of career progression using Groq/Llama3"""
        if not work_experience:
            return self._get_default_ai_assessment()
        
        try:
            prompt = self._create_career_analysis_prompt(work_experience)
            response = self._call_groq_api(prompt)
            ai_assessment = self._parse_ai_response(response)
            return ai_assessment
        except Exception as e:
            print(f"⚠️ AI career analysis failed: {e}, using fallback")
            return self._get_fallback_assessment(work_experience)

    def _create_career_analysis_prompt(self, work_experience):
        """Create structured prompt for career analysis"""
        work_exp_str = json.dumps(work_experience, indent=2)
        
        return f"""
        Analyze this work experience history for career progression assessment:
        
        WORK EXPERIENCE:
        {work_exp_str}
        
        Return ONLY valid JSON with these exact fields:
        {{
            "career_archetype": "high_growth_ic" | "steady_manager" | "strategic_executive" | "portfolio_leader" | "technical_specialist",
            "scope_progression": [array of numbers 1-4 for each role scope level],
            "impact_scale": [array of numbers 0.0-1.0 for each role impact],
            "strategic_mobility_score": 0.0-1.0,
            "executive_potential": 0.0-1.0,
            "analysis_rationale": "brief explanation of career pattern"
        }}
        
        SCOPE LEVELS: 1=individual_contributor, 2=team_lead, 3=department_head, 4=organization_lead
        IMPACT SCALE: 0.1=low impact, 0.5=moderate, 0.9=high strategic impact
        STRATEGIC MOBILITY: 0.1=linear progression, 0.9=strategic lateral moves with increased scope
        """

    def _call_groq_api(self, prompt):
        """Call Groq API with enhanced error handling"""
        # Check if API key is properly configured
        if not self.groq_api_key:
            print("   ⚠️  GROQ_API_KEY not set in environment - using fallback analysis")
            raise ValueError("GROQ_API_KEY environment variable not configured")
    
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
    
        data = {
            "model": "llama-3.3-70b-versatile",  # Current production model
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 1024,
            "response_format": {"type": "json_object"}
        }
    
        try:
            response = requests.post(self.groq_url, json=data, headers=headers, timeout=30)
        
            # Check for specific HTTP errors
            if response.status_code == 400:
                print("   ❌ Groq API: Bad Request - Invalid request format")
                error_detail = response.json().get('error', {}).get('message', 'Unknown error')
                print(f"   📝 Error details: {error_detail}")
            elif response.status_code == 401:
                print("   ❌ Groq API: Unauthorized - Invalid API key")
            elif response.status_code == 429:
                print("   ⚠️  Groq API: Rate limit exceeded")
            elif response.status_code == 500:
                print("   ❌ Groq API: Internal server error")
        
            response.raise_for_status()  # This will raise an exception for 4xx/5xx status codes
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            print(f"   ❌ Groq API HTTP Error: {e}")
            raise
        except requests.exceptions.ConnectionError:
            print("   ❌ Groq API: Connection failed - check internet connection")
            raise
        except requests.exceptions.Timeout:
            print("   ❌ Groq API: Request timeout")
            raise
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Groq API Request Exception: {e}")
            raise
        except Exception as e:
            print(f"   ❌ Unexpected error calling Groq API: {e}")
            raise

    def _parse_ai_response(self, response):
        """Parse and validate AI response"""
        try:
            content = response['choices'][0]['message']['content']
            assessment = json.loads(content)
            
            # Validate required fields
            required_fields = ['career_archetype', 'scope_progression', 'impact_scale', 
                              'strategic_mobility_score', 'executive_potential', 'analysis_rationale']
            if all(field in assessment for field in required_fields):
                return assessment
            else:
                raise ValueError("Missing required fields in AI response")
        except Exception as e:
            print(f"⚠️ Failed to parse AI response: {e}")
            raise

    def _get_fallback_assessment(self, work_experience):
        """Fallback assessment when AI fails"""
        scope_progression = []
        impact_scale = []
        
        for role in work_experience:
            scope_level = self._detect_scope_level(role['role_title'])
            scope_progression.append(scope_level)
            impact_scale.append(min(scope_level * 0.25, 0.9))
        
        return {
            "career_archetype": "technical_specialist",
            "scope_progression": scope_progression,
            "impact_scale": impact_scale,
            "strategic_mobility_score": 0.5,
            "executive_potential": 0.3,
            "analysis_rationale": "Basic fallback analysis"
        }

    def _get_default_ai_assessment(self):
        """Default assessment for no work experience"""
        return {
            "career_archetype": "early_career",
            "scope_progression": [],
            "impact_scale": [],
            "strategic_mobility_score": 0.5,
            "executive_potential": 0.1,
            "analysis_rationale": "No work experience available"
        }

    def _detect_scope_level(self, role_title):
        """Detect scope level from role title (fallback method)"""
        role_lower = role_title.lower()
        
        if any(term in role_lower for term in ['cto', 'chief', 'vp', 'vice president']):
            return 4  # organization_lead
        elif any(term in role_lower for term in ['director', 'head of']):
            return 3  # department_head
        elif any(term in role_lower for term in ['manager', 'lead', 'team lead']):
            return 2  # team_lead
        else:
            return 1  # individual_contributor

    # =========================================================================
    # ENHANCED GROWTH METRICS WITH AI ASSESSMENT
    # =========================================================================

    def _calculate_growth_metrics(self, work_experience):
        """Enhanced growth metrics with AI career assessment"""
        if not work_experience or len(work_experience) < 2:
            print("   ⚠️  Insufficient work experience for growth calculation")
            return self._get_empty_growth_metrics()
        
        # Get AI career assessment
        print("   🤖 Analyzing career progression with AI...")
        ai_assessment = self.analyze_career_with_ai(work_experience)
        
        # FIX: Reverse work experience to get chronological order (oldest first)
        chronological_experience = list(reversed(work_experience))
        print(f"   📅 Chronological order: {[exp['role_title'] for exp in chronological_experience]}")
        
        # Calculate enhanced growth dimensions using AI insights
        growth_dimensions = self._calculate_enhanced_dimensions(chronological_experience, ai_assessment)
        
        # Classify career stage
        career_stage = self._classify_career_stage(chronological_experience)
        
        # Calculate overall score with career stage adjustment
        overall_score = self._calculate_stage_adjusted_score(growth_dimensions, career_stage)
        
        growth_data = {
            'growth_potential_score': round(overall_score, 1),
            'growth_dimensions': growth_dimensions,
            'career_archetype': ai_assessment["career_archetype"],
            'career_stage': career_stage,
            'executive_potential': ai_assessment["executive_potential"],
            'strategic_mobility': ai_assessment["strategic_mobility_score"],
            'analysis_rationale': ai_assessment["analysis_rationale"],
            'promotion_velocity': self._calculate_promotion_velocity(work_experience),
            'max_role_level': max(exp['role_level'] for exp in work_experience)
        }
        
        print("   📈 ENHANCED GROWTH DIMENSIONS CALCULATED:")
        print(f"      ↗️  Vertical Growth: {growth_dimensions['vertical_growth']} (Role level increases)")
        print(f"      📊 Scope Growth: {growth_dimensions['scope_growth']} (Responsibility expansion)")
        print(f"      💼 Impact Growth: {growth_dimensions['impact_growth']} (Business impact scale)") 
        print(f"      🔄 Adaptability: {growth_dimensions['adaptability']} (Domain/company changes)")
        print(f"      ⚡ Leadership Velocity: {growth_dimensions['leadership_velocity']} (Time to leadership)")
        print(f"      🎯 CAREER ARCHETYPE: {ai_assessment['career_archetype']}")
        print(f"      🎯 OVERALL GROWTH SCORE: {overall_score:.1f}/100")
        
        return growth_data

    def _calculate_enhanced_dimensions(self, work_experience, ai_assessment):
        """Calculate enhanced growth dimensions using AI insights"""
        # Vertical growth - account for executive ceiling
        vertical_growth = self._calculate_vertical_growth_enhanced(work_experience, ai_assessment)
        
        # Scope growth using AI-detected scope progression
        scope_growth = self._calculate_scope_growth_enhanced(ai_assessment["scope_progression"])
        
        # Impact growth using AI impact scale
        impact_growth = self._calculate_impact_growth_enhanced(ai_assessment["impact_scale"])
        
        # Adaptability - company changes with strategic value
        adaptability = self._calculate_adaptability_enhanced(work_experience, ai_assessment)
        
        # Leadership velocity
        leadership_velocity = self._calculate_leadership_velocity_enhanced(work_experience)
        
        return {
            'vertical_growth': round(vertical_growth, 2),
            'scope_growth': round(scope_growth, 2),
            'impact_growth': round(impact_growth, 2),
            'adaptability': round(adaptability, 2),
            'leadership_velocity': round(leadership_velocity, 2)
        }

    def _calculate_vertical_growth_enhanced(self, work_experience, ai_assessment):
        """Enhanced vertical growth accounting for executive levels"""
        if len(work_experience) < 2:
            return 0.5
        
        scope_progression = ai_assessment["scope_progression"]
        if not scope_progression:
            return 0.5
        
        # Calculate progression slope
        progression = max(scope_progression) - min(scope_progression)
        max_possible = 3  # Individual to executive (1 to 4)
        
        # Normalize and cap at 1.0
        vertical_growth = min(progression / max_possible, 1.0)
        
        # Boost for executive roles (no penalty for lateral executive moves)
        if max(scope_progression) >= 4:  # Executive level
            vertical_growth = max(vertical_growth, 0.7)
        
        return vertical_growth

    def _calculate_scope_growth_enhanced(self, scope_progression):
        """Calculate scope growth from AI-detected scope levels"""
        if len(scope_progression) < 2:
            return 0.3
        
        scope_range = max(scope_progression) - min(scope_progression)
        max_scope_range = 3  # From IC (1) to Executive (4)
        
        return min(scope_range / max_scope_range, 1.0)

    def _calculate_impact_growth_enhanced(self, impact_scale):
        """Calculate impact growth from AI impact scores"""
        if len(impact_scale) < 2:
            return 0.3
        
        # Use maximum impact achieved
        return max(impact_scale)

    def _calculate_adaptability_enhanced(self, work_experience, ai_assessment):
        """Enhanced adaptability with strategic mobility consideration"""
        if len(work_experience) <= 1:
            return 0.3
        
        # Base adaptability from company changes
        companies = len(set(exp.get('company', '') for exp in work_experience))
        base_adaptability = min(companies / 5, 0.7)  # Cap at 0.7
        
        # Boost with strategic mobility score from AI
        strategic_boost = ai_assessment["strategic_mobility_score"] * 0.3
        
        return min(base_adaptability + strategic_boost, 1.0)

    def _calculate_leadership_velocity_enhanced(self, work_experience):
        """Calculate time to first leadership role"""
        for i, role in enumerate(work_experience):
            role_title = role.get('role_title', '').lower()
            if any(leadership_term in role_title for leadership_term in 
                   ['manager', 'director', 'head', 'lead', 'chief', 'vp', 'cto']):
                # Faster promotion to leadership = higher score
                leadership_velocity = 1.0 - (i / len(work_experience))
                return max(leadership_velocity, 0.3)
        
        return 0.1  # No leadership roles found

    def _classify_career_stage(self, work_experience):
        """Classify career stage based on experience and roles"""
        if not work_experience:
            return "early_career"
        
        # Estimate total experience
        estimated_years = len(work_experience) * 3  # Rough estimate
        
        # Check for executive roles
        has_executive = any('chief' in exp.get('role_title', '').lower() or 
                           'vp' in exp.get('role_title', '').lower() or
                           'president' in exp.get('role_title', '').lower()
                           for exp in work_experience)
        
        if has_executive or estimated_years >= 15:
            return "executive"
        elif estimated_years >= 8:
            return "mid_career"
        else:
            return "early_career"

    def _calculate_stage_adjusted_score(self, growth_dimensions, career_stage):
        """Calculate overall score adjusted for career stage context"""
        # Equal weighting for all dimensions in base calculation
        base_score = sum(growth_dimensions.values()) / len(growth_dimensions)
        
        # Stage-based adjustments
        stage_weights = {
            "early_career": 1.1,  # Slight boost for early potential
            "mid_career": 1.0,    # Neutral
            "executive": 1.0      # Neutral - let dimensions speak for themselves
        }
        
        adjusted_score = base_score * stage_weights.get(career_stage, 1.0)
        return min(adjusted_score * 100, 100)  # Convert to percentage

    def _get_empty_growth_metrics(self):
        """Return empty growth metrics for no experience"""
        return {
            "growth_potential_score": 0.0,
            "growth_dimensions": {
                'vertical_growth': 0.0,
                'scope_growth': 0.0,
                'impact_growth': 0.0,
                'adaptability': 0.0,
                'leadership_velocity': 0.0
            },
            "career_archetype": "early_career",
            "career_stage": "early_career",
            "executive_potential": 0.0,
            "strategic_mobility": 0.0,
            "analysis_rationale": "No work experience available",
            "promotion_velocity": 0,
            "max_role_level": 1
        }

    # =========================================================================
    # EXISTING CAREER METRICS METHODS (UNCHANGED)
    # =========================================================================

    def _get_tenure_years(self, experience):
        """Extract tenure years from duration string"""
        duration = experience.get('duration', '')
        year_matches = re.findall(r'(\d{4})', duration)
        if len(year_matches) >= 2:
            return int(year_matches[1]) - int(year_matches[0])
        return 3  # Default assumption

    def _calculate_promotion_velocity(self, work_experience):
        """Calculate average time between role level increases"""
        if len(work_experience) < 2:
            return 0
        
        # Count level increases
        level_increases = 0
        for i in range(1, len(work_experience)):
            if work_experience[i]['role_level'] > work_experience[i-1]['role_level']:
                level_increases += 1
        
        if level_increases == 0:
            return 10  # No promotions - high velocity (penalty)
        
        # Simplified: assume 2 years between promotions for now
        return 2.0

    def _calculate_career_metrics(self, work_experience):
        """Calculate career progression metrics"""
        if not work_experience:
            return {
                'average_tenure_months': 0,
                'career_progression_slope': 0,
                'leadership_experience': False,
                'number_of_companies': 0,
                'role_variety_score': 0
            }
        
        # Calculate metrics
        companies = set(exp['company'] for exp in work_experience)
        has_leadership = any(exp['scope'] == 'team_leadership' for exp in work_experience)
        role_variety = len(set(exp['role_title'] for exp in work_experience))
        
        metrics = {
            'average_tenure_months': 24.0,  # Simplified calculation
            'career_progression_slope': 0.1,
            'leadership_experience': has_leadership,
            'number_of_companies': len(companies),
            'role_variety_score': role_variety / len(work_experience) if work_experience else 0
        }
        
        print(f"   💼 Career Metrics: {len(companies)} companies, leadership: {has_leadership}")
        
        return metrics

    def _calculate_learning_velocity(self, extracted_info):
        """Calculate learning velocity from skills and experience"""
        skills_count = len(extracted_info['skills'])
        experience_years = extracted_info['experience']
        
        if experience_years > 0:
            velocity = skills_count / experience_years
        else:
            velocity = skills_count
        
        print(f"   🚀 Learning Velocity: {velocity:.1f} (skills: {skills_count}, exp: {experience_years} years)")
        
        return velocity

def main():
    """Test the enhanced resume parser with different methods"""
    test_resume = """
    DOUGLAS LIM
    Phone: +65 98765432
    Email: douglas.lim@yahoo.com

    Career Highlights

    Chief Technology Officer (2018 – Present)
    Global Fintech Solutions
    • Spearheaded digital transformation program

    Head of Technology (2014 – 2018)
    Stanford Computer System
    • Embedded sustainability KPIs

    Senior Software Engineer (2008 – 2014)
    IBM
    • Developed workflow automation tools

    EDUCATION:
    Stanford Executive Program in AI Leadership
    MIT Sloan Certificate in Digital Transformation
    """
    
    print("🧪 TESTING ENHANCED RESUME PARSER")
    print("=" * 50)
    
    # Test pattern method (recommended)
    print("\n🔧 PATTERN METHOD (RECOMMENDED):")
    parser_pattern = ResumeParser(extraction_method='pattern')
    parsed_pattern = parser_pattern.parse_resume_text(test_resume)
    print(f"   Experience: {parsed_pattern['experience']} years")
    print(f"   Education: {parsed_pattern['education']}")
    for exp in parsed_pattern['work_experience']:
        print(f"   • {exp['role_title']} at {exp['company']}")

if __name__ == "__main__":
    main()