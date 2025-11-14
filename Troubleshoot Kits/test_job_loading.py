import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chroma_data_manager import ChromaDataManager

def test_job_loading():
    print("🔍 TESTING JOB LOADING FUNCTION")
    print("=" * 50)
    
    db = ChromaDataManager()
    
    try:
        jobs = db.load_jobs()
        print(f"✅ Successfully loaded {len(jobs)} jobs")
        for job in jobs[:3]:  # Show first 3
            print(f"  - {job.get('title')} at {job.get('company')}")
    except Exception as e:
        print(f"❌ Error loading jobs: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_job_loading()
