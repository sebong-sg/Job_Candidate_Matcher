# 🎯 JOB DESCRIPTION PARSER - Enhanced with Quality Assessment & Growth Requirements
# Robust parsing with quality flags and improvement suggestions

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

        # NEW: Enhanced extraction patterns
        self.skill_proficiency_keywords = {
            'expert': ['expert', 'senior', 'lead', 'advanced', 'master', 'deep knowledge', 'extensive experience'],
            'intermediate': ['intermediate', 'mid-level', 'proficient', 'strong experience', 'solid understanding', 'hands-on'],
            'basic': ['basic', 'familiar', 'aware', 'knowledge of', 'understanding of', 'exposure to']
        }
        
        self.seniority_keywords = {
            'junior': ['junior', 'entry-level', 'graduate', '0-2 years', '1-3 years', 'associate'],
            'mid': ['mid-level', 'intermediate', '3-5 years', '4-7 years', 'experienced'],
            'senior': ['senior', 'lead', '5+ years', '7+ years', 'expert', 'principal'],
            'principal': ['principal', 'staff', 'architect', '10+ years', 'strategic']
        }
        
        self.career_archetypes = {
            'high_growth_ic': ['individual contributor', 'technical track', 'specialist', 'expert'],
            'strategic_executive': ['executive', 'director', 'vp', 'head of', 'chief'],
            'technical_specialist': ['technical', 'engineer', 'developer', 'scientist'],
            'portfolio_leader': ['manager', 'lead', 'supervisor', 'team lead']
        }

        # NEW: Quality assessment thresholds
        self.quality_thresholds = {
            'high': 0.8,      # Excellent JD - full enhanced extraction
            'medium': 0.6,    # Good JD - enhanced extraction  
            'low': 0.4,       # Poor JD - basic extraction with warnings
            'very_low': 0.2   # Very poor - flag for rewriting
        }
        
        # NEW: Required fields for good JD quality
        self.required_fields = ['title', 'company', 'description', 'required_skills']
        self.recommended_fields = ['experience_required', 'location', 'employment_type']

        print("✅ Enhanced Job Description Parser initialized with quality assessment!")

    def parse_job_description(self, text):
        """
        Parse job description with quality assessment and confidence flags
        Maintains backward compatibility with existing code
        """
        if not text or len(text.strip()) < 50:
            return self._get_minimal_job_data(text)
        
        # Get base extraction using resume parser (existing functionality)
        base_data = self.resume_parser.parse_resume_to_candidate(text)
        
        # NEW: Assess JD quality first
        quality_score, quality_issues = self._assess_job_description_quality(text, base_data)
        quality_level = self._get_quality_level(quality_score)
        
        # Extract basic fields (always work - existing functionality)
        title, title_confidence = self._extract_job_title(text)
        company, company_confidence = self._extract_company(text)
        location, location_confidence = self._extract_location(text)
        experience, exp_confidence = self._extract_experience(text)
        employment_type, type_confidence = self._extract_employment_type(text)
        cultural_attributes, cultural_confidence = self.extract_cultural_attributes(text)
        
        # CONDITIONAL: Only extract enhanced data for medium+ quality JDs
        enhanced_data = {}
        enhancement_confidence = 0.3  # Default low confidence
        
        if quality_level in ['high', 'medium']:
            enhanced_data = {
                'growth_requirements': self._extract_growth_requirements(text),
                'skill_requirements': self._extract_skill_requirements_enhanced(text, base_data.get('skills', [])),
                'career_progression': self._extract_career_progression(text)
            }
            enhancement_confidence = 0.7
        else:
            # For low quality JDs, provide defaults with low confidence
            enhanced_data = self._get_default_enhanced_data()
        
        # Build job data (maintains existing structure)
        job_data = {
            # Existing fields (backward compatible)
            'title': title,
            'company': company,
            'location': location,
            'description': text,
            'required_skills': base_data.get('skills', []),
            'preferred_skills': [],
            'experience_required': experience,
            'employment_type': employment_type,
            'cultural_attributes': cultural_attributes,
            
            # Enhanced dimensions (conditionally populated - NEW)
            **enhanced_data,
            
            # NEW: Quality assessment metadata
            'quality_assessment': {
                'quality_score': round(quality_score, 2),
                'quality_level': quality_level,
                'quality_issues': quality_issues,
                'missing_required_fields': self._get_missing_required_fields({
                    'title': title, 'company': company, 'description': text, 
                    'required_skills': base_data.get('skills', [])
                }),
                'missing_recommended_fields': self._get_missing_recommended_fields({
                    'experience_required': experience, 'location': location, 
                    'employment_type': employment_type
                }),
                'suggestions_for_improvement': self._get_improvement_suggestions(quality_issues)
            },
            
            # Confidence scores (enhanced existing structure)
            'confidence_scores': {
                'title': title_confidence,
                'company': company_confidence,
                'location': location_confidence,
                'experience': exp_confidence,
                'skills': 0.80,
                'employment_type': type_confidence,
                'cultural_fit': cultural_confidence,
                'overall_quality': quality_score,
                'enhanced_data': enhancement_confidence  # NEW
            }
        }
        
        print(f"✅ Job parsed: {job_data['title']} at {job_data['company']} (Quality: {quality_level})")
        return job_data

    def _assess_job_description_quality(self, text, base_data):
        """Comprehensive JD quality assessment"""
        quality_score = 0.5  # Base score
        issues = []
        
        # 1. Length assessment
        text_length = len(text.strip())
        if text_length < 200:
            quality_score -= 0.3
            issues.append("Job description is too short (less than 200 characters)")
        elif text_length > 2000:
            quality_score += 0.1
        else:
            quality_score += 0.2
        
        # 2. Structure assessment
        sections_found = self._detect_jd_sections(text)
        if len(sections_found) >= 3:
            quality_score += 0.2
        else:
            issues.append("Missing key sections (Responsibilities, Requirements, etc.)")
        
        # 3. Content completeness
        skills_found = len(base_data.get('skills', []))
        if skills_found >= 5:
            quality_score += 0.2
        elif skills_found < 2:
            quality_score -= 0.2
            issues.append("Very few skills specified")
        
        # 4. Specificity assessment
        specificity_score = self._assess_specificity(text)
        quality_score += specificity_score * 0.2
        
        if specificity_score < 0.3:
            issues.append("Job description is too vague")
        
        # 5. Required fields check
        if not base_data.get('skills'):
            quality_score -= 0.1
            issues.append("No specific skills identified")
        
        return max(0.1, min(1.0, quality_score)), issues

    def _detect_jd_sections(self, text):
        """Detect common JD sections"""
        sections = []
        section_headers = [
            'responsibilities', 'requirements', 'qualifications', 'skills',
            'experience', 'education', 'about the role', 'what you will do',
            'key responsibilities', 'job requirements', 'must have', 'nice to have'
        ]
        
        lines = text.lower().split('\n')
        for line in lines:
            line = line.strip()
            for header in section_headers:
                if header in line and len(line.split()) < 8:  # Likely a section header
                    sections.append(header)
                    break
        
        return list(set(sections))  # Remove duplicates

    def _assess_specificity(self, text):
        """Assess how specific the JD is"""
        text_lower = text.lower()
        vague_terms = ['etc', 'and more', 'similar', 'various', 'other', 'additional', 'etc.']
        specific_terms = ['years of experience', 'proficient in', 'experience with', 'knowledge of', 'bachelor', 'master', 'phd']
        
        vague_count = sum(1 for term in vague_terms if term in text_lower)
        specific_count = sum(1 for term in specific_terms if term in text_lower)
        
        if specific_count + vague_count == 0:
            return 0.3  # Neutral
        
        specificity_ratio = specific_count / (specific_count + vague_count + 1)  # +1 to avoid division by zero
        return specificity_ratio

    def _get_quality_level(self, score):
        """Convert quality score to level"""
        if score >= self.quality_thresholds['high']:
            return 'high'
        elif score >= self.quality_thresholds['medium']:
            return 'medium'
        elif score >= self.quality_thresholds['low']:
            return 'low'
        else:
            return 'very_low'

    def _get_missing_required_fields(self, job_data):
        """Identify missing required fields"""
        missing = []
        if not job_data.get('title') or job_data['title'] in ['Job Title', 'Unknown']:
            missing.append('title')
        if not job_data.get('company') or job_data['company'] in ['Company', 'Unknown']:
            missing.append('company')
        if not job_data.get('description') or len(job_data['description'].strip()) < 50:
            missing.append('description')
        if not job_data.get('required_skills') or len(job_data['required_skills']) == 0:
            missing.append('required_skills')
        return missing

    def _get_missing_recommended_fields(self, job_data):
        """Identify missing recommended fields"""
        missing = []
        if not job_data.get('experience_required') or job_data['experience_required'] == 0:
            missing.append('experience_required')
        if not job_data.get('location') or job_data['location'] in ['Location not specified', 'Unknown']:
            missing.append('location')
        if not job_data.get('employment_type') or job_data['employment_type'] in ['Unknown', '']:
            missing.append('employment_type')
        return missing

    def _get_improvement_suggestions(self, issues):
        """Generate specific improvement suggestions"""
        suggestions = []
        
        issue_text = " ".join(issues).lower()
        
        if "too short" in issue_text:
            suggestions.append("Expand job description to at least 500 characters with detailed responsibilities")
        
        if "missing key sections" in issue_text:
            suggestions.append("Add clear sections: Responsibilities, Requirements, Qualifications, About the Role")
        
        if "few skills" in issue_text or "no specific skills" in issue_text:
            suggestions.append("List at least 5-7 specific technical and soft skills required")
        
        if "too vague" in issue_text:
            suggestions.append("Use specific terms instead of vague language - be precise about requirements")
        
        # Always include general best practices
        suggestions.extend([
            "Include specific years of experience required (e.g., '3+ years of Python experience')",
            "List both technical skills and soft skills separately",
            "Specify whether role is remote, hybrid, or on-site",
            "Mention career growth opportunities and team structure"
        ])
        
        return suggestions[:5]  # Return top 5 suggestions

    def _get_default_enhanced_data(self):
        """Provide safe defaults for low-quality JDs"""
        return {
            'growth_requirements': {
                'target_career_stage': 'mid_career',
                'role_archetype': 'technical_specialist',
                'scope_level_required': 1,
                'executive_potential_required': 0.3,
                'learning_expectations': 0.5,
                'confidence': 0.3,
                'has_clear_requirements': False
            },
            'skill_requirements': {
                'core_skills': [],
                'secondary_skills': [],
                'required_proficiency': {},
                'skill_priority_weights': {},
                'confidence': 0.3
            },
            'career_progression': {
                'promotion_expectations': 'standard',
                'strategic_mobility_preferred': 0.5,
                'impact_scale_required': 0.5,
                'confidence': 0.3
            }
        }

    def _get_minimal_job_data(self, text):
        """Return minimal job data for very poor input"""
        return {
            'title': 'Job Title Needed',
            'company': 'Company Name Needed',
            'location': 'Location not specified',
            'description': text or 'Job description needed',
            'required_skills': [],
            'preferred_skills': [],
            'experience_required': 0,
            'employment_type': 'Full-time',
            'cultural_attributes': {},
            'growth_requirements': self._get_default_enhanced_data()['growth_requirements'],
            'skill_requirements': self._get_default_enhanced_data()['skill_requirements'],
            'career_progression': self._get_default_enhanced_data()['career_progression'],
            'quality_assessment': {
                'quality_score': 0.1,
                'quality_level': 'very_low',
                'quality_issues': ['Job description is empty or too short'],
                'missing_required_fields': ['title', 'company', 'description', 'required_skills'],
                'missing_recommended_fields': ['experience_required', 'location', 'employment_type'],
                'suggestions_for_improvement': [
                    'Provide a complete job description',
                    'Include job title and company name',
                    'List required skills and experience'
                ]
            },
            'confidence_scores': {
                'title': 0.1,
                'company': 0.1,
                'location': 0.1,
                'experience': 0.1,
                'skills': 0.1,
                'employment_type': 0.1,
                'cultural_fit': 0.1,
                'overall_quality': 0.1,
                'enhanced_data': 0.1
            }
        }

    # ENHANCED EXTRACTION METHODS
    def _extract_growth_requirements(self, text):
        """Extract career stage and growth expectations"""
        text_lower = text.lower()
        
        return {
            'target_career_stage': self._extract_career_stage_robust(text_lower),
            'role_archetype': self._extract_role_archetype(text_lower),
            'scope_level_required': self._extract_scope_level(text_lower),
            'executive_potential_required': self._extract_executive_potential(text_lower),
            'learning_expectations': self._extract_learning_expectations(text_lower),
            'confidence': self._calculate_growth_confidence(text_lower),
            'has_clear_requirements': self._has_clear_growth_requirements(text_lower)
        }

    def _extract_career_stage_robust(self, text_lower):
        """Robust career stage extraction with multiple fallbacks"""
        # Method 1: Explicit keywords (highest confidence)
        if any(word in text_lower for word in self.seniority_keywords['junior']):
            return 'early_career'
        elif any(word in text_lower for word in self.seniority_keywords['senior'] + self.seniority_keywords['principal']):
            return 'executive'
        elif any(word in text_lower for word in self.seniority_keywords['mid']):
            return 'mid_career'
        
        # Method 2: Experience requirements
        exp_match = re.search(r'(\d+)\+?\s*years', text_lower)
        if exp_match:
            years = int(exp_match.group(1))
            if years <= 2: return 'early_career'
            elif years <= 5: return 'mid_career'
            else: return 'executive'
        
        # Method 3: Default based on common patterns
        return 'mid_career'  # Most common case

    def _extract_role_archetype(self, text_lower):
        """Extract role archetype from job description"""
        archetype_scores = {key: 0 for key in self.career_archetypes.keys()}
        
        for archetype, keywords in self.career_archetypes.items():
            for keyword in keywords:
                if keyword in text_lower:
                    archetype_scores[archetype] += 1
        
        best_archetype = max(archetype_scores, key=archetype_scores.get)
        return best_archetype if archetype_scores[best_archetype] > 0 else 'technical_specialist'

    def _extract_scope_level(self, text_lower):
        """Extract required scope level from job description"""
        scope_indicators = {
            1: ['individual contributor', 'ic', 'specialist', 'developer', 'engineer', 'analyst'],
            2: ['team lead', 'supervisor', 'mentor', 'technical lead', 'senior'],
            3: ['manager', 'head of', 'department head', 'director'],
            4: ['vp', 'vice president', 'chief', 'cto', 'executive', 'principal']
        }
        
        for level, indicators in scope_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    return level
        
        return 1  # Default to individual contributor

    def _extract_executive_potential(self, text_lower):
        """Extract executive potential requirements"""
        executive_keywords = ['strategic', 'vision', 'leadership', 'executive', 'manage', 'direct', 'oversee']
        matches = sum(1 for keyword in executive_keywords if keyword in text_lower)
        return min(matches / len(executive_keywords), 1.0)

    def _extract_learning_expectations(self, text_lower):
        """Extract learning and development expectations"""
        learning_keywords = ['learn', 'develop', 'growth', 'training', 'mentorship', 'upskill', 'development']
        matches = sum(1 for keyword in learning_keywords if keyword in text_lower)
        return min(matches / len(learning_keywords), 1.0)

    def _calculate_growth_confidence(self, text_lower):
        """Calculate confidence for growth requirement extraction"""
        relevant_keywords = []
        for keywords in self.seniority_keywords.values():
            relevant_keywords.extend(keywords)
        for keywords in self.career_archetypes.values():
            relevant_keywords.extend(keywords)
        
        matches = sum(1 for keyword in relevant_keywords if keyword in text_lower)
        confidence = min(0.3 + (matches * 0.1), 0.9)
        return confidence

    def _has_clear_growth_requirements(self, text_lower):
        """Check if job has clear growth requirements"""
        growth_indicators = ['growth', 'career path', 'advancement', 'promotion', 'development', 'progression']
        return any(indicator in text_lower for indicator in growth_indicators)

    def _extract_skill_requirements_enhanced(self, text, basic_skills):
        """Enhanced skill extraction with proficiency levels"""
        text_lower = text.lower()
        
        # Separate core vs secondary skills
        core_skills, secondary_skills = self._classify_skill_importance(text_lower, basic_skills)
        
        # Extract proficiency requirements
        required_proficiency = self._extract_skill_proficiency(text_lower, core_skills + secondary_skills)
        
        return {
            'core_skills': core_skills,
            'secondary_skills': secondary_skills,
            'required_proficiency': required_proficiency,
            'skill_priority_weights': self._calculate_skill_priority(core_skills, secondary_skills),
            'confidence': 0.7
        }

    def _classify_skill_importance(self, text_lower, skills):
        """Classify skills as core vs secondary based on context"""
        core_indicators = ['required', 'must have', 'essential', 'mandatory', 'necessary']
        secondary_indicators = ['preferred', 'nice to have', 'bonus', 'plus']
        
        core_skills = []
        secondary_skills = []
        
        for skill in skills:
            skill_lower = skill.lower()
            # Check if skill is mentioned in core context
            if any(indicator in text_lower for indicator in core_indicators):
                # Simple check - if skill is mentioned near core indicators
                core_skills.append(skill)
            elif any(indicator in text_lower for indicator in secondary_indicators):
                secondary_skills.append(skill)
            else:
                # Default to core for important technical skills
                if skill_lower in ['python', 'java', 'javascript', 'sql', 'aws']:
                    core_skills.append(skill)
                else:
                    secondary_skills.append(skill)
        
        return core_skills, secondary_skills

    def _extract_skill_proficiency(self, text_lower, skills):
        """Extract required proficiency levels for skills"""
        proficiency = {}
        
        for skill in skills:
            skill_lower = skill.lower()
            # Check for proficiency keywords near skill mentions
            for level, keywords in self.skill_proficiency_keywords.items():
                for keyword in keywords:
                    # Simple proximity check (could be enhanced)
                    if keyword in text_lower:
                        proficiency[skill] = level
                        break
            if skill not in proficiency:
                proficiency[skill] = 'intermediate'  # Default
        
        return proficiency

    def _calculate_skill_priority(self, core_skills, secondary_skills):
        """Calculate priority weights for skills"""
        weights = {}
        total_core = len(core_skills)
        total_secondary = len(secondary_skills)
        
        # Assign higher weights to core skills
        for i, skill in enumerate(core_skills):
            weights[skill] = 0.8 + (0.2 * (i / max(1, total_core)))
        
        for i, skill in enumerate(secondary_skills):
            weights[skill] = 0.3 + (0.2 * (i / max(1, total_secondary)))
        
        return weights

    def _extract_career_progression(self, text):
        """Extract career progression expectations"""
        text_lower = text.lower()
        
        return {
            'promotion_expectations': self._extract_promotion_expectations(text_lower),
            'strategic_mobility_preferred': self._extract_strategic_mobility(text_lower),
            'impact_scale_required': self._extract_impact_scale(text_lower),
            'confidence': 0.6
        }

    def _extract_promotion_expectations(self, text_lower):
        """Extract promotion timeline expectations"""
        if 'fast-paced' in text_lower or 'rapid growth' in text_lower:
            return 'fast'
        elif 'stable' in text_lower or 'established' in text_lower:
            return 'slow'
        else:
            return 'standard'

    def _extract_strategic_mobility(self, text_lower):
        """Extract preference for strategic career moves"""
        mobility_indicators = ['cross-functional', 'multiple departments', 'varied experience', 'diverse background']
        matches = sum(1 for indicator in mobility_indicators if indicator in text_lower)
        return min(matches / len(mobility_indicators), 1.0)

    def _extract_impact_scale(self, text_lower):
        """Extract required impact scale"""
        impact_indicators = ['strategic impact', 'business impact', 'company-wide', 'organization']
        matches = sum(1 for indicator in impact_indicators if indicator in text_lower)
        return min(matches / len(impact_indicators), 1.0)

    # EXISTING METHODS (KEEP FOR BACKWARD COMPATIBILITY)
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

        return cultural_attributes, overall_confidence

    def _calculate_cultural_score(self, text, terms):
        """Calculate cultural attribute presence score with confidence"""
        matches = sum(1 for term in terms if term in text)
        max_possible = len(terms)
    
        if matches == 0:
            return (0.5, 0.3)  # Default neutral with low confidence
    
        score = matches / max(1, max_possible)
        confidence = min(0.3 + (matches * 0.15), 0.9)  # Confidence based on number of matches
    
        return (score, confidence)

