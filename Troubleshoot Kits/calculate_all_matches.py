import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from matcher import SimpleMatcher
from chroma_data_manager import ChromaDataManager

def calculate_all_matches():
    print("🎯 CALCULATING ALL CANDIDATE-JOB MATCHES")
    print("=" * 70)
    
    # Initialize matcher and database
    matcher = SimpleMatcher()
    db = ChromaDataManager()
    
    # Get all jobs and candidates
    jobs = db.load_jobs()
    candidates = db.load_candidates()
    
    print(f"📊 Found {len(jobs)} jobs and {len(candidates)} candidates")
    print()
    
    # Calculate matches for each job
    for job in jobs:
        print(f"💼 JOB: {job.get('title')} at {job.get('company')}")
        print(f"   Required Skills: {', '.join(job.get('required_skills', []))}")
        print(f"   Experience: {job.get('experience_required', 0)}+ years")
        print(f"   Location: {job.get('location', 'Not specified')}")
        print()
        
        # Calculate matches for this job
        job_matches = []
        for candidate in candidates:
            # Calculate individual scores
            skill_score = matcher._calculate_skill_match(job, candidate)
            experience_score = matcher._calculate_experience_match(job, candidate)
            location_score = matcher._calculate_location_match(job, candidate)
            semantic_score = matcher._calculate_semantic_match(job, candidate)
            cultural_fit = matcher._calculate_cultural_fit(job, candidate)
            
            # Calculate total weighted score
            total_score = (
                skill_score * 0.35 +           # 35%
                experience_score * 0.25 +      # 25% 
                location_score * 0.15 +        # 15%
                semantic_score * 0.20 +        # 20%
                cultural_fit * 0.05            # 5%
            )
            
            job_matches.append({
                'candidate': candidate,
                'total_score': total_score,
                'breakdown': {
                    'skills': skill_score,
                    'experience': experience_score,
                    'location': location_score,
                    'semantic': semantic_score,
                    'cultural_fit': cultural_fit
                }
            })
        
        # Sort by total score
        job_matches.sort(key=lambda x: x['total_score'], reverse=True)
        
        # Display top 3 matches
        print("   🏆 TOP MATCHES:")
        for i, match in enumerate(job_matches[:3]):
            candidate = match['candidate']
            breakdown = match['breakdown']
            
            print(f"      {i+1}. {candidate['name']}: {match['total_score']:.1%}")
            print(f"          Skills: {breakdown['skills']:.1%} | "
                  f"Experience: {breakdown['experience']:.1%} | "
                  f"Location: {breakdown['location']:.1%}")
            print(f"          Semantic: {breakdown['semantic']:.1%} | "
                  f"Cultural: {breakdown['cultural_fit']:.1%}")
            print(f"          Common Skills: {', '.join(set(job.get('required_skills', [])).intersection(candidate.get('skills', [])))}")
            print()
        
        print("-" * 70)
        print()

if __name__ == "__main__":
    calculate_all_matches()
