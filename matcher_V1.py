# 🚀 ENHANCED JOB MATCHING PROGRAM WITH SCORE BREAKDOWN
# This is the brain of our application

from database import DataManager
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("=== 🤖 JOB-CANDIDATE MATCHER STARTING ===")

class SimpleMatcher:
    def __init__(self):
        self.db = DataManager()
        print("✅ Matcher initialized with database!")
    
    def calculate_skill_score(self, job_skills, candidate_skills):
        """Calculate weighted skill match score"""
        if not job_skills:
            return 0.0
        
        # Skill weights for more realistic scoring
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
        
        return matched_weight / total_weight if total_weight > 0 else 0.0
    
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
    
    def calculate_profile_relevance(self, job_description, candidate_profile):
        """Calculate profile relevance using improved keyword matching"""
        if not candidate_profile or not job_description:
            return 0.7  # Reasonable default
        
        job_lower = job_description.lower()
        candidate_lower = candidate_profile.lower()
        
        # Count meaningful keyword matches
        important_keywords = [
            'python', 'django', 'developer', 'development', 'web', 
            'applications', 'senior', 'experience', 'cloud', 'technical',
            'projects', 'lead', 'build', 'create', 'design'
        ]
        
        matches = 0
        for keyword in important_keywords:
            if keyword in job_lower and keyword in candidate_lower:
                matches += 1
        
        # Reasonable scoring logic
        if matches >= 5:
            return 0.85  # Excellent match
        elif matches >= 3:
            return 0.70  # Good match
        elif matches >= 1:
            return 0.50  # Basic match
        else:
            return 0.30  # Poor match
    
    def get_match_grade(self, total_score):
        """Convert numerical score to letter grade"""
        if total_score >= 0.9: return 'A+'
        elif total_score >= 0.8: return 'A'
        elif total_score >= 0.7: return 'B+'
        elif total_score >= 0.6: return 'B'
        elif total_score >= 0.5: return 'C+'
        elif total_score >= 0.4: return 'C'
        else: return 'D'
    
    def prepare_text_for_matching(self, jobs, candidates):
        """Prepare text data for semantic matching"""
        job_texts = []
        candidate_texts = []
        
        for job in jobs:
            job_text = f"{job['title']} {job['description']} {' '.join(job['required_skills'])}"
            job_texts.append(job_text)
        
        for candidate in candidates:
            candidate_text = f"{candidate['name']} {candidate['profile']} {' '.join(candidate['skills'])}"
            candidate_texts.append(candidate_text)
        
        return job_texts, candidate_texts
    
    def find_matches(self, jobs=None, candidates=None):
        """Enhanced matching with score breakdown"""
        if jobs is None:
            jobs = self.db.load_jobs()
        if candidates is None:
            candidates = self.db.load_candidates()
        
        print(f"🔍 Matching {len(jobs)} jobs with {len(candidates)} candidates...")
        
        # Prepare text for semantic matching
        job_texts, candidate_texts = self.prepare_text_for_matching(jobs, candidates)
        
        # Use TF-IDF for semantic matching
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        all_texts = job_texts + candidate_texts
        vectorizer.fit(all_texts)
        job_vectors = vectorizer.transform(job_texts)
        candidate_vectors = vectorizer.transform(candidate_texts)
        similarity_matrix = cosine_similarity(job_vectors, candidate_vectors)
        
        matches = {}
        
        for job_index, job in enumerate(jobs):
            print(f"\n📋 Processing: {job['title']}")
            matches[job_index] = []
            
            for candidate_index, candidate in enumerate(candidates):
                semantic_score = similarity_matrix[job_index, candidate_index]
                
                if semantic_score > 0.1:
                    # Calculate individual score components
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
                    
                    profile_score = self.calculate_profile_relevance(
                        job.get('description', ''), 
                        candidate.get('profile', '')
                    )
                    
                    # Calculate total weighted score
                    total_score = (
                        skill_score * 0.50 +
                        experience_score * 0.25 +  
                        location_score * 0.15 +
                        profile_score * 0.10
                    )
                    
                    # Find common skills
                    job_skills_lower = [s.lower() for s in job.get('required_skills', [])]
                    candidate_skills_lower = [s.lower() for s in candidate.get('skills', [])]
                    common_skills = list(set(job_skills_lower) & set(candidate_skills_lower))
                    
                    matches[job_index].append({
                        'candidate_index': candidate_index,
                        'candidate': candidate,
                        'score': total_score,
                        'common_skills': common_skills,
                        'score_breakdown': {
                            'skills': int(skill_score * 100),
                            'experience': int(experience_score * 100),
                            'location': int(location_score * 100),
                            'profile': int(profile_score * 100)
                        },
                        'match_grade': self.get_match_grade(total_score)
                    })
            
            matches[job_index].sort(key=lambda x: x['score'], reverse=True)
        
        return matches, jobs, candidates

# Keep your existing main function for testing
def main():
    matcher = SimpleMatcher()
    results, jobs, candidates = matcher.find_matches()
    
    print("\n🎯 ENHANCED MATCHING RESULTS:")
    for job_index, job_matches in results.items():
        job = jobs[job_index]
        print(f"\n🏢 {job['title']}")
        for match in job_matches[:3]:
            candidate = match['candidate']
            breakdown = match.get('score_breakdown', {})
            print(f"   👤 {candidate['name']} - Score: {match['score']:.3f}")
            print(f"      Skills: {breakdown.get('skills', 0)}% | Exp: {breakdown.get('experience', 0)}% | Location: {breakdown.get('location', 0)}% | Profile: {breakdown.get('profile', 0)}%")

if __name__ == "__main__":
    main()