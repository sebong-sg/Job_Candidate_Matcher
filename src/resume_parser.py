# 📄 RESUME PARSER - ENHANCED VERSION WITH CONSISTENT FILTERING
# Extracts skills and information from resume text using hybrid pattern + transformer approach

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
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
        
        print("✅ Resume parser initialized with PATTERN METHOD ONLY")
        

#        self.extraction_method = extraction_method
        
        # Initialize transformer model for semantic parsing
#        self.transformer_model = None
#        if extraction_method in ['transformer', 'hybrid']:
#            try:
#                print("🔄 Loading Sentence Transformer model...")
#                self.transformer_model = SentenceTransformer('all-MiniLM-L6-v2')
#                print("✅ Transformer model loaded successfully!")
#            except Exception as e:
#                print(f"⚠️ Failed to load transformer model: {e}")
#                self.transformer_model = None
        
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
#        pattern3 = r'^(.+?)\s*[|-]\s*(.+?)\s*[|-]\s*(.+)'
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
            "extraction_method": parsed_data.get('extraction_method_used', 'unknown')
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

    def _calculate_growth_metrics(self, work_experience):
        """Calculate multi-dimensional growth potential from career progression"""
        if not work_experience or len(work_experience) < 2:
            print("   ⚠️  Insufficient work experience for growth calculation")
            return {
                'growth_potential_score': 0, 
                'growth_dimensions': {
                    'vertical_growth': 0,
                    'scope_growth': 0, 
                    'impact_growth': 0,
                    'adaptability': 0,
                    'leadership_velocity': 0
                }
            }
        # FIX: Reverse work experience to get chronological order (oldest first)
        chronological_experience = list(reversed(work_experience))
        print(f"   📅 Chronological order: {[exp['role_title'] for exp in chronological_experience]}")
        
        # Calculate individual growth dimensions (use chronological_experience instead of work_experience)
        vertical_growth = self._calculate_vertical_growth(chronological_experience)
        scope_growth = self._calculate_scope_growth(chronological_experience)
        impact_growth = self._calculate_impact_growth(chronological_experience)
        adaptability = self._calculate_adaptability(chronological_experience)
        leadership_velocity = self._calculate_leadership_velocity(chronological_experience)
                
        # Calculate overall growth score (weighted average)
        weights = {
            'vertical_growth': 0.25,
            'scope_growth': 0.20, 
            'impact_growth': 0.25,
            'adaptability': 0.15,
            'leadership_velocity': 0.15
        }
        
        overall_score = (
            vertical_growth * weights['vertical_growth'] +
            scope_growth * weights['scope_growth'] +
            impact_growth * weights['impact_growth'] + 
            adaptability * weights['adaptability'] +
            leadership_velocity * weights['leadership_velocity']
        ) * 100  # Convert to 0-100 scale
        
        growth_dimensions = {
            'vertical_growth': round(vertical_growth, 2),
            'scope_growth': round(scope_growth, 2),
            'impact_growth': round(impact_growth, 2),
            'adaptability': round(adaptability, 2),
            'leadership_velocity': round(leadership_velocity, 2)
        }
        
        print("   📈 GROWTH DIMENSIONS CALCULATED:")
        print(f"      ↗️  Vertical Growth: {vertical_growth:.2f} (Role level increases)")
        print(f"      📊 Scope Growth: {scope_growth:.2f} (Responsibility expansion)")
        print(f"      💼 Impact Growth: {impact_growth:.2f} (Business impact scale)") 
        print(f"      🔄 Adaptability: {adaptability:.2f} (Domain/company changes)")
        print(f"      ⚡ Leadership Velocity: {leadership_velocity:.2f} (Time to leadership)")
        print(f"      🎯 OVERALL GROWTH SCORE: {overall_score:.1f}/100")
        
        return {
            'growth_potential_score': round(overall_score, 1),
            'growth_dimensions': growth_dimensions,
            'promotion_velocity': self._calculate_promotion_velocity(work_experience),
            'max_role_level': max(exp['role_level'] for exp in work_experience)
        }

    def _calculate_vertical_growth(self, work_experience):
        """Calculate vertical career progression (role level increases)"""
        role_levels = [exp['role_level'] for exp in work_experience]
        
        # Count significant level increases (>1 level jump)
        level_increases = 0
        for i in range(1, len(role_levels)):
            if role_levels[i] > role_levels[i-1]:
                level_increases += (role_levels[i] - role_levels[i-1])
        
        max_possible_increases = (4 - min(role_levels)) * (len(role_levels) - 1)
        return min(1.0, level_increases / max_possible_increases) if max_possible_increases > 0 else 0

    def _calculate_scope_growth(self, work_experience):
        """Calculate scope expansion (individual → team → leadership)"""
        scope_weights = {'individual_contributor': 1, 'team_leadership': 2, 'executive': 3}
        scope_scores = [scope_weights.get(exp['scope'], 1) for exp in work_experience]
        
        # Calculate scope progression
        scope_increases = 0
        for i in range(1, len(scope_scores)):
            if scope_scores[i] > scope_scores[i-1]:
                scope_increases += (scope_scores[i] - scope_scores[i-1])
        
        max_possible_scope = (3 - min(scope_scores)) * (len(scope_scores) - 1)
        return min(1.0, scope_increases / max_possible_scope) if max_possible_scope > 0 else 0.5

    def _calculate_impact_growth(self, work_experience):
        """Calculate business impact growth based on role level and tenure"""
        # Higher level roles + longer tenure = more impact opportunity
        total_impact_score = sum(exp['role_level'] * self._get_tenure_years(exp) for exp in work_experience)
        max_possible_impact = 4 * 10 * len(work_experience)  # Level 4 * 10 years * roles
        
        return min(1.0, total_impact_score / max_possible_impact)

    def _calculate_adaptability(self, work_experience):
        """Calculate adaptability through company/domain changes"""
        companies = set(exp['company'] for exp in work_experience)
        unique_companies = len(companies)
        
        # More companies = more adaptability, but balance with stability
        if len(work_experience) <= 2:
            return 0.3  # Limited data
        elif unique_companies == len(work_experience):
            return 0.9  # Changed company every time (high adaptability)
        else:
            return min(0.8, unique_companies / len(work_experience))

    def _calculate_leadership_velocity(self, work_experience):
        """Calculate how quickly candidate reached leadership roles"""
        leadership_roles = [exp for exp in work_experience if exp['scope'] != 'individual_contributor']
        
        if not leadership_roles:
            return 0  # No leadership experience
        
        # Find first leadership role
        first_leadership_index = next((i for i, exp in enumerate(work_experience) 
                                     if exp['scope'] != 'individual_contributor'), None)
        
        if first_leadership_index == 0:
            return 1.0  # Started in leadership
        elif first_leadership_index <= len(work_experience) * 0.3:
            return 0.9  # Reached leadership quickly
        elif first_leadership_index <= len(work_experience) * 0.6:
            return 0.7  # Moderate pace to leadership
        else:
            return 0.4  # Slow to reach leadership

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