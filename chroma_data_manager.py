# 🗃️ CHROMA DATA MANAGER - Pure Chroma DB Version
# Complete removal of JSON dependencies

from vector_db import vector_db

class ChromaDataManager:
    def __init__(self):
        print(f"✅ Chroma Data Manager initialized!")
    
    def load_jobs(self):
        """Get all jobs from Chroma DB"""
        try:
            jobs = vector_db.get_all_jobs()
            print(f"📁 Loaded {len(jobs)} jobs from Chroma DB")
            return jobs
        except Exception as e:
            print(f"❌ Error loading jobs from Chroma DB: {e}")
            return []
    
    def load_candidates(self):
        """Get all candidates from Chroma DB"""
        try:
            candidates = vector_db.get_all_candidates()
            print(f"📁 Loaded {len(candidates)} candidates from Chroma DB")
            return candidates
        except Exception as e:
            print(f"❌ Error loading candidates from Chroma DB: {e}")
            return []
    
    def add_job(self, job_data):
        """Add a new job to Chroma DB with complete job structure"""
        try:
            # Get next ID from existing jobs
            existing_jobs = vector_db.get_all_jobs()
            new_id = max([j['id'] for j in existing_jobs]) + 1 if existing_jobs else 1
            
            # Create complete job object with defaults
            complete_job = {
                'id': new_id,
                'title': job_data.get('title', ''),
                'company': job_data.get('company', ''),
                'location': job_data.get('location', ''),
                'description': job_data.get('description', ''),
                'required_skills': job_data.get('required_skills', []),
                'preferred_skills': job_data.get('preferred_skills', []),
                'experience_required': job_data.get('experience_required', 0),
                'salary_range': job_data.get('salary_range', ''),
                'job_type': job_data.get('job_type', 'Full-time'),
                'cultural_attributes': job_data.get('cultural_attributes', {})  # ADD THIS LINE
            }
            
            # Add to Chroma DB
            success = vector_db.add_job(complete_job)
            if success:
                print(f"✅ Added new job to Chroma DB: {complete_job['title']} (ID: {new_id})")
                return new_id
            else:
                print("❌ Failed to add job to Chroma DB")
                return None
                
        except Exception as e:
            print(f"❌ Error adding job: {e}")
            return None
    
    def add_candidate(self, candidate_data):
        """Add a new candidate to Chroma DB"""
        try:
            # Get next ID
            existing_candidates = vector_db.get_all_candidates()
            new_id = max([c['id'] for c in existing_candidates]) + 1 if existing_candidates else 1
            candidate_data['id'] = new_id
                   
            # Ensure cultural_attributes are included
            if not candidate_data.get('cultural_attributes'):
                candidate_data['cultural_attributes'] = {}  # Only set if truly missing/empty
            
            # Buggy code below replace by above
#            if 'cultural_attributes' not in candidate_data:
#                candidate_data['cultural_attributes'] = {}  # ADD THIS LINE

            # Add to Chroma DB
            success = vector_db.add_candidate(candidate_data)
            if success:
                print(f"✅ Added new candidate to Chroma DB: {candidate_data['name']} (ID: {new_id})")
                return new_id
            else:
                return None
        except Exception as e:
            print(f"❌ Error adding candidate: {e}")
            return None
    
    def get_vector_db_stats(self):
        """Get statistics about the vector database"""
        return {
            'candidates_in_vector_db': vector_db.get_candidate_count(),
            'jobs_count': len(self.load_jobs())
        }

# Test function
if __name__ == "__main__":
    print("🧪 Testing Chroma Data Manager...")
    db = ChromaDataManager()
    
    stats = db.get_vector_db_stats()
    print(f"📊 Database Stats: {stats}")
    
    jobs = db.load_jobs()
    candidates = db.load_candidates()
    
    print(f"📝 Jobs: {len(jobs)}")
    print(f"👤 Candidates: {len(candidates)}")
