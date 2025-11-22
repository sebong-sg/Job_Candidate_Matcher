# 📄 RESUME PARSER - ENHANCED VERSION WITH AI CAREER ASSESSMENT & GROQ PARSING
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

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    from enhanced_cultural_extractor import EnhancedCulturalExtractor
    ENHANCED_CULTURAL_AVAILABLE = True
except ImportError:
    ENHANCED_CULTURAL_AVAILABLE = False

class ResumeParser:
    def __init__(self, extraction_method='groq'):
        self.stop_words = set(stopwords.words('english'))
        self.extraction_method = extraction_method
        
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        
        if not self.groq_api_key:
            print("❌ GROQ_API_KEY environment variable not set - AI parsing required")
            raise Exception("GROQ_API_KEY not found - AI parsing is required")
        
        print("✅ Resume parser initialized with Groq AI method")
        
        # Skill keywords for cultural attribute extraction only
        self.skill_keywords = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust'],
            'web': ['html', 'css', 'react', 'angular', 'vue', 'django', 'flask', 'node.js', 'express', 'spring'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd'],
            'data_science': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'statistics'],
            'soft_skills': ['leadership', 'communication', 'teamwork', 'problem solving', 'analytical', 'agile', 'scrum']
        }
        
        self.cultural_keywords = {
            'teamwork': ['team', 'collaborat', 'partner', 'work together', 'group project', 'cross-functional'],
            'innovation': ['innovati', 'creativ', 'initiative', 'think outside', 'new ideas', 'problem solv'],
            'work_environment': ['remote', 'work from home', 'wfh', 'office', 'on-site', 'hybrid', 'flexible work'],
            'work_pace': ['fast-paced', 'dynamic', 'rapid', 'startup', 'agile', 'stable', 'methodical', 'structured'],
            'customer_focus': ['customer', 'client focus', 'user experience', 'stakeholder', 'end user']
        }

        if ENHANCED_CULTURAL_AVAILABLE:
            self.enhanced_extractor = EnhancedCulturalExtractor()
        else:
            self.enhanced_extractor = None

    def parse_resume_text(self, resume_text):
        print(f"🔍 Parsing resume text ({len(resume_text)} characters)...")
        
        if not self.groq_api_key:
            raise Exception("GROQ_API_KEY not found - AI parsing is required")
        
        try:
            print("🤖 Using Groq AI for resume parsing...")
            parsed_data = self._parse_with_groq(resume_text)
            if parsed_data:
                print("✅ Groq parsing successful")
                # Always include original text
                parsed_data['original_text'] = resume_text
                return parsed_data
            else:
                raise Exception("Groq API returned no data")
        except Exception as e:
            print(f"❌ Groq parsing failed: {e}")
            raise Exception(f"AI parsing failed: {e}")

    def _parse_with_groq(self, text):
        prompt = self._create_resume_parsing_prompt(text)
        response = self._call_groq_api(prompt)
        
        if response:
            try:
                parsed_data = json.loads(response)
                parsed_data['extraction_method_used'] = 'groq'
                
                # VALIDATE REQUIRED FIELDS - throw error if missing
                required_fields = ['name', 'email', 'experience_years', 'education', 'skills', 'summary']
                missing_fields = [field for field in required_fields if field not in parsed_data]
                
                if missing_fields:
                    print(f"❌ Groq response missing required fields: {missing_fields}")
                    raise Exception(f"Groq API response missing fields: {missing_fields}")
                
                # Ensure consistent field naming
                parsed_data['experience'] = parsed_data.get('experience_years', 0)
                
                # Add enhanced data
                work_experience = self.extract_work_experience(text)
                parsed_data['work_experience'] = work_experience
                parsed_data['cultural_attributes'] = self.extract_cultural_attributes(text)
                
                # ENHANCED: Use actual growth metrics calculation instead of hardcoded
                parsed_data['growth_metrics'] = self._calculate_growth_metrics(work_experience)
                parsed_data['career_metrics'] = self._calculate_career_metrics(work_experience)
                parsed_data['learning_velocity'] = self._calculate_learning_velocity(parsed_data)
                
                quality_assessment = self._assess_quality(text, parsed_data)
                parsed_data['quality_assessment'] = quality_assessment

                # Add original text
                parsed_data['original_text'] = text
                
                print("✅ Groq parsing completed successfully")
                return parsed_data
                
            except Exception as e:
                print(f"❌ Groq response parsing failed: {e}")
                raise Exception(f"Groq parsing failed: {str(e)}")

        return None

    def _create_resume_parsing_prompt(self, text):
        return f"""
        Analyze this resume and extract ALL required fields. If any field cannot be extracted, provide a reasonable default value.

        RESUME TEXT:
        {text}
        
        REQUIRED FIELDS (must all be present):
        - name: Full name of candidate (string)
        - email: Email address (string) 
        - phone: Phone number (string)
        - location: Location/City (string)
        - experience_years: Number of years experience (integer, 0 if not found)
        - education: Highest education degree (string)
        - skills: Array of technical and soft skills (array of strings, at least 3 items)
        - summary: Professional summary (string, 2-3 sentences)
        - career_stage: "early_career", "mid_career", or "executive" (string)
        
        IMPORTANT: 
        - ALL fields must be present in the response
        - For experience_years: Extract from phrases like "X years", "X+ years", or estimate from work history
        - For skills: Include at least 5 skills from the resume content
        - For summary: Create a 2-3 sentence professional summary
        
        Return ONLY valid JSON in this exact format:
        {{
            "name": "Extracted Name",
            "email": "extracted@email.com",
            "phone": "extracted phone",
            "location": "Extracted Location",
            "experience_years": 0,
            "education": "Extracted Education",
            "skills": ["skill1", "skill2", "skill3"],
            "summary": "Professional summary...",
            "career_stage": "mid_career"
        }}
        """

    def _call_groq_api(self, prompt):
        if not self.groq_api_key:
            return None
            
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
        
        try:
            response = requests.post(self.groq_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"❌ Groq API call failed: {e}")
            return None

    def extract_work_experience(self, text):
        # Simple work experience extraction for cultural attributes
        results = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            # Look for patterns that might indicate work experience
            if any(keyword in line.lower() for keyword in [' at ', ' - ', ' | ', ' company', ' corp', ' inc']):
                if len(line) > 10 and len(line) < 100:  # Reasonable length for a job title
                    results.append({
                        'role_title': line,
                        'company': 'Extracted Company',
                        'duration': 'Present',
                        'role_level': 2,
                        'scope': 'individual_contributor'
                    })
        
        return results if results else [{
            'role_title': 'Extracted role',
            'company': 'Extracted company', 
            'duration': 'Extracted duration',
            'role_level': 2,
            'scope': 'individual_contributor'
        }]

    def extract_cultural_attributes(self, text):
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

    # =========================================================================
    # ENHANCED GROWTH METRICS WITH AI ASSESSMENT
    # =========================================================================

    def _calculate_growth_metrics(self, work_experience):
        """Enhanced growth metrics with AI career assessment"""
        if not work_experience:
            print("   ⚠️  No work experience for growth calculation")
            return self._get_empty_growth_metrics()

        # Calculate actual experience years
        estimated_years = self._estimate_experience_from_career(work_experience)

        # Use experience years for sufficiency check
        if estimated_years < 2:
            print(f"   ⚠️  Limited experience ({estimated_years} years) for detailed growth analysis")
            return self._get_empty_growth_metrics()
    
        elif estimated_years < 4:
            print(f"   📊 Basic growth analysis for {estimated_years} years experience")
            return self._get_basic_growth_metrics(work_experience, estimated_years)
    
        else:
            # Get AI career assessment
            print("   🤖 Analyzing career progression with AI...")
            ai_assessment = self.analyze_career_with_ai(work_experience)
        
        # Reverse work experience to get chronological order (oldest first)
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
        # EQUAL WEIGHTING for all dimensions (20% each)
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
            "career_archetype": "Career_Starter",
            "career_stage": "early_career",
            "executive_potential": 0.0,
            "strategic_mobility": 0.0,
            "analysis_rationale": "No work experience available",
            "promotion_velocity": 0,
            "max_role_level": 1
        }

    def _get_basic_growth_metrics(self, work_experience, experience_years):
        """Basic growth metrics for candidates with 2-4 years experience"""
        max_role_level = max(exp.get('role_level', 1) for exp in work_experience)
    
        # Determine appropriate archetype based on role progression
        if max_role_level >= 3:  # Senior or leadership roles
            career_archetype = "growth_track_ic"
            career_stage = "mid_career"
        else:
            career_archetype = "career_starter" 
            career_stage = "early_career"
    
        # Calculate basic growth scores based on experience
        base_score = min(experience_years * 20, 60)  # Scale with experience
    
        return {
            'growth_potential_score': base_score,
            'growth_dimensions': {
                'vertical_growth': min(max_role_level / 4.0, 0.6),
                'scope_growth': 0.4,
                'impact_growth': 0.3,
                'adaptability': 0.5,
                'leadership_velocity': 0.2 if max_role_level >= 2 else 0.1
            },
            'career_archetype': career_archetype,
            'career_stage': career_stage,
            'executive_potential': 0.1,
            'strategic_mobility': 0.3,
            'analysis_rationale': f"Early-mid career professional with {experience_years} years experience",
            'promotion_velocity': 0,
            'max_role_level': max_role_level
        }

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
            "career_archetype": "Career_Starter",
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
        skills_count = len(extracted_info.get('skills', []))
        experience_years = extracted_info.get('experience', 0)
        
        if experience_years > 0:
            velocity = skills_count / experience_years
        else:
            velocity = skills_count
        
        return velocity

    def _assess_quality(self, text, parsed_data):
        score = 0.5
        
        if len(text) > 500:
            score += 0.2
        elif len(text) < 200:
            score -= 0.2
            
        if parsed_data.get('name') and parsed_data['name'] != 'Unknown Candidate':
            score += 0.1
        if parsed_data.get('email') and parsed_data['email'] != 'email@example.com':
            score += 0.1
        if parsed_data.get('skills') and len(parsed_data['skills']) > 3:
            score += 0.1
        if parsed_data.get('work_experience') and len(parsed_data['work_experience']) > 0:
            score += 0.1
        if parsed_data.get('education') and 'not specified' not in parsed_data['education'].lower():
            score += 0.1

        # Cap the score at 1.0 (100%)
        score = min(score, 1.0)

        quality_level = 'high' if score >= 0.7 else 'medium' if score >= 0.5 else 'low'
        
        quality_issues = []
        if len(text) < 200:
            quality_issues.append('Resume is too short')
        if not parsed_data.get('skills') or len(parsed_data['skills']) < 2:
            quality_issues.append('Limited skills information')
        if not parsed_data.get('work_experience') or len(parsed_data['work_experience']) == 0:
            quality_issues.append('No work experience found')
            
        return {
            'quality_score': round(score, 2),
            'quality_level': quality_level,
            'quality_issues': quality_issues,
            'missing_required_fields': [],
            'missing_recommended_fields': [],
            'suggestions_for_improvement': [
                'Include detailed work experience with durations',
                'List specific technical skills',
                'Add education background',
                'Provide contact information'
            ]
        }

    def parse_resume_to_candidate(self, resume_text, candidate_name=None, include_extensions=None):
        parsed_data = self.parse_resume_text(resume_text)
        
        candidate_data = {
            "name": candidate_name or parsed_data['name'],
            "profile": parsed_data['summary'],
            "skills": parsed_data['skills'],
            "experience_years": parsed_data['experience'],
            "location": parsed_data.get('location', 'Location not specified'),
            "email": parsed_data['email'],
            "phone": parsed_data['phone'],
            "education": parsed_data['education'],
            "work_experience": parsed_data['work_experience'],
            "cultural_attributes": parsed_data['cultural_attributes'],
            "extraction_method": parsed_data.get('extraction_method_used', 'unknown'),
            "growth_metrics": parsed_data.get('growth_metrics', {}),
            "career_metrics": parsed_data.get('career_metrics', {}),
            "learning_velocity": parsed_data.get('learning_velocity', 0.0),
            "quality_assessment": parsed_data.get('quality_assessment', {}),
            "original_resume_text": parsed_data.get('original_text', resume_text)
        }
        
        return candidate_data

def main():
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
    
    parser = ResumeParser()
    try:
        parsed_data = parser.parse_resume_text(test_resume)
        print(f"   Experience: {parsed_data['experience']} years")
        print(f"   Education: {parsed_data['education']}")
        print(f"   Original text length: {len(parsed_data.get('original_text', ''))}")
        for exp in parsed_data['work_experience']:
            print(f"   • {exp['role_title']} at {exp['company']}")
    except Exception as e:
        print(f"   ❌ Test failed: {e}")

if __name__ == "__main__":
    main()