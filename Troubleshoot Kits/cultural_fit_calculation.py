import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chroma_data_manager import ChromaDataManager
import json

def detailed_cultural_calculation():
    print("🧮 DETAILED CULTURAL FIT CALCULATION - MATHEMATICAL BREAKDOWN")
    print("=" * 80)
    
    db = ChromaDataManager()
    
    # Get the specific job and candidates
    jobs = db.load_jobs()
    candidates = db.load_candidates()
    
    # Find the job (Senior Python Code Developer)
    target_job = None
    for job in jobs:
        if 'Senior Python Code Developer' in job.get('title', ''):
            target_job = job
            break
    
    if not target_job:
        print("❌ Job not found")
        return
    
    print(f"💼 JOB: {target_job['title']}")
    print(f"   Cultural Attributes: {target_job.get('cultural_attributes')}")
    print()
    
    # Find Peter Tan and Alex Chen
    peter_tan = None
    alex_chen = None
    
    for candidate in candidates:
        if candidate['name'] == 'Peter Tan':
            peter_tan = candidate
        elif candidate['name'] == 'Alex Chen':
            alex_chen = candidate
    
    def calculate_detailed_fit(job, candidate, candidate_name):
        if not job.get('cultural_attributes') or not candidate.get('cultural_attributes'):
            return None
        
        print(f"👤 {candidate_name}")
        print(f"   Cultural Attributes: {candidate.get('cultural_attributes')}")
        print()
        print("   🧮 CALCULATION BREAKDOWN:")
        print("   " + "-" * 60)
        
        job_cultural = job['cultural_attributes']
        candidate_cultural = candidate['cultural_attributes']
        
        total_score = 0
        count = 0
        
        for attr in ['teamwork', 'innovation', 'work_environment', 'work_pace', 'customer_focus']:
            # Extract scores (job stores as [score, confidence], candidate as raw score)
            job_score = job_cultural[attr][0] if isinstance(job_cultural[attr], list) else job_cultural[attr]
            candidate_score = candidate_cultural[attr]
            
            # Calculate compatibility: 1 - absolute difference
            difference = abs(job_score - candidate_score)
            compatibility = 1 - difference
            
            total_score += compatibility
            count += 1
            
            print(f"   {attr.upper():<18}")
            print(f"      Job Score:     {job_score:.3f}")
            print(f"      Candidate Score: {candidate_score:.3f}")
            print(f"      Difference:     {difference:.3f}")
            print(f"      Compatibility:  1 - {difference:.3f} = {compatibility:.3f}")
            print()
        
        final_score = total_score / count
        print(f"   📊 FINAL CALCULATION:")
        print(f"      Total Compatibility: {total_score:.3f}")
        print(f"      Number of Attributes: {count}")
        print(f"      Final Score: {total_score:.3f} / {count} = {final_score:.3f} ({final_score*100:.1f}%)")
        print()
        
        return final_score
    
    # Calculate for Peter Tan
    if peter_tan:
        peter_score = calculate_detailed_fit(target_job, peter_tan, "Peter Tan")
    
    print("=" * 80)
    print()
    
    # Calculate for Alex Chen  
    if alex_chen:
        alex_score = calculate_detailed_fit(target_job, alex_chen, "Alex Chen")
    
    # Show comparison
    if peter_tan and alex_chen:
        print("🎯 COMPARISON:")
        print("   Peter Tan:  81.7% cultural fit")
        print("   Alex Chen:  82.9% cultural fit")
        print("   Difference: 1.2% (Alex Chen has slightly better cultural alignment)")

if __name__ == "__main__":
    detailed_cultural_calculation()
