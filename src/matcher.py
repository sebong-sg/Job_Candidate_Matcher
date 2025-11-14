# 🚀 ENHANCED JOB MATCHING WITH CHROMA VECTOR DATABASE
# Hybrid approach: Chroma for semantic search + traditional scoring

from chroma_data_manager import ChromaDataManager
from vector_db import vector_db
from semantic_matcher import semantic_matcher
from profile_analyzer import profile_analyzer

# New imports to support the hybrid cultuiral score calc.  
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from semantic_matcher import semantic_matcher


print("=== 🤖 JOB-CANDIDATE MATCHER WITH CHROMA DB ===")

class SimpleMatcher:
    def __init__(self):
        self.db = ChromaDataManager()
        self.semantic_matcher = semantic_matcher  # ADD THIS LINE
        print("✅ Matcher initialized with Chroma Vector Database!")
    
    def calculate_skill_score(self, job_skills, candidate_skills):
        """Calculate weighted skill match score"""
        if not job_skills:
            return 0.0
        
        # Skill weights for realistic scoring
        skill_weights = {
            'python': 0.15, 'javascript': 0.12, 'java': 0.12, 'react': 0.10,
            'django': 0.08, 'flask': 0.08, 'node.js': 0.08, 'sql': 0.10,
            'mongodb': 0.07, 'docker': 0.06, 'aws': 0.06, 'machine learning': 0.12,
            'tensorflow': 0.08, 'pytorch': 0.08, 'statistics': 0.09, 'data analysis': 0.08,
            'css': 0.05, 'html': 0.05, 'git': 0.04, 'rest api': 0.06
        }
        
        total_weight = 0
        matched_weight = 0
        
        candidate_skills_lower = [skill.lower() for skill in candidate_skills]
        
        for skill in job_skills:
            skill_lower = skill.lower()
            weight = skill_weights.get(skill_lower, 0.05)
            total_weight += weight
            if skill_lower in candidate_skills_lower:
                matched_weight += weight
        
        score = matched_weight / total_weight if total_weight > 0 else 0.0
        return score
    
    def calculate_experience_score(self, job_title, candidate_experience):
        """Calculate experience suitability score"""
        job_lower = job_title.lower()
        
        if 'senior' in job_lower or 'lead' in job_lower or 'principal' in job_lower:
            required_exp = 5
        elif 'junior' in job_lower or 'entry' in job_lower:
            required_exp = 1
        else:
            required_exp = 3
        
        if candidate_experience >= required_exp:
            return 1.0
        elif candidate_experience > 0:
            return candidate_experience / required_exp
        else:
            return 0.1
    
    def calculate_global_location_score(self, job_location, candidate_location, candidate_willing_to_relocate=False, company_relocation_support=False):
        """Enhanced global location compatibility scoring"""
        if not job_location or not candidate_location:
            return 0.5
        
        job_loc = job_location.lower().strip()
        candidate_loc = candidate_location.lower().strip()
        
        # Handle remote work scenarios
        if self._is_remote(job_loc):
            return 1.0
        
        if self._is_remote(candidate_loc) and not self._is_remote(job_loc):
            return 0.3  # Candidate wants remote but job requires on-site
        
        # Exact match
        if job_loc == candidate_loc:
            return 1.0
        
        # Calculate base geographic proximity (40% weight)
        geo_score = self._calculate_geographic_proximity(job_loc, candidate_loc)
        
        # Calculate relocation practicality (30% weight)
        practical_score = self._calculate_relocation_practicality(job_loc, candidate_loc)
        
        # Calculate professional context (20% weight)
        professional_score = self._calculate_professional_context(job_loc, candidate_loc)
        
        # Calculate candidate preferences (10% weight)
        preference_score = self._calculate_preference_score(candidate_willing_to_relocate, company_relocation_support)
        
        # Weighted combined score
        base_score = (geo_score * 0.4) + (practical_score * 0.3) + (professional_score * 0.2) + (preference_score * 0.1)
        
        # Apply modifiers
        final_score = self._apply_location_modifiers(base_score, job_loc, candidate_loc)
        
        return max(0.0, min(1.0, final_score))
    
    def _is_remote(self, location):
        """Check if location indicates remote work"""
        remote_indicators = ['remote', 'anywhere', 'flexible', 'virtual', 'wfh', 'work from home']
        return any(indicator in location for indicator in remote_indicators)
    
    def _calculate_geographic_proximity(self, job_loc, candidate_loc):
        """Calculate geographic proximity score (40% weight)"""
        # Major global tech hubs and metro areas
        tech_hubs = {
            'north_america': ['san francisco', 'new york', 'seattle', 'toronto', 'chicago','austin', 'boston', 'los angeles'],
            'europe': ['london', 'berlin', 'paris', 'amsterdam', 'dublin', 'stockholm', 'barcelona'],
            'asia': ['tokyo', 'singapore', 'bangalore', 'hong kong', 'seoul', 'shanghai', 'shenzhen'],
            'south_asia': ['mumbai', 'delhi', 'bangalore', 'hyderabad', 'chennai'],
            'middle_east': ['dubai', 'tel aviv', 'riyadh'],
            'oceania': ['sydney', 'melbourne', 'auckland']
        }
        
        # Check same city/metro area
        if self._is_same_metro_area(job_loc, candidate_loc):
            return 0.9
        
        # Check same major hub
        job_hub = self._identify_tech_hub(job_loc, tech_hubs)
        candidate_hub = self._identify_tech_hub(candidate_loc, tech_hubs)
        
        if job_hub and candidate_hub and job_hub == candidate_hub:
            return 0.8  # Same hub cluster
        
        # Same country
        if self._is_same_country(job_loc, candidate_loc):
            return 0.6
        
        # Neighboring countries/same region
        if self._is_same_region(job_loc, candidate_loc):
            return 0.4
        
        # Same continent
        if self._is_same_continent(job_loc, candidate_loc):
            return 0.3
        
        # Global (different continents)
        return 0.2
    
    def _calculate_relocation_practicality(self, job_loc, candidate_loc):
        """Calculate relocation practicality score (30% weight)"""
        score = 0.5  # Base neutral score
        
        # Visa requirements consideration
        if self._has_visa_advantages(job_loc, candidate_loc):
            score += 0.2
        elif self._has_visa_complexity(job_loc, candidate_loc):
            score -= 0.2
        
        # Language compatibility
        if self._has_language_compatibility(job_loc, candidate_loc):
            score += 0.15
        
        # Cultural similarity
        if self._has_cultural_similarity(job_loc, candidate_loc):
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def _calculate_professional_context(self, job_loc, candidate_loc):
        """Calculate professional context score (20% weight)"""
        global_tech_hubs = ['san francisco', 'london', 'tokyo', 'singapore', 'bangalore', 'berlin', 'new york', 'seattle']
        
        job_is_hub = any(hub in job_loc for hub in global_tech_hubs)
        candidate_is_hub = any(hub in candidate_loc for hub in global_tech_hubs)
        
        if job_is_hub and candidate_is_hub:
            return 0.8  # Both global tech hubs
        elif job_is_hub or candidate_is_hub:
            return 0.6  # One is a tech hub
        else:
            return 0.4  # Neither major hub
    
    def _calculate_preference_score(self, willing_to_relocate, company_relocation_support):
        """Calculate preference score (10% weight)"""
        score = 0.5  # Base neutral
        
        if willing_to_relocate:
            score += 0.3
        
        if company_relocation_support:
            score += 0.2
        
        return max(0.0, min(1.0, score))
    
    def _apply_location_modifiers(self, base_score, job_loc, candidate_loc):
        """Apply final location modifiers"""
        final_score = base_score
        
        # Time zone difference penalty
        tz_penalty = self._calculate_timezone_penalty(job_loc, candidate_loc)
        final_score -= tz_penalty
        
        # Established business corridor bonus
        if self._is_established_corridor(job_loc, candidate_loc):
            final_score += 0.1
        
        return max(0.0, min(1.0, final_score))
    
    def _is_same_metro_area(self, loc1, loc2):
        """Check if locations are in same metropolitan area"""
        metro_areas = {
            'san francisco': ['oakland', 'san jose', 'berkeley', 'palo alto'],
            'london': ['greater london', 'london uk'],
            'tokyo': ['tokyo japan', 'greater tokyo'],
            'bangalore': ['bengaluru', 'bangalore india']
        }
        
        for city, areas in metro_areas.items():
            if city in loc1 and any(area in loc2 for area in areas):
                return True
            if city in loc2 and any(area in loc1 for area in areas):
                return True
        return False
    
    def _identify_tech_hub(self, location, tech_hubs):
        """Identify which tech hub cluster the location belongs to"""
        for region, hubs in tech_hubs.items():
            if any(hub in location for hub in hubs):
                return region
        return None
    
    def _is_same_country(self, loc1, loc2):
        """Simple same country detection"""
        country_indicators = {
            'usa': ['new york', 'san francisco', 'chicago', 'austin', 'boston'],
            'india': ['bangalore', 'mumbai', 'delhi', 'hyderabad', 'chennai'],
            'uk': ['london', 'manchester', 'birmingham', 'edinburgh'],
            'germany': ['berlin', 'munich', 'hamburg', 'frankfurt'],
            'japan': ['tokyo', 'osaka', 'kyoto', 'yokohama']
        }
        
        for country, cities in country_indicators.items():
            if any(city in loc1 for city in cities) and any(city in loc2 for city in cities):
                return True
        return False
    
    def _is_same_region(self, loc1, loc2):
        """Check if locations are in same geographic region"""
        regions = {
            'europe': ['london', 'berlin', 'paris', 'amsterdam', 'dublin'],
            'south_asia': ['bangalore', 'mumbai', 'delhi', 'chennai'],
            'east_asia': ['tokyo', 'seoul', 'shanghai', 'hong kong'],
            'north_america': ['san francisco', 'new york', 'toronto', 'seattle']
        }
        
        loc1_region = None
        loc2_region = None
        
        for region, cities in regions.items():
            if any(city in loc1 for city in cities):
                loc1_region = region
            if any(city in loc2 for city in cities):
                loc2_region = region
        
        return loc1_region and loc2_region and loc1_region == loc2_region
    
    def _is_same_continent(self, loc1, loc2):
        """Simple continent detection"""
        continents = {
            'asia': ['tokyo', 'singapore', 'bangalore', 'seoul', 'shanghai'],
            'europe': ['london', 'berlin', 'paris', 'amsterdam', 'dublin'],
            'north america': ['san francisco', 'new york', 'toronto', 'chicago'],
            'south america': ['sao paulo', 'buenos aires', 'bogota']
        }
        
        loc1_continent = None
        loc2_continent = None
        
        for continent, cities in continents.items():
            if any(city in loc1 for city in cities):
                loc1_continent = continent
            if any(city in loc2 for city in cities):
                loc2_continent = continent
        
        return loc1_continent and loc2_continent and loc1_continent == loc2_continent
    
    def _has_visa_advantages(self, job_loc, candidate_loc):
        """Check if visa situation is favorable"""
        # EU free movement, Commonwealth countries, etc.
        favorable_pairs = [
            ('germany', 'france'), ('uk', 'ireland'), 
            ('australia', 'new zealand'), ('canada', 'usa')
        ]
        
        for country1, country2 in favorable_pairs:
            if country1 in job_loc and country2 in candidate_loc:
                return True
            if country2 in job_loc and country1 in candidate_loc:
                return True
        return False
    
    def _has_visa_complexity(self, job_loc, candidate_loc):
        """Check if visa situation is complex"""
        # Simplified - in reality would need comprehensive visa data
        complex_pairs = [
            ('usa', 'china'), ('russia', 'europe'), 
            ('middle east', 'certain countries')  # Placeholder
        ]
        return any(pair[0] in job_loc and pair[1] in candidate_loc for pair in complex_pairs)
    
    def _has_language_compatibility(self, job_loc, candidate_loc):
        """Check language compatibility"""
        english_speaking = ['usa', 'uk', 'canada', 'australia', 'singapore', 'india']
        return any(country in job_loc for country in english_speaking) and any(country in candidate_loc for country in english_speaking)
    
    def _has_cultural_similarity(self, job_loc, candidate_loc):
        """Check cultural similarity"""
        similar_cultures = [
            ('usa', 'canada'), ('uk', 'australia'), 
            ('germany', 'france'), ('japan', 'south korea')
        ]
        return any(pair[0] in job_loc and pair[1] in candidate_loc for pair in similar_cultures)
    
    def _calculate_timezone_penalty(self, job_loc, candidate_loc):
        """Calculate timezone difference penalty"""
        # Simplified timezone estimation
        timezones = {
            'usa': -5, 'uk': 0, 'germany': 1, 'india': 5.5, 
            'singapore': 8, 'japan': 9, 'australia': 10
        }
        
        job_tz = next((tz for country, tz in timezones.items() if country in job_loc), 0)
        candidate_tz = next((tz for country, tz in timezones.items() if country in candidate_loc), 0)
        
        difference = abs(job_tz - candidate_tz)
        
        if difference <= 2:
            return 0.0
        elif difference <= 4:
            return 0.05
        elif difference <= 6:
            return 0.1
        else:
            return 0.15
    
    def _is_established_corridor(self, job_loc, candidate_loc):
        """Check if locations have established business corridor"""
        established_corridors = [
            ('san francisco', 'bangalore'), ('london', 'new york'),
            ('singapore', 'hong kong'), ('berlin', 'amsterdam')
        ]
        
        for loc1, loc2 in established_corridors:
            if loc1 in job_loc and loc2 in candidate_loc:
                return True
            if loc2 in job_loc and loc1 in candidate_loc:
                return True
        return False
    
    def get_match_grade(self, total_score):
        """Convert numerical score to letter grade"""
        if total_score >= 0.9: return 'A+'
        elif total_score >= 0.8: return 'A'
        elif total_score >= 0.7: return 'B+'
        elif total_score >= 0.6: return 'B'
        elif total_score >= 0.5: return 'C+'
        elif total_score >= 0.4: return 'C'
        else: return 'D'
    
    def find_matches(self, jobs=None, candidates=None):
        """Enhanced matching using Chroma vector database for semantic search"""
        if jobs is None:
            jobs = self.db.load_jobs()
        if candidates is None:
            candidates = self.db.load_candidates()
        
        print(f"🔍 Matching {len(jobs)} jobs using Chroma vector database...")
        print(f"   Vector DB has {vector_db.get_candidate_count()} candidates indexed")
        
        matches = {}
        
        for job_index, job in enumerate(jobs):
            print(f"\n📋 Processing: {job['title']}")
            matches[job_index] = []
            
            # Use Chroma for instant semantic search
            chroma_matches = vector_db.find_matches_for_job(job, top_k=50)
            
            for match in chroma_matches:
                candidate = match['candidate']
                
                # Calculate individual score components
                skill_score = self.calculate_skill_score(
                    job.get('required_skills', []), 
                    candidate.get('skills', [])
                )
                
                experience_score = self.calculate_experience_score(
                    job.get('title', ''), 
                    candidate.get('experience_years', 0)
                )
                
                # Use enhanced global location scoring
                location_score = self.calculate_global_location_score(
                    job.get('location', ''), 
                    candidate.get('location', '')
                )
                
                # Get semantic score from Chroma
                semantic_score = match['score']

                # Calculate cultural fit
                cultural_fit = self._calculate_cultural_fit(job, candidate)

                # Calculate total weighted score with cultural fit
                total_score = (
                    skill_score * 0.35 +           # Skill matching (reduced from 0.40)
                    experience_score * 0.25 +      # Experience rules
                    location_score * 0.15 +        # Global location scoring  
                    semantic_score * 0.20 +        # Semantic understanding from Chroma
#                    cultural_fit * 0.05            # NEW: Cultural fit (5% weight)
                    cultural_fit['final_score'] * 0.05
                )

