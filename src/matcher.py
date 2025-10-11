# 🚀 ENHANCED JOB MATCHING WITH CHROMA VECTOR DATABASE
# Hybrid approach: Chroma for semantic search + traditional scoring

from chroma_data_manager import ChromaDataManager
from vector_db import vector_db
from semantic_matcher import semantic_matcher
from profile_analyzer import profile_analyzer

print("=== 🤖 JOB-CANDIDATE MATCHER WITH CHROMA DB ===")

class SimpleMatcher:
    def __init__(self):
        self.db = ChromaDataManager()
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
    
    def calculate_location_score(self, job_location, candidate_location):
        """Calculate location compatibility score"""
        if not job_location or not candidate_location:
            return 0.5
            
        job_loc = job_location.lower()
        candidate_loc = candidate_location.lower()
        
        if 'remote' in job_loc:
            return 1.0
        elif job_loc == candidate_loc:
            return 1.0
        elif 'remote' in candidate_loc:
            return 0.8
        else:
            return 0.3
    
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
                
                # Calculate additional scoring components
                skill_score = self.calculate_skill_score(
                    job.get('required_skills', []), 
                    candidate.get('skills', [])
                )
                
                experience_score = self.calculate_experience_score(
                    job.get('title', ''), 
                    candidate.get('experience_years', 0)
                )
                
                location_score = self.calculate_location_score(
                    job.get('location', ''), 
                    candidate.get('location', '')
                )
                
                # Get semantic score from Chroma
                semantic_score = match['score']
                
                # Calculate total weighted score
                total_score = (
                    skill_score * 0.40 +           # Skill matching
                    experience_score * 0.25 +      # Experience rules
                    location_score * 0.15 +        # Location rules  
                    semantic_score * 0.20          # Semantic understanding from Chroma
                )
                
                # Update the match with complete scoring
                match['score'] = total_score
                match['score_breakdown'] = {
                    'skills': int(skill_score * 100),
                    'experience': int(experience_score * 100),
                    'location': int(location_score * 100),
                    'semantic': int(semantic_score * 100)
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