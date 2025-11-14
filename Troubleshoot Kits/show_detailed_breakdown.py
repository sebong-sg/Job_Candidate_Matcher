import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from matcher import SimpleMatcher
from chroma_data_manager import ChromaDataManager

def show_detailed_breakdown():
    print("📊 DETAILED SCORE BREAKDOWN FOR ALL MATCHES")
    print("=" * 100)
    
    matcher = SimpleMatcher()
    db = ChromaDataManager()
    
    jobs = db.load_jobs()
    candidates = db.load_candidates()
    
    # Get all matches with detailed breakdown
    results, jobs_list, candidates_list = matcher.find_matches()
    
    for job_index, job_matches in results.items():
        if job_index < len(jobs):
            job = jobs[job_index]
            print(f"\n💼 {job['title']} at {job['company']}")
            print(f"   Skills: {', '.join(job.get('required_skills', []))}")
            print("-" * 100)
            
            # Show detailed breakdown for each candidate match
            for match in job_matches:
                candidate = match['candidate']
                breakdown = match.get('score_breakdown', {})
                
                print(f"👤 {candidate['name']:<15} | "
                      f"Total: {match['score']:>5.1%} | "
                      f"Skills: {breakdown.get('skills', 0):>3}% | "
                      f"Exp: {breakdown.get('experience', 0):>3}% | "
                      f"Location: {breakdown.get('location', 0):>3}% | "
                      f"Semantic: {breakdown.get('semantic', 0):>3}% | "
                      f"Cultural: {breakdown.get('cultural_fit', 0):>3}% | "
                      f"Common: {', '.join(match.get('common_skills', []))}")

if __name__ == "__main__":
    show_detailed_breakdown()
