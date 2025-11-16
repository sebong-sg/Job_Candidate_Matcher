# 🗃️ CHROMA DATA MANAGER - Enhanced with Growth Data
# Complete removal of JSON dependencies with growth data integration

from vector_db import vector_db

class ChromaDataManager:
    def __init__(self):
        print(f"✅ Chroma Data Manager initialized with growth data support!")
    
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
        """Get all candidates from Chroma DB - NOW WITH GROWTH DATA"""
        try:
            candidates = vector_db.get_all_candidates()
            print(f"📁 Loaded {len(candidates)} candidates from Chroma DB with growth data")
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
                'cultural_attributes': job_data.get('cultural_attributes', {})
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
        """Add a new candidate to Chroma DB - ENHANCED WITH GROWTH DATA"""
        try:
            # Get next ID
            existing_candidates = vector_db.get_all_candidates()
            new_id = max([c['id'] for c in existing_candidates]) + 1 if existing_candidates else 1
            candidate_data['id'] = new_id

            # Ensure cultural_attributes are included
            if not candidate_data.get('cultural_attributes'):
                candidate_data['cultural_attributes'] = {}  # Only set if truly missing/empty

                   
            # ENHANCED: Ensure all required fields are included with growth data
            self._ensure_candidate_data_integrity(candidate_data)
            
            # Add to Chroma DB
            success = vector_db.add_candidate(candidate_data)
            if success:
                print(f"✅ Added new candidate to Chroma DB with growth data: {candidate_data['name']} (ID: {new_id})")
                return new_id
            else:
                return None
        except Exception as e:
            print(f"❌ Error adding candidate: {e}")
            return None
    
    def _ensure_candidate_data_integrity(self, candidate_data):
        """Ensure all required fields are present, including growth data"""
        # Core required fields
        if not candidate_data.get('cultural_attributes'):
            candidate_data['cultural_attributes'] = {}
        
        # ENHANCED: Ensure growth data fields exist with defaults
        growth_fields = {
            'work_experience': [],
            'career_metrics': {},
            'skill_timeline': [],
            'growth_metrics': {},
            'learning_velocity': 0.0
        }
        
        for field, default_value in growth_fields.items():
            if field not in candidate_data:
                print(f"   ⚠️  Field missing: {field} - setting default")                
                candidate_data[field] = default_value
            else:
                print(f"   ✅ Field exists: {field} = {candidate_data[field]}")

        print(f"🔍 DEBUG: Final growth_metrics: {candidate_data.get('growth_metrics')}")        
    
    def add_candidates_batch(self, candidates_data):
        """Add multiple candidates to Chroma DB - ENHANCED WITH GROWTH DATA"""
        try:
            candidate_ids = []
            
            for candidate_data in candidates_data:
                # ENHANCED: Ensure growth data integrity
                self._ensure_candidate_data_integrity(candidate_data)
                
                candidate_id = self.add_candidate(candidate_data)
                if candidate_id:
                    candidate_ids.append(candidate_id)
            
            print(f"✅ Added {len(candidate_ids)} candidates to Chroma DB with growth data")
            return candidate_ids
            
        except Exception as e:
            print(f"❌ Error adding candidates batch: {e}")
            return []
    
    def get_candidate_with_growth_data(self, candidate_id):
        """Get a specific candidate with full growth data"""
        try:
            candidates = self.load_candidates()
            for candidate in candidates:
                if candidate['id'] == candidate_id:
                    # ENHANCED: Verify growth data is present
                    self._ensure_candidate_data_integrity(candidate)
                    return candidate
            return None
        except Exception as e:
            print(f"❌ Error getting candidate with growth data: {e}")
            return None
    
    def get_candidates_by_growth_potential(self, min_score=0):
        """Get candidates filtered by growth potential score"""
        try:
            candidates = self.load_candidates()
            filtered_candidates = []
            
            for candidate in candidates:
                growth_metrics = candidate.get('growth_metrics', {})
                growth_score = growth_metrics.get('growth_potential_score', 0)
                
                if growth_score >= min_score:
                    filtered_candidates.append(candidate)
            
            print(f"✅ Found {len(filtered_candidates)} candidates with growth potential >= {min_score}")
            return filtered_candidates
        except Exception as e:
            print(f"❌ Error filtering by growth potential: {e}")
            return []
    
    def get_vector_db_stats(self):
        """Get statistics about the vector database - ENHANCED WITH GROWTH METRICS"""
        try:
            candidates = self.load_candidates()
            
            # Calculate growth metrics statistics
            growth_scores = [c.get('growth_metrics', {}).get('growth_potential_score', 0) for c in candidates]
            avg_growth_score = sum(growth_scores) / len(growth_scores) if growth_scores else 0
            high_growth_candidates = len([score for score in growth_scores if score >= 70])
            
            return {
                'candidates_in_vector_db': vector_db.get_candidate_count(),
                'jobs_count': len(self.load_jobs()),
                'average_growth_potential': round(avg_growth_score, 1),
                'high_growth_candidates': high_growth_candidates,
                'candidates_with_career_data': len([c for c in candidates if c.get('work_experience')])
            }
        except Exception as e:
            print(f"❌ Error getting enhanced stats: {e}")
            return {
                'candidates_in_vector_db': vector_db.get_candidate_count(),
                'jobs_count': len(self.load_jobs()),
                'average_growth_potential': 0,
                'high_growth_candidates': 0,
                'candidates_with_career_data': 0
            }
# Test function
if __name__ == "__main__":
    print("🧪 Testing Enhanced Chroma Data Manager...")
    db = ChromaDataManager()
    
    stats = db.get_vector_db_stats()
    print(f"📊 Enhanced Database Stats: {stats}")
    
    jobs = db.load_jobs()
    candidates = db.load_candidates()
    
    print(f"📝 Jobs: {len(jobs)}")
    print(f"👤 Candidates: {len(candidates)}")
    
    # Test growth data functionality
    if candidates:
        high_growth_candidates = db.get_candidates_by_growth_potential(min_score=70)
        print(f"🚀 High growth candidates (score >= 70): {len(high_growth_candidates)}")
        
        if high_growth_candidates:
            sample_candidate = high_growth_candidates[0]
            growth_score = sample_candidate.get('growth_metrics', {}).get('growth_potential_score', 0)
            print(f"📈 Sample high-growth candidate: {sample_candidate['name']} (Score: {growth_score})")  
