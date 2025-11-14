# 🎯 JOB DESCRIPTION PARSER - Enhanced with Real Confidence Scoring
# Improved field extraction with dynamic confidence calculation

from resume_parser import ResumeParser
import re

# ADD THESE IMPORTS:
try:
    from enhanced_cultural_extractor import EnhancedCulturalExtractor
    ENHANCED_CULTURAL_AVAILABLE = True
except ImportError:
    ENHANCED_CULTURAL_AVAILABLE = False
    print("⚠️ Enhanced cultural extractor not available, using basic method")


class JobDescriptionParser:
    def __init__(self):
        self.resume_parser = ResumeParser()

        # ADD THIS: Initialize enhanced cultural extractor
        if ENHANCED_CULTURAL_AVAILABLE:
            self.enhanced_extractor = EnhancedCulturalExtractor()
        else:
            self.enhanced_extractor = None            

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

        # NEW: Extract cultural attributes
        cultural_attributes, cultural_confidence = self.extract_cultural_attributes(text)
        
        job_data = {
            'title': title,
            'company': company,
            'location': location,
            'description': text,
            'required_skills': base_data.get('skills', []),
            'preferred_skills': [],
            'experience_required': experience,
            'employment_type': employment_type,
            # NEW: cultural attributes
            'cultural_attributes': cultural_attributes,  # The actual cultural data
            'confidence_scores': {
                'title': title_confidence,
                'company': company_confidence,
                'location': location_confidence,
                'experience': exp_confidence,
                'skills': 0.80,  # Based on resume parser performance
                'employment_type': type_confidence,
                # NEW: cultural attributes
               'cultural_fit': cultural_confidence  # NEW: Overall reliability of cultural extraction
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

    def extract_cultural_attributes(self, text):

        """Extract cultural fit attributes from job description with enhanced semantic analysis"""
        
        # Use enhanced extraction if available
        if self.enhanced_extractor and self.enhanced_extractor.semantic_enabled:
            print("   🎯 Using enhanced cultural extraction with semantic analysis")
            cultural_attributes, overall_confidence = self._extract_cultural_enhanced(text)
        else:
            print("   🔧 Using basic cultural keyword extraction")
            cultural_attributes, overall_confidence = self._extract_cultural_basic(text)
        
        return cultural_attributes, overall_confidence
    
    def _extract_cultural_enhanced(self, text):
        """Enhanced cultural extraction with semantic analysis"""
        try:
            enhanced_result = self.enhanced_extractor.extract_cultural_attributes_enhanced(text)
            
            # Convert enhanced format to match existing format
            cultural_attributes = {}
            total_confidence = 0
            
            for attr, (score, confidence) in enhanced_result.items():
                cultural_attributes[attr] = (score, confidence)
                total_confidence += confidence
            
            overall_confidence = total_confidence / len(cultural_attributes) if cultural_attributes else 0.3
            
            return cultural_attributes, overall_confidence
            
        except Exception as e:
            print(f"⚠️ Enhanced cultural extraction failed: {e}")
            # Fallback to basic extraction
            return self._extract_cultural_basic(text)
    
    def _extract_cultural_basic(self, text):
        """Original basic cultural extraction (keep your existing code)"""
        text_lower = text.lower()
    
        cultural_attributes = {
            'teamwork': (0.5, 0.3),
            'innovation': (0.5, 0.3),
            'work_environment': (0.5, 0.3),
            'work_pace': (0.5, 0.3),
            'customer_focus': (0.5, 0.3)
        }
    


#        """Extract cultural fit attributes from job description with confidence scores"""
#        text_lower = text.lower()
    
#        cultural_attributes = {
#            'teamwork': (0.5, 0.3),
#            'innovation': (0.5, 0.3),
#            'work_environment': (0.5, 0.3),
#            'work_pace': (0.5, 0.3),
#            'customer_focus': (0.5, 0.3)
#        }
    
        # Teamwork indicators
        teamwork_terms = ['team', 'collaborat', 'partner', 'work together', 'group project', 'cross-functional']
        cultural_attributes['teamwork'] = self._calculate_cultural_score(text_lower, teamwork_terms)
    
        # Innovation indicators  
        innovation_terms = ['innovati', 'creativ', 'initiative', 'think outside', 'new ideas', 'problem solv']
        cultural_attributes['innovation'] = self._calculate_cultural_score(text_lower, innovation_terms)
    
        # Work environment preferences
        remote_terms = ['remote', 'work from home', 'wfh', 'virtual office']
        office_terms = ['office', 'on-site', 'in-person', 'physical workspace']
        hybrid_terms = ['hybrid', 'flexible work', 'partial remote']
    
        env_scores = [
            self._calculate_cultural_score(text_lower, remote_terms),
            self._calculate_cultural_score(text_lower, office_terms), 
            self._calculate_cultural_score(text_lower, hybrid_terms)
        ]
        best_env_score = max(env_scores)
        cultural_attributes['work_environment'] = best_env_score if best_env_score[1] > 0.3 else (0.5, 0.3)
    
        # Work pace indicators
        fast_pace_terms = ['fast-paced', 'dynamic', 'rapid', 'startup', 'agile', 'high-growth']
        methodical_terms = ['stable', 'methodical', 'structured', 'process-driven', 'established']
    
        pace_scores = [
          self._calculate_cultural_score(text_lower, fast_pace_terms),
          self._calculate_cultural_score(text_lower, methodical_terms)
        ]
        best_pace_score = max(pace_scores)
        cultural_attributes['work_pace'] = best_pace_score if best_pace_score[1] > 0.3 else (0.5, 0.3)
    
        # Customer focus indicators
        customer_terms = ['customer', 'client focus', 'user experience', 'stakeholder', 'end user']
        cultural_attributes['customer_focus'] = self._calculate_cultural_score(text_lower, customer_terms)
    
        # Calculate overall cultural fit confidence
        total_confidence = sum(attr[1] for attr in cultural_attributes.values())
        overall_confidence = total_confidence / len(cultural_attributes)
    
        # DEFAULT ASSUMPTION - if no strong cultural signals detected
        if overall_confidence < 0.4:  # If low confidence across all attributes
            overall_confidence = 0.30  # Set to default low confidence

        return cultural_attributes, overall_confidence  # Default return
    
    def _calculate_cultural_score(self, text, terms):
        """Calculate cultural attribute presence score with confidence"""
        matches = sum(1 for term in terms if term in text)
        max_possible = len(terms)
    
        if matches == 0:
            return (0.5, 0.3)  # Default neutral with low confidence
    
        score = matches / max(1, max_possible)
        confidence = min(0.3 + (matches * 0.15), 0.9)  # Confidence based on number of matches
    
        return (score, confidence)