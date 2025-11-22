# 🗃️ CHROMA DATA MANAGER - Enhanced with Growth Data & Job Requirements
# Fixed data integrity issue - preserves Groq AI extracted data

from vector_db import vector_db
import json

class ChromaDataManager:
    def __init__(self):
        print(f"✅ Enhanced Chroma Data Manager initialized with job requirements support!")
    
    def load_jobs(self):
        """Get all jobs from Chroma DB - NOW WITH ENHANCED DATA"""
        try:
            jobs = vector_db.get_all_jobs()
            print(f"📁 Loaded {len(jobs)} jobs from Chroma DB with enhanced data")
            
            # ENSURE backward compatibility - add missing fields if needed
            for job in jobs:
                self._ensure_job_data_backward_compatibility(job)
                
            return jobs
        except Exception as e:
            print(f"❌ Error loading jobs from Chroma DB: {e}")
            return []
    
    def load_candidates(self):
        """Get all candidates from Chroma DB - WITH GROWTH DATA"""
        try:
            candidates = vector_db.get_all_candidates()
            print(f"📁 Loaded {len(candidates)} candidates from Chroma DB with growth data")
            return candidates
        except Exception as e:
            print(f"❌ Error loading candidates from Chroma DB: {e}")
            return []
    
    def add_job(self, job_data):
        """Add a new job to Chroma DB with complete job structure - ENHANCED"""
        try:
            # Get next ID from existing jobs
            existing_jobs = vector_db.get_all_jobs()
            new_id = max([j['id'] for j in existing_jobs]) + 1 if existing_jobs else 1
            
            # ENSURE backward compatibility for existing job data
            self._ensure_job_data_backward_compatibility(job_data)
            
            # Create complete job object with enhanced data
            complete_job = {
                'id': new_id,
                # Existing fields (required for backward compatibility)
                'title': job_data.get('title', ''),
                'company': job_data.get('company', ''),
                'location': job_data.get('location', ''),
                'description': job_data.get('description', ''),
                'required_skills': job_data.get('required_skills', []),
                'preferred_skills': job_data.get('preferred_skills', []),
                'experience_required': job_data.get('experience_required', 0),
                'salary_range': job_data.get('salary_range', ''),
                'job_type': job_data.get('job_type', 'Full-time'),
                'cultural_attributes': job_data.get('cultural_attributes', {}),
                # NEW: Enhanced job dimensions
                'growth_requirements': job_data.get('growth_requirements', self._get_default_growth_requirements()),
                'skill_requirements': job_data.get('skill_requirements', self._get_default_skill_requirements()),
                'career_progression': job_data.get('career_progression', self._get_default_career_progression()),
                'quality_assessment': job_data.get('quality_assessment', self._get_default_quality_assessment()),
                'confidence_scores': job_data.get('confidence_scores', self._get_default_confidence_scores())
            }
            
            # Add to Chroma DB
            success = vector_db.add_job(complete_job)
            if success:
                print(f"✅ Added new job to Chroma DB with enhanced data: {complete_job['title']} (ID: {new_id})")
                print(f"   Quality Level: {complete_job['quality_assessment'].get('quality_level', 'unknown')}")
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

            # ENHANCED: Ensure all required fields are included WITHOUT overwriting existing data
            self._ensure_candidate_data_integrity(candidate_data)
            
            # Add to Chroma DB
            success = vector_db.add_candidate(candidate_data)
            if success:
                print(f"✅ Added new candidate to Chroma DB with growth data: {candidate_data['name']} (ID: {new_id})")
                
                # DEBUG: Verify work_experience is preserved
                work_exp_count = len(candidate_data.get('work_experience', []))
                if work_exp_count > 0:
                    print(f"   ✅ Preserved {work_exp_count} work experience entries")
                else:
                    print(f"   ⚠️  No work experience data found")
                    
                return new_id
            else:
                return None
        except Exception as e:
            print(f"❌ Error adding candidate: {e}")
            return None
    
    def _ensure_job_data_backward_compatibility(self, job_data):
        """Ensure job data has all required fields for backward compatibility"""
        # Required fields for existing code
        if 'required_skills' not in job_data:
            job_data['required_skills'] = []
        if 'preferred_skills' not in job_data:
            job_data['preferred_skills'] = []
        if 'cultural_attributes' not in job_data:
            job_data['cultural_attributes'] = {}
        if 'experience_required' not in job_data:
            job_data['experience_required'] = 0
        if 'job_type' not in job_data:
            job_data['job_type'] = 'Full-time'
            
        # NEW: Ensure enhanced fields exist with defaults
        enhanced_fields = {
            'growth_requirements': self._get_default_growth_requirements(),
            'skill_requirements': self._get_default_skill_requirements(),
            'career_progression': self._get_default_career_progression(),
            'quality_assessment': self._get_default_quality_assessment(),
            'confidence_scores': self._get_default_confidence_scores()
        }
        
        for field, default_value in enhanced_fields.items():
            if field not in job_data:
                job_data[field] = default_value
                print(f"   ⚠️  Job field missing: {field} - set to default")
    
    def _get_default_growth_requirements(self):
        """Default growth requirements for jobs without enhanced parsing"""
        return {
            'target_career_stage': 'mid_career',
            'role_archetype': 'technical_specialist',
            'scope_level_required': 1,
            'executive_potential_required': 0.3,
            'learning_expectations': 0.5,
            'confidence': 0.3,
            'has_clear_requirements': False
        }
    
    def _get_default_skill_requirements(self):
        """Default skill requirements for jobs without enhanced parsing"""
        return {
            'core_skills': [],
            'secondary_skills': [],
            'required_proficiency': {},
            'skill_priority_weights': {},
            'confidence': 0.3
        }
    
    def _get_default_career_progression(self):
        """Default career progression for jobs without enhanced parsing"""
        return {
            'promotion_expectations': 'standard',
            'strategic_mobility_preferred': 0.5,
            'impact_scale_required': 0.5,
            'confidence': 0.3
        }
    
    def _get_default_quality_assessment(self):
        """Default quality assessment for jobs without enhanced parsing"""
        return {
            'quality_score': 0.5,
            'quality_level': 'medium',
            'quality_issues': ['No quality assessment available'],
            'missing_required_fields': [],
            'missing_recommended_fields': [],
            'suggestions_for_improvement': ['Use enhanced job parser for better quality assessment']
        }
    
    def _get_default_confidence_scores(self):
        """Default confidence scores for jobs without enhanced parsing"""
        return {
            'title': 0.5,
            'company': 0.5,
            'location': 0.5,
            'experience': 0.5,
            'skills': 0.5,
            'employment_type': 0.5,
            'cultural_fit': 0.5,
            'overall_quality': 0.5,
            'enhanced_data': 0.1
        }
    
    def _ensure_candidate_data_integrity(self, candidate_data):
        """Ensure all required fields are present WITHOUT overwriting existing data"""
        # Core required fields
        if not candidate_data.get('cultural_attributes'):
            candidate_data['cultural_attributes'] = {}
        
        # FIXED: Only set defaults if field is COMPLETELY missing or None
        # Do NOT overwrite existing data with empty defaults
        required_fields = {
            'work_experience': [],
            'career_metrics': {},
            'skill_timeline': [],
            'growth_metrics': {},
            'learning_velocity': 0.0
        }
        
        for field, default_value in required_fields.items():
            if field not in candidate_data or candidate_data[field] is None:
                # Only show warning for critical fields, not optional growth fields
                if field == 'work_experience':
 #                  print(f"   ⚠️  Candidate field missing: {field} - setting default")                
                    print(f"   ⚠️  Candidate field missing: {field} - setting default")                
                candidate_data[field] = default_value
            # FIXED: Don't overwrite if field exists but is empty - Groq AI might have provided empty but valid data

        # DEBUG: Check if work_experience is preserved
        work_exp = candidate_data.get('work_experience', [])
        if work_exp and len(work_exp) > 0:
            print(f"   ✅ Preserving {len(work_exp)} work experience entries from Groq AI")
    
    def add_candidates_batch(self, candidates_data):
        """Add multiple candidates to Chroma DB - ENHANCED WITH GROWTH DATA"""
        try:
            candidate_ids = []
            
            for candidate_data in candidates_data:
                # ENHANCED: Ensure growth data integrity WITHOUT overwriting
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
    
    def get_jobs_by_quality(self, min_quality='medium'):
        """Get jobs filtered by quality level - NEW"""
        try:
            jobs = self.load_jobs()
            quality_levels = ['very_low', 'low', 'medium', 'high']
            min_quality_index = quality_levels.index(min_quality)
            
            filtered_jobs = []
            for job in jobs:
                quality_level = job.get('quality_assessment', {}).get('quality_level', 'medium')
                if quality_levels.index(quality_level) >= min_quality_index:
                    filtered_jobs.append(job)
            
            print(f"✅ Found {len(filtered_jobs)} jobs with quality >= {min_quality}")
            return filtered_jobs
        except Exception as e:
            print(f"❌ Error filtering jobs by quality: {e}")
            return []
    
    def get_vector_db_stats(self):
        """Get statistics about the vector database - ENHANCED WITH JOB METRICS"""
        try:
            jobs = self.load_jobs()
            candidates = self.load_candidates()
            
            # Calculate growth metrics statistics
            growth_scores = [c.get('growth_metrics', {}).get('growth_potential_score', 0) for c in candidates]
            avg_growth_score = sum(growth_scores) / len(growth_scores) if growth_scores else 0
            high_growth_candidates = len([score for score in growth_scores if score >= 70])
            
            # NEW: Count candidates with actual work experience data
            candidates_with_work_exp = len([c for c in candidates if c.get('work_experience') and len(c['work_experience']) > 0])
            
            # NEW: Job quality statistics
            quality_levels = [j.get('quality_assessment', {}).get('quality_level', 'medium') for j in jobs]
            quality_counts = {
                'high': quality_levels.count('high'),
                'medium': quality_levels.count('medium'),
                'low': quality_levels.count('low'),
                'very_low': quality_levels.count('very_low')
            }
            
            return {
                'candidates_in_vector_db': vector_db.get_candidate_count(),
                'jobs_count': len(jobs),
                'average_growth_potential': round(avg_growth_score, 1),
                'high_growth_candidates': high_growth_candidates,
                'candidates_with_career_data': candidates_with_work_exp,  # FIXED: Use actual work experience count
                # NEW: Job quality metrics
                'job_quality_breakdown': quality_counts,
                'high_quality_jobs': quality_counts['high'] + quality_counts['medium'],
                'needs_improvement_jobs': quality_counts['low'] + quality_counts['very_low']
            }
        except Exception as e:
            print(f"❌ Error getting enhanced stats: {e}")
            return {
                'candidates_in_vector_db': vector_db.get_candidate_count(),
                'jobs_count': len(self.load_jobs()),
                'average_growth_potential': 0,
                'high_growth_candidates': 0,
                'candidates_with_career_data': 0,
                'job_quality_breakdown': {'high': 0, 'medium': 0, 'low': 0, 'very_low': 0},
                'high_quality_jobs': 0,
                'needs_improvement_jobs': 0
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
    
    # Test new functionality
    high_quality_jobs = db.get_jobs_by_quality(min_quality='high')
    print(f"⭐ High quality jobs: {len(high_quality_jobs)}")
    
    if jobs:
        sample_job = jobs[0]
        print(f"🔍 Sample job quality: {sample_job.get('quality_assessment', {}).get('quality_level', 'unknown')}")
        print(f"🔍 Sample job growth reqs: {sample_job.get('growth_requirements', {}).get('target_career_stage', 'unknown')}")