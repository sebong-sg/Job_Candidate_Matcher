# 📄 RESUME PARSER - SEMANTIC ENHANCED VERSION
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
    def __init__(self, extraction_method='hybrid'):
        self.stop_words = set(stopwords.words('english'))
        self.extraction_method = extraction_method
        
        # Initialize transformer model for semantic parsing
        self.transformer_model = None
        if extraction_method in ['transformer', 'hybrid']:
            try:
                print("🔄 Loading Sentence Transformer model...")
                self.transformer_model = SentenceTransformer('all-MiniLM-L6-v2')
                print("✅ Transformer model loaded successfully!")
            except Exception as e:
                print(f"⚠️ Failed to load transformer model: {e}")
                self.transformer_model = None
        
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
            'experience': self.extract_experience(resume_text),
            'education': self.extract_education(resume_text),
            'summary': self.generate_summary(resume_text),
            'work_experience': self.extract_work_experience(resume_text),
            'cultural_attributes': self.extract_cultural_attributes(resume_text),
            'extraction_method_used': self.extraction_method
        }
        
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
    
    def extract_experience(self, text):
        """Extract years of experience"""
        experience_patterns = [
            r'(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yr',
            r'experience.*?(\d+)\+?\s*years?'
        ]
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                return max(int(match) for match in matches)
        
        return 2
    
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
        Hybrid work experience extraction with pattern + transformer methods
        """
        if self.extraction_method == 'pattern':
            return self._extract_pattern_based(text)
        elif self.extraction_method == 'transformer':
            return self._extract_transformer_based(text)
        else:  # hybrid
            pattern_result = self._extract_pattern_based(text)
            transformer_result = self._extract_transformer_based(text)
            
            return self._merge_extraction_results(pattern_result, transformer_result)

    def _extract_pattern_based(self, text):
        """Pattern-based work experience extraction"""
        work_experience = []
        
        # Pattern 1: Role (Duration)\nCompany
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
        
        # Pattern 2: Role\nCompany, Location Duration
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
        
        # Pattern 3: Company | Role | Duration
        pattern3 = r'^(.+?)\s*[|-]\s*(.+?)\s*[|-]\s*(.+)'
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
        
        return self._finalize_experience_data(work_experience)

    def _extract_transformer_based(self, text):
        """Transformer-based semantic work experience extraction"""
        if not self.transformer_model:
            print("⚠️ Transformer model not available, falling back to pattern method")
            return self._extract_pattern_based(text)
        
        work_experience = []
        
        try:
            # Segment text into potential experience blocks
            experience_blocks = self._segment_experience_blocks(text)
            
            # Reference templates for semantic matching
            role_templates = [
                "Chief Technology Officer at Google 2018-Present",
                "Senior Software Engineer at Microsoft 2015-2018",
                "Software Developer at Startup 2012-2015",
                "Head of Engineering at Tech Company 2016-2020",
                "Director of AI at AI Company 2019-2023"
            ]
            
            template_embeddings = self.transformer_model.encode(role_templates)
            
            for block in experience_blocks:
                block_embedding = self.transformer_model.encode(block)
                similarities = util.cos_sim(block_embedding, template_embeddings)
                max_similarity, best_match_idx = torch.max(similarities, dim=1)
                
                if max_similarity.item() > 0.6:  # Confidence threshold
                    parsed_experience = self._parse_experience_semantic(block)
                    if parsed_experience and self._is_valid_company_role(parsed_experience['role_title'], parsed_experience['company']):
                        parsed_experience['confidence'] = max_similarity.item()
                        parsed_experience['method'] = 'transformer'
                        work_experience.append(parsed_experience)
                        
        except Exception as e:
            print(f"⚠️ Transformer extraction failed: {e}")
        
        return self._finalize_experience_data(work_experience)

    def _segment_experience_blocks(self, text):
        """Segment text into potential work experience blocks"""
        lines = text.split('\n')
        blocks = []
        current_block = []
        
        # Look for section headers
        experience_headers = ['experience', 'work history', 'employment', 'career', 'professional']
        
        in_experience_section = False
        bullet_count = 0
        
        for line in lines:
            line_stripped = line.strip()
            
            # Check if we're entering experience section
            if any(header in line_stripped.lower() for header in experience_headers) and len(line_stripped.split()) < 5:
                in_experience_section = True
                continue
            
            if in_experience_section:
                # Skip empty lines at start of section
                if not line_stripped and not current_block:
                    continue
                
                # Detect role-like lines (title case, not too long)
                words = line_stripped.split()
                if (len(words) >= 2 and len(words) <= 8 and 
                    any(word[0].isupper() for word in words if word) and
                    not line_stripped.startswith('•')):
                    
                    if current_block:
                        blocks.append('\n'.join(current_block))
                        current_block = []
                    
                    current_block.append(line_stripped)
                elif current_block:
                    current_block.append(line_stripped)
        
        if current_block:
            blocks.append('\n'.join(current_block))
        
        return blocks

    def _parse_experience_semantic(self, block):
        """Parse experience block using semantic patterns"""
        lines = block.split('\n')
        if not lines:
            return None
        
        # First line typically contains role/company/duration
        first_line = lines[0]
        
        # Try to extract using enhanced patterns
        patterns = [
            r'^(.+?)\s*[\(\[].*?(\d{4}\s*[–-]\s*(?:Present|\d{4})).*?[\)\]].*?at\s+(.+)$',
            r'^(.+?)\s+at\s+(.+?)\s*[\(\[].*?(\d{4}\s*[–-]\s*(?:Present|\d{4})).*?[\)\]]',
            r'^(.+?)\s*-\s*(.+?)\s*-\s*(\d{4}\s*[–-]\s*(?:Present|\d{4}))'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, first_line, re.IGNORECASE)
            if match:
                if len(match.groups()) == 3:
                    return {
                        'role_title': match.group(1).strip(),
                        'company': match.group(3).strip() if 'at' in pattern else match.group(2).strip(),
                        'duration': match.group(2).strip() if 'at' in pattern else match.group(3).strip()
                    }
        
        # Fallback: simple split-based extraction
        words = first_line.split()
        if len(words) >= 3:
            return {
                'role_title': ' '.join(words[:-2]),
                'company': words[-2],
                'duration': words[-1]
            }
        
        return None

    def _merge_extraction_results(self, pattern_results, transformer_results):
        """Merge results from both methods, preferring higher confidence"""
        all_results = pattern_results + transformer_results
        
        # Remove duplicates based on role+company
        seen = set()
        merged = []
        
        for result in sorted(all_results, key=lambda x: x.get('confidence', 0), reverse=True):
            key = (result['role_title'].lower(), result['company'].lower())
            if key not in seen:
                seen.add(key)
                merged.append(result)
        
        return merged

    def _finalize_experience_data(self, work_experience):
        """Add role level and scope to experience data"""
        for exp in work_experience:
            exp['role_level'] = self._infer_role_level(exp['role_title'])
            exp['scope'] = self._infer_role_scope(exp['role_title'])
            # Remove method field from final output
            if 'method' in exp:
                del exp['method']
        
        return work_experience if work_experience else [{
            'role_title': 'Extracted role',
            'company': 'Extracted company', 
            'duration': 'Extracted duration',
            'role_level': 2,
            'scope': 'individual_contributor'
        }]

    def _is_valid_company_role(self, role_title, company):
        """Validate that extracted role/company are not actually skills"""
        skill_indicators = ['python', 'java', 'kubernetes', 'docker', 'aws', 'machine learning', 
                           'deep learning', 'pytorch', 'tensorflow', 'go', 'react', 'angular']
        
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
    """
    
    print("🧪 TESTING SEMANTIC RESUME PARSER")
    print("=" * 50)
    
    # Test pattern method
    print("\n🔧 PATTERN METHOD:")
    parser_pattern = ResumeParser(extraction_method='pattern')
    parsed_pattern = parser_pattern.parse_resume_text(test_resume)
    for exp in parsed_pattern['work_experience']:
        print(f"  • {exp['role_title']} at {exp['company']}")
    
    # Test transformer method
    print("\n🤖 TRANSFORMER METHOD:")
    parser_transformer = ResumeParser(extraction_method='transformer')
    parsed_transformer = parser_transformer.parse_resume_text(test_resume)
    for exp in parsed_transformer['work_experience']:
        print(f"  • {exp['role_title']} at {exp['company']}")
    
    # Test hybrid method
    print("\n🔀 HYBRID METHOD:")
    parser_hybrid = ResumeParser(extraction_method='hybrid')
    parsed_hybrid = parser_hybrid.parse_resume_text(test_resume)
    for exp in parsed_hybrid['work_experience']:
        print(f"  • {exp['role_title']} at {exp['company']}")

if __name__ == "__main__":
    main()