import sys
sys.path.append('.')
from chroma_data_manager import ChromaDataManager

db = ChromaDataManager()
jobs = db.load_jobs()

if jobs:
    job = jobs[0]
    print("Job data fields:")
    print(f"  title: {job.get('title')}")
    print(f"  description length: {len(job.get('description', ''))}")
    print(f"  original_job_text length: {len(job.get('original_job_text', ''))}")
    print(f"  original_job_text present: {'original_job_text' in job}")
    if 'original_job_text' in job:
        print(f"  First 200 chars: {job['original_job_text'][:200]}...")
else:
    print("No jobs found")
