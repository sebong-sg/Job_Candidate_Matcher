import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def debug_load_jobs():
    print("🔍 DEBUGGING load_jobs() METHOD STEP-BY-STEP")
    print("=" * 50)
    
    from chroma_data_manager import ChromaDataManager
    from vector_db import vector_db
    
    db = ChromaDataManager()
    
    try:
        print("1. Testing vector_db.get_all_jobs() directly...")
        vector_jobs = vector_db.get_all_jobs()
        print(f"   vector_db.get_all_jobs() returned: {len(vector_jobs)} items")
        
        # Check each job from vector_db
        none_count = 0
        for i, job_data in enumerate(vector_jobs):
            if job_data is None:
                none_count += 1
                print(f"   🚨 FOUND None at index {i}")
            else:
                print(f"   Job {i}: {job_data.get('title', 'No title')} at {job_data.get('company', 'No company')}")
        
        print(f"\n📊 Summary: {none_count} None values out of {len(vector_jobs)} total jobs")
        
        if none_count > 0:
            print(f"\n🚨 PROBLEM: {none_count} jobs are None in vector database")
            print("This is causing the 'NoneType' object has no attribute 'get' error")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_load_jobs()
