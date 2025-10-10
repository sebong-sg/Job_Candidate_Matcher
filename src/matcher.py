# 🚀 MAIN JOB MATCHING PROGRAM - NOW WITH DATABASE!
# This is the brain of our application

from database import DataManager
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("=== 🤖 JOB-CANDIDATE MATCHER STARTING ===")

class SimpleMatcher:
    def __init__(self):
        self.db = DataManager()
        print("✅ Matcher initialized with database!")
    
    def prepare_text_for_matching(self, jobs, candidates):
        """Prepare text data for semantic matching"""
        job_texts = []
        candidate_texts = []
        
        for job in jobs:
            # Combine title, description, and skills for better matching
            job_text = f"{job['title']} {job['description']} {' '.join(job['required_skills'])}"
            job_texts.append(job_text)
        
        for candidate in candidates:
            # Combine name, profile, and skills for better matching  
            candidate_text = f"{candidate['name']} {candidate['profile']} {' '.join(candidate['skills'])}"
            candidate_texts.append(candidate_text)
        
        return job_texts, candidate_texts
    
    def find_matches(self, jobs=None, candidates=None):
        """Find the best candidates for each job using semantic matching"""
        
        # Load data from database if not provided
        if jobs is None:
            jobs = self.db.load_jobs()
        if candidates is None:
            candidates = self.db.load_candidates()
        
        print(f"🔍 Matching {len(jobs)} jobs with {len(candidates)} candidates...")
        
        # Prepare text for semantic matching
        job_texts, candidate_texts = self.prepare_text_for_matching(jobs, candidates)
        
        # Use TF-IDF and cosine similarity for semantic matching
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        
        # Combine all texts for consistent vocabulary
        all_texts = job_texts + candidate_texts
        vectorizer.fit(all_texts)
        
        # Transform job and candidate texts
        job_vectors = vectorizer.transform(job_texts)
        candidate_vectors = vectorizer.transform(candidate_texts)
        
        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(job_vectors, candidate_vectors)
        
        matches = {}
        
        for job_index, job in enumerate(jobs):
            print(f"\n📋 Processing: {job['title']}")
            matches[job_index] = []
            
            for candidate_index, candidate in enumerate(candidates):
                score = similarity_matrix[job_index, candidate_index]
                
                if score > 0.1:  # Only include meaningful matches
                    matches[job_index].append({
                        'candidate_index': candidate_index,
                        'candidate': candidate,
                        'score': score,
                        'common_skills': self.find_common_skills(job, candidate)
                    })
            
            # Sort by best matches
            matches[job_index].sort(key=lambda x: x['score'], reverse=True)
        
        return matches, jobs, candidates
    
    def find_common_skills(self, job, candidate):
        """Find common skills between job and candidate"""
        job_skills = set(skill.lower() for skill in job['required_skills'])
        candidate_skills = set(skill.lower() for skill in candidate['skills'])
        return list(job_skills.intersection(candidate_skills))

def main():
    """Main function that runs our program"""
    # Create our matcher (it automatically loads from database)
    matcher = SimpleMatcher()
    
    # Find matches using database data
    print("\n" + "="*60)
    results, jobs, candidates = matcher.find_matches()
    print("="*60)
    
    # Display results
    print("\n🎯 SEMANTIC MATCHING RESULTS:")
    print("="*60)
    
    for job_index, job_matches in results.items():
        job = jobs[job_index]
        print(f"\n🏢 JOB: {job['title']}")
        print(f"   Company: {job['company']} | Location: {job['location']}")
        print(f"   Description: {job['description'][:100]}...")
        print("   Top matches:")
        
        for match in job_matches[:3]:  # Show top 3 matches
            candidate = match['candidate']
            print(f"\n   👤 {candidate['name']} (Exp: {candidate['experience_years']} years)")
            print(f"      📊 Match Score: {match['score']:.3f}")
            print(f"      💬 Common skills: {', '.join(match['common_skills'])}")
            print(f"      📍 Location: {candidate['location']}")
    
    print("\n" + "="*60)
    print("✅ Semantic matching completed! Database is working perfectly.")

# This makes the program run when we execute the file
if __name__ == "__main__":
    main()