# Below OLD code replace by above                
                # Calculate total weighted score
#                total_score = (
#                    skill_score * 0.40 +           # Skill matching
#                    experience_score * 0.25 +      # Experience rules
#                    location_score * 0.15 +        # Global location scoring  
#                    semantic_score * 0.20          # Semantic understanding from Chroma
#                )
                
                # Update the match with complete scoring
                match['score'] = total_score
                match['score_breakdown'] = {
                    'skills': int(skill_score * 100),
                    'experience': int(experience_score * 100),
                    'location': int(location_score * 100),
                    'semantic': int(semantic_score * 100),
#                    'cultural_fit': int(cultural_fit * 100)  # NEW: Add cultural fit to breakdown
                    'cultural_fit': int(cultural_fit['final_score'] * 100)  # CHANGE HERE
                }

                # ADD THIS SECTION for cultural fit breakdown
                match['cultural_breakdown'] = {
                    'keyword_score': int(cultural_fit['keyword_score'] * 100),
                    'semantic_score': int(cultural_fit['semantic_score'] * 100),  
                    'final_score': int(cultural_fit['final_score'] * 100)    
#                    'final_score': int(cultural_fit * 100)
                }

                match['match_grade'] = self.get_match_grade(total_score)
                
                matches[job_index].append(match)
            
            # Sort by final score
            matches[job_index].sort(key=lambda x: x['score'], reverse=True)
            
            print(f"   ✅ Found {len(matches[job_index])} matches using vector search")
        
        return matches, jobs, candidates
    
    def add_new_candidate(self, candidate_data):
        """Add a new candidate to both database and vector index"""
        try:
            # Add to both databases (ChromaDataManager handles both)
            candidate_id = self.db.add_candidate(candidate_data)
            if candidate_id:
                print(f"✅ Candidate added to both databases (ID: {candidate_id})")
            return candidate_id
        except Exception as e:
            print(f"❌ Error adding candidate: {e}")
            return None
    
    def add_new_job(self, job_data):
        """Add a new job to the database"""
        try:
            job_id = self.db.add_job(job_data)
            if job_id:
                print(f"✅ Job added to database (ID: {job_id})")
            return job_id
        except Exception as e:
            print(f"❌ Error adding job: {e}")
            return None
    # New Cultural Attribute method

    def _calculate_cultural_fit(self, job_data, candidate):
        """Calculate cultural fit between job and candidate"""
        job_cultural = job_data.get('cultural_attributes', {})
        candidate_cultural = candidate.get('cultural_attributes', {})
    
        if not job_cultural or not candidate_cultural:
            return {
                'keyword_score': 0.5,
                'semantic_score': 0.5,
                'final_score': 0.5
            }     
