# 📄 ENHANCED RESUME PARSER WITH GROWTH DATA
# Maintains all existing functionality while adding growth analysis

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Enhanced cultural extractor
try:
    from enhanced_cultural_extractor import EnhancedCulturalExtractor
    ENHANCED_CULTURAL_AVAILABLE = True
except ImportError:
    ENHANCED_CULTURAL_AVAILABLE = False
    print("⚠️ Enhanced cultural extractor not available, using basic method")

class ResumeParser:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        
        # KEEP YOUR EXISTING COMPREHENSIVE SKILL KEYWORDS
        self.skill_keywords = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust'],
            'web': ['html', 'css', 'react', 'angular', 'vue', 'django', 'flask', 'node.js', 'express', 'spring'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd'],
            'data_science': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'statistics'],
            'soft_skills': ['leadership', 'communication', 'teamwork', 'problem solving', 'analytical', 'agile', 'scrum']
        }
        
        # KEEP YOUR EXISTING CULTURAL ATTRIBUTE KEYWORDS
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

        # NEW: Growth data extractors
        self.extractors = {
            'core': self._extract_core_profile,
            'career_timeline': self._extract_career_timeline,
            'skill_progression': self._extract_skill_progression,
            'growth_metrics': self._extract_growth_metrics
        }

        print("✅ Enhanced resume parser initialized with growth analysis!")
    
    def parse_resume_text(self, resume_text):
        """Parse resume text and extract structured information - EXISTING FUNCTION"""
        print(f"🔍 Parsing resume text ({len(resume_text)} characters)...")
        
        # Extract basic information using existing logic
        extracted_info = {
            'name': self.extract_name(resume_text),
            'email': self.extract_email(resume_text),
            'phone': self.extract_phone(resume_text),
            'skills': self.extract_skills(resume_text),
            'experience': self.extract_experience(resume_text),
            'education': self.extract_education(resume_text),
            'summary': self.generate_summary(resume_text),
            'cultural_attributes': self.extract_cultural_attributes(resume_text)            
        }
        
        print(f"✅ Extracted: {extracted_info['name']} | {len(extracted_info['skills'])} skills | {extracted_info['experience']} years experience")
        
        return extracted_info
    
    def parse_resume_to_candidate(self, resume_text, candidate_name=None, include_extensions=None):
        """Enhanced: Convert parsed resume into candidate format with growth data"""
        # Default to core only for backward compatibility
        if include_extensions is None:
            include_extensions = ['core']
        
        # Get core data using existing method
        parsed_data = self.parse_resume_text(resume_text)
        
        # Start with core candidate data
        candidate_data = {
            "name": candidate_name or parsed_data['name'],
            "profile": parsed_data['summary'],
            "skills": parsed_data['skills'],
            "experience_years": parsed_data['experience'],
            "location": "Location not specified",
            "email": parsed_data['email'],
            "phone": parsed_data['phone'],
            "education": parsed_data['education'],
            "cultural_attributes": parsed_data['cultural_attributes']
        }
        
        # Add growth data if requested
        for extractor_name in include_extensions:
            if extractor_name in self.extractors and extractor_name != 'core':
                try:
                    growth_data = self.extractors[extractor_name](resume_text)
                    candidate_data.update(growth_data)
                except Exception as e:
                    print(f"⚠️ Growth extractor '{extractor_name}' failed: {e}")
        
        return candidate_data
    
    def get_embedding_text(self, candidate_data: Dict[str, Any]) -> str:
        """Generate enhanced text for embedding that includes growth context"""
        core_text = f"{candidate_data.get('name', '')} {candidate_data.get('profile', '')}"
        
        # Add growth context to embedding
        growth_context = self._build_growth_context(candidate_data)
        
        return f"{core_text} {growth_context}".strip()
    
    def _build_growth_context(self, candidate_data: Dict[str, Any]) -> str:
        """Build growth context text for enhanced embeddings"""
        growth_parts = []
        
        # Career progression context
        work_exp = candidate_data.get('work_experience', [])
        if work_exp:
            roles = [exp.get('role_title', '') for exp in work_exp]
            growth_parts.append(f"Career progression: {' -> '.join(roles)}")
        
        # Skill progression context  
        skills = candidate_data.get('skill_timeline', [])
        if skills:
            skill_names = [skill.get('skill', '') for skill in skills]
            growth_parts.append(f"Skills: {', '.join(skill_names)}")
        
        # Growth metrics context
        growth_metrics = candidate_data.get('growth_metrics', {})
        if growth_metrics:
            trajectory = growth_metrics.get('career_trajectory_score', 0)
            learning = growth_metrics.get('learning_agility', 0)
            growth_parts.append(f"Growth potential: {trajectory:.1f} trajectory, {learning:.1f} learning agility")
        
        return " ".join(growth_parts)
    
    # NEW: Growth data extraction methods
    def _extract_core_profile(self, text: str) -> Dict[str, Any]:
        """Core profile extraction - uses existing parse_resume_text"""
        return self.parse_resume_text(text)
    
    def _extract_career_timeline(self, text: str) -> Dict[str, Any]:
        """Extract chronological work history and role progression"""
        work_experience = self._parse_work_experience(text)
        career_metrics = self._calculate_career_metrics(work_experience)
        
        return {
            "work_experience": work_experience,
            "career_metrics": career_metrics
        }
    
    def _extract_skill_progression(self, text: str) -> Dict[str, Any]:
        """Extract skill acquisition timeline and proficiency"""
        skill_timeline = self._build_skill_timeline(text)
        learning_velocity = self._calculate_learning_velocity(skill_timeline)
        
        return {
            "skill_timeline": skill_timeline,
            "learning_velocity": learning_velocity
        }
    
    def _extract_growth_metrics(self, text: str) -> Dict[str, Any]:
        """Calculate growth potential metrics"""
        work_experience = self._parse_work_experience(text)
        skill_timeline = self._build_skill_timeline(text)
        
        growth_metrics = {
            "promotion_velocity": self._calculate_promotion_velocity(work_experience),
            "scope_expansion_rate": self._calculate_scope_expansion(work_experience),
            "career_trajectory_score": self._calculate_trajectory_score(work_experience),
            "learning_agility": self._calculate_learning_agility(skill_timeline),
            "growth_potential_score": self._calculate_growth_potential_score(work_experience, skill_timeline)
        }
        
        return {"growth_metrics": growth_metrics}
    
    # KEEP ALL YOUR EXISTING METHODS (they remain unchanged)
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
        """Extract skills from resume text - USING YOUR COMPREHENSIVE KEYWORDS"""
        text_lower = text.lower()
        found_skills = []
        
        # Check each skill category from your comprehensive list
        for category, skills in self.skill_keywords.items():
            for skill in skills:
                if skill in text_lower:
                    found_skills.append(skill)
        
        # Remove duplicates and return
        return list(set(found_skills))
    
    def extract_experience(self, text):
        """Extract years of experience (simple heuristic)"""
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
            top_skills = skills[:4]
            summary = f"Professional with {experience} years of experience. Skilled in {', '.join(top_skills)}."
        else:
            summary = f"Experienced professional with {experience} years in the industry."
        
        return summary

    def extract_cultural_attributes(self, text):
        """Extract cultural fit attributes with enhanced semantic analysis - USING YOUR KEYWORDS"""
        # Use enhanced extraction if available
        if self.enhanced_extractor and self.enhanced_extractor.semantic_enabled:
            return self.enhanced_extractor.extract_cultural_attributes_enhanced(text)
    
        # Fallback to YOUR original keyword extraction
        text_lower = text.lower()
        cultural_attributes = {}
    
        for attribute, keywords in self.cultural_keywords.items():
            matches = []
            for keyword in keywords:
                if keyword in text_lower:
                    matches.append(keyword)
        
            # Calculate score based on percentage of keywords found
            if matches:
                score = len(matches) / len(keywords)
            else:
                score = 0.0
            
            cultural_attributes[attribute] = score
   
        return cultural_attributes

    # NEW: Growth analysis helper methods

    def _parse_work_experience(self, text: str) -> List[Dict[str, Any]]:
        """Parse work experience with dates and role details - ENHANCED VERSION"""
        work_experience = []
    
        # ENHANCED: Better pattern matching for various resume formats
        sections = re.split(r'\n\s*(?:Experience|Work History|Employment|Work Experience|Career)', text, flags=re.IGNORECASE)
    
        if len(sections) > 1:
            experience_text = sections[1]
        
            # ENHANCED: Multiple patterns for different resume formats
            role_patterns = [
                # Pipe-separated format: "Role | Company | Location | Dates"
                r'([^|\n]+)\s*\|\s*([^|\n]+)\s*\|\s*([^|\n]+)\s*\|\s*([^|\n]+)',
                # Dash-separated format: "Role - Company - Location - Dates"  
                r'([^-\n]+)\s*-\s*([^-\n]+)\s*-\s*([^-\n]+)\s*-\s*([^-\n]+)',
                # Simple "at" format: "Role at Company (Dates)"
                    r'([^@\n]+)\s+at\s+([^(]+)\s*\(([^)]+)\)',
                # Role and company on same line
                r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+at\s+([A-Z][a-zA-Z0-9\s&]+)',
            ]
        
            for pattern in role_patterns:
                matches = re.finditer(pattern, experience_text)
                for match in matches:
                    try:
                        if len(match.groups()) >= 2:
                            role_title = match.group(1).strip()
                            company = match.group(2).strip()
                        
                            # Skip if these are clearly not roles (too short, common words)
                            if len(role_title) < 3 or role_title.lower() in ['python', 'java', 'javascript', 'react']:
                                continue
                            
                            # Skip if company looks like a skill
                            if any(skill in company.lower() for skill in ['python', 'tensorflow', 'kubernetes', 'docker']):
                                continue
                        
                            work_experience.append({
                                "role_title": role_title,
                                "company": company,
                                "duration": match.group(4).strip() if len(match.groups()) >= 4 else "Extracted duration",
                                "role_level": self._infer_role_level(role_title),
                                "scope": self._infer_scope(role_title, company)
                            })
                    except Exception as e:
                        continue  # Skip problematic matches
        
            # ENHANCED: Also look for bullet points with role context
            bullet_points = re.finditer(r'[-•*]\s*(.+?)(?=\n[-•*]|\n\n|$)', experience_text)
            for bullet in bullet_points:
                bullet_text = bullet.group(1).lower()
                # Look for leadership/management indicators in bullet points
                if any(word in bullet_text for word in ['led', 'managed', 'directed', 'oversaw', 'supervised']):
                    # Try to find the most recent role to associate this achievement with
                    if work_experience:
                        work_experience[-1]['achievements'] = work_experience[-1].get('achievements', []) + [bullet.group(1)]
    
        # Limit and return
        return work_experience[:8]  # Limit to most recent 8 roles
    
    def _build_skill_timeline(self, text: str) -> List[Dict[str, Any]]:
        """Build timeline of skill acquisition USING YOUR COMPREHENSIVE SKILLS"""
        skills = self.extract_skills(text)
        
        skill_timeline = []
        for skill in skills:
            skill_timeline.append({
                "skill": skill,
                "first_mentioned": "Inferred from context",
                "proficiency_level": self._infer_proficiency(skill, text),
                "category": self._categorize_skill(skill),
                "relevance_score": self._calculate_skill_relevance(skill, text)
            })
        
        return skill_timeline
    
    def _calculate_career_metrics(self, work_experience: List[Dict]) -> Dict[str, Any]:
        """Calculate career progression metrics"""
        if not work_experience:
            return {
                "average_tenure_months": 0,
                "career_progression_slope": 0,
                "number_of_companies": 0,
                "role_variety_score": 0,
                "leadership_experience": False
            }
        
        tenure_months = [self._parse_duration(exp.get('duration', '')) for exp in work_experience]
        avg_tenure = sum(tenure_months) / len(tenure_months) if tenure_months else 0
        
        role_levels = [exp.get('role_level', 0) for exp in work_experience]
        progression_slope = self._calculate_progression_slope(role_levels)
        
        return {
            "average_tenure_months": avg_tenure,
            "career_progression_slope": progression_slope,
            "number_of_companies": len(set(exp.get('company', '') for exp in work_experience)),
            "role_variety_score": self._calculate_role_variety(work_experience),
            "leadership_experience": any(exp.get('scope') == 'team_leadership' for exp in work_experience)
        }
    
    def _calculate_growth_potential_score(self, work_experience: List[Dict], skill_timeline: List[Dict]) -> float:
        """Calculate overall growth potential score (0-100)"""
        if not work_experience:
            return 50.0  # Default neutral score
        
        career_metrics = self._calculate_career_metrics(work_experience)
        
        # Weighted factors for growth potential
        factors = {
            'career_progression': career_metrics.get('career_progression_slope', 0) * 30,
            'learning_velocity': len(skill_timeline) * 2,
            'role_variety': career_metrics.get('role_variety_score', 0) * 20,
            'leadership_potential': 15 if career_metrics.get('leadership_experience') else 5
        }
        
        total_score = sum(factors.values())
        return min(max(total_score, 0), 100)
    
    # Growth analysis helper methods (same as before)

    def _infer_role_level(self, role_title: str) -> int:
        """Infer role hierarchy level from title - ENHANCED"""
        role_title_lower = role_title.lower()
    
        # Executive level
        if any(word in role_title_lower for word in ['director', 'vp', 'vice president', 'cto', 'ceo', 'head of']):
            return 5
        # Senior management
        elif any(word in role_title_lower for word in ['manager', 'lead', 'principal']):
            return 4
        # Senior individual contributor
        elif any(word in role_title_lower for word in ['senior', 'staff', 'architect']):
            return 3
        # Mid-level
        elif any(word in role_title_lower for word in ['engineer', 'developer', 'analyst', 'specialist']):
            return 2
        # Entry level
        elif any(word in role_title_lower for word in ['junior', 'associate', 'intern', 'trainee']):
            return 1
        else:
            return 2  # Default mid-level

    
    def _infer_scope(self, role_title: str, company: str) -> str:
        role_title_lower = role_title.lower()
        if any(word in role_title_lower for word in ['manager', 'director', 'head', 'lead']):
            return "team_leadership"
        elif any(word in role_title_lower for word in ['senior', 'principal']):
            return "individual_contributor_advanced"
        else:
            return "individual_contributor"
    
    def _parse_duration(self, duration_text: str) -> int:
        return 24  # Default 2 years
    
    def _calculate_progression_slope(self, role_levels: List[int]) -> float:
        if len(role_levels) < 2: return 0.0
        x = list(range(len(role_levels)))
        slope = sum((x[i] - sum(x)/len(x)) * (role_levels[i] - sum(role_levels)/len(role_levels)) for i in range(len(role_levels)))
        slope /= sum((x[i] - sum(x)/len(x)) ** 2 for i in range(len(role_levels)))
        return max(slope, 0.0)
    
    def _calculate_role_variety(self, work_experience: List[Dict]) -> float:
        unique_roles = len(set(exp.get('role_title', '') for exp in work_experience))
        unique_companies = len(set(exp.get('company', '') for exp in work_experience))
        return (unique_roles + unique_companies) / max(len(work_experience) * 2, 1)
    
    def _infer_proficiency(self, skill: str, text: str) -> str:
        skill_context = re.findall(rf'.{{0,50}}{re.escape(skill)}.{{0,50}}', text, re.IGNORECASE)
        context_text = ' '.join(skill_context).lower()
        if any(word in context_text for word in ['expert', 'advanced', 'senior', 'lead']): return "advanced"
        elif any(word in context_text for word in ['proficient', 'experienced', 'skilled']): return "intermediate"
        else: return "basic"
    
    def _categorize_skill(self, skill: str) -> str:
        tech_skills = {'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust'}
        data_skills = {'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'statistics', 'data analysis'}
        if skill in tech_skills: return "technical"
        elif skill in data_skills: return "data_science"
        else: return "general"
    
    def _calculate_skill_relevance(self, skill: str, text: str) -> float:
        skill_occurrences = len(re.findall(rf'\b{re.escape(skill)}\b', text, re.IGNORECASE))
        return min(skill_occurrences / 5.0, 1.0)
    
    def _calculate_promotion_velocity(self, work_experience: List[Dict]) -> float:
        if len(work_experience) < 2: return 0.0
        role_levels = [exp.get('role_level', 0) for exp in work_experience]
        return max(role_levels) - min(role_levels)
    
    def _calculate_scope_expansion(self, work_experience: List[Dict]) -> float:
        if len(work_experience) < 2: return 0.0
        scopes = [1 if exp.get('scope') == 'team_leadership' else 0 for exp in work_experience]
        return sum(scopes) / len(scopes)
    
    def _calculate_trajectory_score(self, work_experience: List[Dict]) -> float:
        metrics = self._calculate_career_metrics(work_experience)
        promotion_velocity = self._calculate_promotion_velocity(work_experience)
        scope_expansion = self._calculate_scope_expansion(work_experience)
        return (metrics.get('career_progression_slope', 0) + promotion_velocity + scope_expansion) / 3
    
    def _calculate_learning_velocity(self, skill_timeline: List[Dict]) -> float:
        if len(skill_timeline) < 2: return 0.0
        return len(skill_timeline) / 5.0
    
    def _calculate_learning_agility(self, skill_timeline: List[Dict]) -> float:
        categories = [skill['category'] for skill in skill_timeline]
        unique_categories = len(set(categories))
        return min(unique_categories / 3.0, 1.0)

# Backward compatibility - existing function interface
def parse_resume_to_candidate(resume_text: str, candidate_name: str = None) -> Dict[str, Any]:
    """Legacy function for backward compatibility"""
    parser = ResumeParser()
    return parser.parse_resume_to_candidate(resume_text, candidate_name, include_extensions=['core'])

# Global instance for module-level usage
resume_parser = ResumeParser()

def main():
    """Test the resume parser - EXISTING CODE UNCHANGED"""
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

# NEW: Test growth data extraction
    print("\n🧪 TESTING GROWTH DATA EXTRACTION")
    print("=" * 50)
    
    candidate_with_growth = parser.parse_resume_to_candidate(
        sample_resume, 
        include_extensions=['core', 'career_timeline', 'skill_progression', 'growth_metrics']
    )
    
    print("\n📈 GROWTH DATA:")
    print(f"Growth Potential Score: {candidate_with_growth.get('growth_metrics', {}).get('growth_potential_score', 0)}")
    print(f"Career Progression: {candidate_with_growth.get('career_metrics', {}).get('career_progression_slope', 0)}")
    print(f"Work Experience: {len(candidate_with_growth.get('work_experience', []))} roles")

if __name__ == "__main__":
    main()