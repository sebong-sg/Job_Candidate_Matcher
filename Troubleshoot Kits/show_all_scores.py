import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from matcher import SimpleMatcher
from chroma_data_manager import ChromaDataManager

def show_all_scores():
    print("📊 ALL CANDIDATE-JOB SCORES (COMPLETE MATRIX)")
    print("=" * 80)
    
    matcher = SimpleMatcher()
    db = ChromaDataManager()
    
    jobs = db.load_jobs()
    candidates = db.load_candidates()
    
    print(f"Jobs: {len(jobs)}, Candidates: {len(candidates)}")
    print()
    
    # Use the main matching method
    results, jobs_list, candidates_list = matcher.find_matches()
    
    # Header row with candidate names
    header = "JOB".ljust(40)
    for candidate in candidates:
        header += f" | {candidate['name'][:15]:<15}"
    print(header)
    print("-" * 80)
    
    # Display scores for each job from the results
    for job_index, job_matches in results.items():
        if job_index < len(jobs):
            job = jobs[job_index]
            job_title = f"{job['title'][:35]}...".ljust(40) if len(job['title']) > 35 else job['title'].ljust(40)
            row = job_title
            
            # Create lookup for this job's matches
            match_scores = {}
            for match in job_matches:
                match_scores[match['candidate']['name']] = match['score']
            
            # Display score for each candidate
            for candidate in candidates:
                score = match_scores.get(candidate['name'], 0)
                row += f" | {score:.1%}".ljust(15)
            
            print(row)
    
    print()
    print("🔍 CANDIDATES WITH CULTURAL ATTRIBUTES:")
    print("=" * 80)
    cultural_candidates = []
    for candidate in candidates:
        if candidate.get('cultural_attributes'):
            cultural_candidates.append(candidate)
    
    if cultural_candidates:
        for candidate in cultural_candidates:
            print(f"👤 {candidate['name']}: {candidate['cultural_attributes']}")
    else:
        print("No candidates with cultural attributes found")

if __name__ == "__main__":
    show_all_scores()