#            return 0.5
    
        total_score = 0
        count = 0
    
        for attr in ['teamwork', 'innovation', 'work_environment', 'work_pace', 'customer_focus']:
            job_score_raw = job_cultural.get(attr, 0.5)
            candidate_score_raw = candidate_cultural.get(attr, 0.5)

            # Handle case where scores are stored as tuples/lists (score, confidence)
            if isinstance(job_score_raw, (list, tuple)) and len(job_score_raw) > 0:
                job_score = job_score_raw[0]  # Take the first element (score)
            else:
                job_score = job_score_raw
            
            if isinstance(candidate_score_raw, (list, tuple)) and len(candidate_score_raw) > 0:
                candidate_score = candidate_score_raw[0]  # Take the first element (score)
            else:
                candidate_score = candidate_score_raw
        
            # Ensure scores are numbers
            try:
                job_score = float(job_score)
                candidate_score = float(candidate_score)
            except (ValueError, TypeError):
                job_score = 0.5
                candidate_score = 0.5    

            # Compatibility: 1 - absolute difference
            compatibility = 1 - abs(job_score - candidate_score)
            total_score += compatibility
            count += 1
            
        # Calculate keyword score (existing logic)
        keyword_score = total_score / count if count > 0 else 0.5
        
        # Calculate semantic score (new addition)
        semantic_score = self._calculate_semantic_cultural_fit(job_data, candidate)
        
        # Combine with 70/30 weighting (keyword emphasized)
        final_score = (0.7 * keyword_score) + (0.3 * semantic_score)
                
        return {
            'keyword_score': keyword_score,
            'semantic_score': semantic_score,
            'final_score': final_score
        }
       
