# 🗃️ CHROMA VECTOR DATABASE MANAGER - ENHANCED WITH GROWTH DATA & JOB REQUIREMENTS
# Fixed metadata serialization issue with enhanced job data integration

import chromadb
import os
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import json

class ChromaVectorDB:
    def __init__(self, persist_directory="./chroma_db"):
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Initialize embedding model
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Chroma Vector DB initialized with embedding model!")
        except Exception as e:
            print(f"❌ Failed to load embedding model: {e}")
            self.embedding_model = None
        
        # Create collections
        self.candidates_collection = self.client.get_or_create_collection(
            name="candidates",
            metadata={"description": "Candidate profiles for semantic search"}
        )
        self.jobs_collection = self.client.get_or_create_collection(
            name="jobs", 
            metadata={"description": "Job descriptions for semantic search"}
        )
        
        print("✅ Chroma collections ready for enhanced data!")
    
    def get_candidate_count(self) -> int:
        """Get number of candidates in the vector database"""
        try:
            count = self.candidates_collection.count()
            return count
        except:
            return 0
    
    def add_candidate(self, candidate: Dict) -> bool:
        """Add a single candidate to the vector database - WITH GROWTH DATA"""
        if not self.embedding_model:
            print("❌ Embedding model not available")
            return False
            
        try:
            # Generate embedding from candidate profile and skills
            text_to_embed = f"{candidate.get('profile', '')} {' '.join(candidate.get('skills', []))}"
            if not text_to_embed.strip():
                return False
                
            embedding = self.embedding_model.encode(text_to_embed).tolist()
            
            # ENHANCED: Include growth data in metadata
            self.candidates_collection.add(
                ids=[str(candidate['id'])],
                embeddings=[embedding],
                documents=[text_to_embed],
                metadatas=[{
                    'name': candidate.get('name', 'Unknown'),
                    'skills': json.dumps(candidate.get('skills', [])),
                    'experience_years': candidate.get('experience_years', 0),
                    'location': candidate.get('location', ''),
                    'email': candidate.get('email', ''),
                    'phone': candidate.get('phone', ''),
                    'profile': candidate.get('profile', ''),
                    'education': candidate.get('education', ''),
                    'cultural_attributes': json.dumps(candidate.get('cultural_attributes', {})),
                    # ENHANCED: Growth data fields
                    'work_experience': json.dumps(candidate.get('work_experience', [])),
                    'career_metrics': json.dumps(candidate.get('career_metrics', {})),
                    'skill_timeline': json.dumps(candidate.get('skill_timeline', [])),
                    'growth_metrics': json.dumps(candidate.get('growth_metrics', {})),
                    'learning_velocity': candidate.get('learning_velocity', 0.0),
                    # CRITICAL: Store original resume text
                    'original_resume_text': candidate.get('original_resume_text', '')
                }]
            )
            print(f"✅ Candidate added to vector DB with growth data: {candidate.get('name', 'Unknown')}")
            return True
        except Exception as e:
            print(f"❌ Error adding candidate to vector DB: {e}")
            return False
    
    def add_candidates_batch(self, candidates: List[Dict]) -> bool:
        """Add multiple candidates to the vector database - WITH GROWTH DATA"""
        if not self.embedding_model:
            return False
            
        try:
            ids = []
            embeddings = []
            documents = []
            metadatas = []
            
            for candidate in candidates:
                text_to_embed = f"{candidate.get('profile', '')} {' '.join(candidate.get('skills', []))}"
                if text_to_embed.strip():
                    embedding = self.embedding_model.encode(text_to_embed).tolist()
                    
                    ids.append(str(candidate['id']))
                    embeddings.append(embedding)
                    documents.append(text_to_embed)
                    # ENHANCED: Include growth data in metadata
                    metadatas.append({
                        'name': candidate.get('name', 'Unknown'),
                        'skills': json.dumps(candidate.get('skills', [])),
                        'experience_years': candidate.get('experience_years', 0),
                        'location': candidate.get('location', ''),
                        'email': candidate.get('email', ''),
                        'phone': candidate.get('phone', ''),
                        'profile': candidate.get('profile', ''),
                        'education': candidate.get('education', ''),
                        'cultural_attributes': json.dumps(candidate.get('cultural_attributes', {})),
                        # ENHANCED: Growth data fields
                        'work_experience': json.dumps(candidate.get('work_experience', [])),
                        'career_metrics': json.dumps(candidate.get('career_metrics', {})),
                        'skill_timeline': json.dumps(candidate.get('skill_timeline', [])),
                        'growth_metrics': json.dumps(candidate.get('growth_metrics', {})),
                        'learning_velocity': candidate.get('learning_velocity', 0.0),
                        # CRITICAL: Store original resume text
                        'original_resume_text': candidate.get('original_resume_text', '')
                    })
            
            if ids:
                self.candidates_collection.add(
                    ids=ids,
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=metadatas
                )
                print(f"✅ Added {len(ids)} candidates to vector database with growth data")
                return True
            return False
        except Exception as e:
            print(f"❌ Error adding candidates batch: {e}")
            return False
    
    def add_job(self, job: Dict) -> bool:
        """Add a single job to the vector database - ENHANCED WITH JOB REQUIREMENTS"""
        if not self.embedding_model:
            print("❌ Embedding model not available")
            return False
            
        try:
            # Generate embedding from job description and skills
            text_to_embed = f"{job.get('description', '')} {' '.join(job.get('required_skills', []))}"
            if not text_to_embed.strip():
                return False
                
            embedding = self.embedding_model.encode(text_to_embed).tolist()
            
            # ENHANCED: Include job requirements data in metadata
            self.jobs_collection.add(
                ids=[str(job['id'])],
                embeddings=[embedding],
                documents=[text_to_embed],
                metadatas=[{
                    # Existing fields
                    'title': job.get('title', 'Unknown'),
                    'company': job.get('company', ''),
                    'location': job.get('location', ''),
                    'description': job.get('description', ''),
                    'required_skills': json.dumps(job.get('required_skills', [])),
                    'preferred_skills': json.dumps(job.get('preferred_skills', [])),
                    'experience_required': job.get('experience_required', 0),
                    'salary_range': job.get('salary_range', ''),
                    'job_type': job.get('job_type', ''),
                    'cultural_attributes': json.dumps(job.get('cultural_attributes', {})),
                    # NEW: Enhanced job dimensions
                    'growth_requirements': json.dumps(job.get('growth_requirements', {})),
                    'skill_requirements': json.dumps(job.get('skill_requirements', {})),
                    'career_progression': json.dumps(job.get('career_progression', {})),
                    'quality_assessment': json.dumps(job.get('quality_assessment', {})),
                    'confidence_scores': json.dumps(job.get('confidence_scores', {})),
                    'original_job_text': job.get('original_job_text', ''),
                    # NEW: AI Job Profile - CRITICAL MISSING FIELD
                    'ai_job_profile': json.dumps(job.get('ai_job_profile', {}))
                }]
            )
            print(f"✅ Job added to vector DB with enhanced data: {job.get('title', 'Unknown')}")
            print(f"   AI Job Profile stored: {'ai_job_profile' in job and bool(job['ai_job_profile'])}")
            return True
        except Exception as e:
            print(f"❌ Error adding job to vector DB: {e}")
            return False

    def add_jobs_batch(self, jobs: List[Dict]) -> bool:
        """Add multiple jobs to the vector database - ENHANCED"""
        if not self.embedding_model:
            return False
            
        try:
            ids = []
            embeddings = []
            documents = []
            metadatas = []
            
            for job in jobs:
                text_to_embed = f"{job.get('description', '')} {' '.join(job.get('required_skills', []))}"
                if text_to_embed.strip():
                    embedding = self.embedding_model.encode(text_to_embed).tolist()
                    
                    ids.append(str(job['id']))
                    embeddings.append(embedding)
                    documents.append(text_to_embed)
                    metadatas.append({
                        # Existing fields
                        'title': job.get('title', 'Unknown'),
                        'company': job.get('company', ''),
                        'location': job.get('location', ''),
                        'description': job.get('description', ''),
                        'required_skills': json.dumps(job.get('required_skills', [])),
                        'preferred_skills': json.dumps(job.get('preferred_skills', [])),
                        'experience_required': job.get('experience_required', 0),
                        'salary_range': job.get('salary_range', ''),
                        'job_type': job.get('job_type', ''),
                        'cultural_attributes': json.dumps(job.get('cultural_attributes', {})),
                        # NEW: Enhanced job dimensions
                        'growth_requirements': json.dumps(job.get('growth_requirements', {})),
                        'skill_requirements': json.dumps(job.get('skill_requirements', {})),
                        'career_progression': json.dumps(job.get('career_progression', {})),
                        'quality_assessment': json.dumps(job.get('quality_assessment', {})),
                        'confidence_scores': json.dumps(job.get('confidence_scores', {})),
                        'original_job_text': job.get('original_job_text', ''),
                        # NEW: AI Job Profile - CRITICAL MISSING FIELD
                        'ai_job_profile': json.dumps(job.get('ai_job_profile', {}))
                    })
            
            if ids:
                self.jobs_collection.add(
                    ids=ids,
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=metadatas
                )
                print(f"✅ Added {len(ids)} jobs to vector database with enhanced data")
                return True
            return False
        except Exception as e:
            print(f"❌ Error adding jobs batch: {e}")
            return False

    def find_matches_for_job(self, job: Dict, top_k: int = 20) -> List[Dict]:
        """Find candidate matches for a job using semantic search - WITH GROWTH DATA"""
        if not self.embedding_model:
            return []
            
        try:
            # Generate embedding from job description and requirements
            text_to_embed = f"{job.get('description', '')} {' '.join(job.get('required_skills', []))}"
            if not text_to_embed.strip():
                return []
                
            query_embedding = self.embedding_model.encode(text_to_embed).tolist()
            
            # Semantic search in Chroma
            results = self.candidates_collection.query(
                query_embeddings=[query_embedding],
                n_results=min(top_k, self.get_candidate_count()),
                include=['metadatas', 'distances', 'documents']
            )
            
            matches = []
            if results['ids'] and len(results['ids'][0]) > 0:
                for i in range(len(results['ids'][0])):
                    metadata = results['metadatas'][0][i]
                    # ADD NULL CHECK HERE
                    if not metadata:
                        continue  # Skip this candidate if metadata is None

                    distance = results['distances'][0][i]
                    similarity_score = max(0, 1 - distance)  # Convert distance to similarity
                    
                    # Parse JSON strings back to original formats
                    candidate_skills = json.loads(metadata.get('skills', '[]'))
                    
                    # Calculate skill overlap (traditional matching)
                    job_skills = set([s.lower() for s in job.get('required_skills', [])])
                    candidate_skills_set = set([s.lower() for s in candidate_skills])
                    skill_overlap = len(job_skills.intersection(candidate_skills_set)) / len(job_skills) if job_skills else 0
                    
                    # ENHANCED: Include growth data in candidate profile
                    matches.append({
                        'candidate': {
                            'id': int(results['ids'][0][i]),
                            'name': metadata.get('name', 'Unknown'),
                            'skills': candidate_skills,
                            'experience_years': metadata.get('experience_years', 0),
                            'location': metadata.get('location', ''),
                            'email': metadata.get('email', ''),
                            'phone': metadata.get('phone', ''),
                            'profile': metadata.get('profile', ''),
                            'education': metadata.get('education', ''),
                            'cultural_attributes': json.loads(metadata.get('cultural_attributes', '{}')),
                            # ENHANCED: Growth data fields
                            'work_experience': json.loads(metadata.get('work_experience', '[]')),
                            'career_metrics': json.loads(metadata.get('career_metrics', '{}')),
                            'skill_timeline': json.loads(metadata.get('skill_timeline', '[]')),
                            'growth_metrics': json.loads(metadata.get('growth_metrics', '{}')),
                            'learning_velocity': metadata.get('learning_velocity', 0.0)
                        },
                        'score': similarity_score,
                        'common_skills': list(job_skills.intersection(candidate_skills_set)),
                        'score_breakdown': {
                            'semantic': int(similarity_score * 100),
                            'skills': int(skill_overlap * 100),
                            'experience': 0,  # Will be calculated by matcher
                            'location': 0     # Will be calculated by matcher
                        }
                    })
            
            return matches
        except Exception as e:
            print(f"❌ Error in semantic search: {e}")
            return []

    def clear_candidates(self):
        """Clear all candidates from the vector database (for testing)"""
        try:
            self.client.delete_collection("candidates")
            self.candidates_collection = self.client.get_or_create_collection(
                name="candidates",
                metadata={"description": "Candidate profiles for semantic search"}
            )
            print("✅ Vector database cleared!")
            return True
        except Exception as e:
            print(f"❌ Error clearing vector database: {e}")
            return False

    def get_all_candidates(self) -> List[Dict]:
        """Retrieve all candidates from Chroma DB in original format - WITH GROWTH DATA"""
        try:
            # Get all candidates from collection
            results = self.candidates_collection.get(
                include=['metadatas', 'documents']
            )
            
            candidates = []
            for i in range(len(results['ids'])):
                metadata = results['metadatas'][i]
                # ENHANCED: Include growth data in candidate profile
                candidates.append({
                    'id': int(results['ids'][i]),
                    'name': metadata.get('name', 'Unknown'),
                    'email': metadata.get('email', ''),
                    'phone': metadata.get('phone', ''),
                    'location': metadata.get('location', ''),
                    'experience_years': metadata.get('experience_years', 0),
                    'skills': json.loads(metadata.get('skills', '[]')),
                    'profile': metadata.get('profile', ''),
                    'education': metadata.get('education', ''),
                    'cultural_attributes': json.loads(metadata.get('cultural_attributes', '{}')),
                    # ENHANCED: Growth data fields
                    'work_experience': json.loads(metadata.get('work_experience', '[]')),
                    'career_metrics': json.loads(metadata.get('career_metrics', '{}')),
                    'skill_timeline': json.loads(metadata.get('skill_timeline', '[]')),
                    'growth_metrics': json.loads(metadata.get('growth_metrics', '{}')),
                    'learning_velocity': metadata.get('learning_velocity', 0.0),
                    # CRITICAL: Include original resume text
                    'original_resume_text': metadata.get('original_resume_text', '')
                })
            
            print(f"✅ Retrieved {len(candidates)} candidates from Chroma DB with growth data")
            return candidates
        except Exception as e:
            print(f"❌ Error retrieving candidates from Chroma DB: {e}")
            return []

    def get_all_jobs(self) -> List[Dict]:
        """Retrieve all jobs from Chroma DB in original format - ENHANCED"""
        try:
            # Get all jobs from collection
            results = self.jobs_collection.get(
                include=['metadatas', 'documents']
            )
            
            jobs = []
            for i in range(len(results['ids'])):
                metadata = results['metadatas'][i]
                jobs.append({
                    'id': int(results['ids'][i]),
                    # Existing fields
                    'title': metadata.get('title', 'Unknown'),
                    'company': metadata.get('company', ''),
                    'location': metadata.get('location', ''),
                    'description': metadata.get('description', ''),
                    'required_skills': json.loads(metadata.get('required_skills', '[]')),
                    'preferred_skills': json.loads(metadata.get('preferred_skills', '[]')),
                    'experience_required': metadata.get('experience_required', 0),
                    'salary_range': metadata.get('salary_range', ''),
                    'job_type': metadata.get('job_type', ''),
                    'cultural_attributes': json.loads(metadata.get('cultural_attributes', '{}')),
                    # NEW: Enhanced job dimensions
                    'growth_requirements': json.loads(metadata.get('growth_requirements', '{}')),
                    'skill_requirements': json.loads(metadata.get('skill_requirements', '{}')),
                    'career_progression': json.loads(metadata.get('career_progression', '{}')),
                    'quality_assessment': json.loads(metadata.get('quality_assessment', '{}')),
                    'confidence_scores': json.loads(metadata.get('confidence_scores', '{}')),
                    'original_job_text': metadata.get('original_job_text', ''),
                    # NEW: AI Job Profile - CRITICAL MISSING FIELD
                    'ai_job_profile': json.loads(metadata.get('ai_job_profile', '{}'))
                })
            
            print(f"✅ Retrieved {len(jobs)} jobs from Chroma DB with enhanced data")
            return jobs
        except Exception as e:
            print(f"❌ Error retrieving jobs from Chroma DB: {e}")
            return []

