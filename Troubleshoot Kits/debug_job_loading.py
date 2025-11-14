import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chroma_data_manager import ChromaDataManager

def debug_job_loading():
    print("🔍 DEBUGGING JOB LOADING PIPELINE")
    print("=" * 50)
    
    db = ChromaDataManager()
    
    try:
        # Test get_all_jobs directly
        print("1. Testing get_all_jobs()...")
        all_jobs_data = db.get_all_jobs()
        print(f"   get_all_jobs returned: {len(all_jobs_data)} items")
        
        for i, job_data in enumerate(all_jobs_data[:5]):  # Check first 5
            print(f"   Job {i}: {type(job_data)} = {job_data}")
            if job_data is None:
                print(f"   ⚠️ FOUND NONE at index {i}")
        
        # Now test load_jobs with detailed debugging
        print("\n2. Testing load_jobs with detailed processing...")
        jobs_data = db.get_all_jobs()
        jobs = []
        
        for i, job_data in enumerate(jobs_data):
            print(f"   Processing job {i}: {job_data}")
            if job_data is None:
                print(f"   🚨 SKIPPING None value at index {i}")
                continue
                
            try:
                job = {
                    'id': job_data.get('id'),
                    'title': job_data.get('title', 'Unknown'),
                    'company': job_data.get('company', ''),
                    'location': job_data.get('location', ''),
                    'description': job_data.get('description', ''),
                    'required_skills': job_data.get('required_skills', []),
                    'experience_required': job_data.get('experience_required', 0),
                    'employment_type': job_data.get('job_type', ''),
                    'cultural_attributes': job_data.get('cultural_attributes', {})
                }
                jobs.append(job)
                print(f"   ✅ Successfully processed: {job['title']}")
            except Exception as e:
                print(f"   ❌ Failed to process job {i}: {e}")
        
        print(f"\n📊 Final result: {len(jobs)} jobs successfully loaded")
        return jobs
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_job_loading()