#        return final_score

    def _calculate_semantic_cultural_fit(self, job_data, candidate):
        """Calculate cultural fit using semantic similarity of cultural context"""
        # Extract cultural-relevant text from job and candidate
        job_text = self._extract_cultural_context(job_data)
        candidate_text = self._extract_cultural_context(candidate)
        
        if not job_text or not candidate_text:
            return 0.5
            
        # Calculate semantic similarity
        semantic_score = self.semantic_matcher.calculate_similarity(job_text, candidate_text)
        return semantic_score
    
    def _extract_cultural_context(self, data):
        """Extract cultural-relevant text from job or candidate data"""
        cultural_text_parts = []
    
        cultural_attrs = data.get('cultural_attributes', {})
        # Extract from cultural attributes if available
        if cultural_attrs:
            # Convert numerical scores to descriptive text for semantic analysis
            for attr, value in cultural_attrs.items():
                if isinstance(value, (list, tuple)) and len(value) > 0:
                    score = value[0]
                    if score >= 0.7:
                        cultural_text_parts.append(f"strong {attr}")
                    elif score >= 0.6:
                        cultural_text_parts.append(f"moderate {attr}")
                    elif score <= 0.4:
                        cultural_text_parts.append(f"low {attr}")
        
        # Add general description for broader context
        description = data.get('description', '') or data.get('summary', '') or data.get('role', '')
        if description:
            cultural_text_parts.append(description)
            
        return " ".join(cultural_text_parts) if cultural_text_parts else ""

#        return total_score / count if count > 0 else 0.5

# Test function
def main():
    matcher = SimpleMatcher()
    results, jobs, candidates = matcher.find_matches()
    
    print("\n🎯 CHROMA VECTOR DATABASE MATCHING RESULTS:")
    for job_index, job_matches in results.items():
        job = jobs[job_index]
        print(f"\n🏢 {job['title']}")
        for match in job_matches[:3]:  # Show top 3
            candidate = match['candidate']
            breakdown = match.get('score_breakdown', {})
            print(f"   👤 {candidate['name']} - Score: {match['score']:.3f} ({match['match_grade']})")
            print(f"      Skills: {breakdown.get('skills', 0)}% | Exp: {breakdown.get('experience', 0)}% | Location: {breakdown.get('location', 0)}% | Semantic: {breakdown.get('semantic', 0)}%")

if __name__ == "__main__":
    main()