# Test the enhanced parser
if __name__ == "__main__":
    print("🧪 Testing Enhanced Job Parser with Quality Assessment...")
    
    parser = JobDescriptionParser()
    
    # Test with a good job description
    good_jd = """
    Senior Python Developer
    TechInnovate Solutions
    
    We are looking for a Senior Python Developer with 5+ years of experience to join our dynamic team.
    
    Responsibilities:
    - Develop and maintain Python applications using Django and Flask
    - Design and implement RESTful APIs
    - Collaborate with cross-functional teams
    - Mentor junior developers
    
    Requirements:
    - 5+ years of Python development experience
    - Strong knowledge of Django, Flask, and SQL
    - Experience with AWS cloud services
    - Excellent problem-solving skills
    
    This is a full-time remote position with opportunities for career growth and advancement.
    """
    
    result = parser.parse_job_description(good_jd)
    print(f"✅ Good JD - Quality: {result['quality_assessment']['quality_level']} ({result['quality_assessment']['quality_score']})")
    print(f"   Growth Requirements: {result['growth_requirements']}")
    
    # Test with a poor job description
    poor_jd = "Python developer needed. Contact us for details."
    result = parser.parse_job_description(poor_jd)
    print(f"❌ Poor JD - Quality: {result['quality_assessment']['quality_level']} ({result['quality_assessment']['quality_score']})")
    print(f"   Issues: {result['quality_assessment']['quality_issues']}")