# Global instance
vector_db = ChromaVectorDB()

# Test function
if __name__ == "__main__":
    print("🧪 Testing Enhanced Chroma Vector DB...")
    print(f"Current candidate count: {vector_db.get_candidate_count()}")
    
    # Test enhanced job storage
    test_job = {
        'id': 999,
        'title': 'Test Senior Developer',
        'company': 'TestCorp',
        'location': 'Remote',
        'description': 'Senior developer with 5+ years experience',
        'required_skills': ['python', 'django'],
        'preferred_skills': ['aws', 'docker'],
        'experience_required': 5,
        'job_type': 'Full-time',
        'cultural_attributes': {},
        'growth_requirements': {
            'target_career_stage': 'executive',
            'role_archetype': 'technical_specialist',
            'scope_level_required': 2
        },
        'quality_assessment': {
            'quality_level': 'high',
            'quality_score': 0.85
        },
        'ai_job_profile': {
            'role_overview': 'Test AI profile content',
            'ideal_candidate': 'Test ideal candidate',
            'success_factors': 'Test success factors',
            'growth_potential': 'Test growth potential',
            'cultural_fit': 'Test cultural fit',
            'recruiting_insights': 'Test recruiting insights'
        }
    }
    
    success = vector_db.add_job(test_job)
    print(f"Test job added: {success}")