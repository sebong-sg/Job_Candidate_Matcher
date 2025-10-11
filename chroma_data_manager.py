# 🗃️ CHROMA DATA MANAGER - Enhanced with Vector Database
# Combines traditional data management with Chroma vector DB

import json
import os
from vector_db import vector_db

class ChromaDataManager:
    def __init__(self, data_folder="data"):
        self.data_folder = data_folder
        print(f"✅ Chroma Data Manager initialized!")
        
        # Initialize vector database with existing data
        self._initialize_vector_db()
    
    def _initialize_vector_db(self):
        """Initialize Chroma DB with existing JSON data"""
        try:
            candidates = self._load_json_candidates()
            current_count = vector_db.get_candidate_count()
            
            # Only initialize if vector DB is empty but we have JSON data
            if current_count == 0 and candidates:
                print("🔄 Initializing vector database with existing candidates...")
                success = vector_db.add_candidates_batch(candidates)
                if success:
                    print(f"✅ Vector database initialized with {len(candidates)} candidates")
                else:
                    print("❌ Failed to initialize vector database")
            elif current_count > 0:
                print(f"✅ Vector database already has {current_count} candidates")
            else:
                print("ℹ️ No candidates found to initialize vector database")
                
        except Exception as e:
            print(f"⚠️ Vector database initialization warning: {e}")
    
    def _load_json_jobs(self):
        """Load jobs from JSON file (temporary during migration)"""
        try:
            file_path = os.path.join(self.data_folder, "jobs.json")
            with open(file_path, 'r') as file:
                data = json.load(file)
                print(f"📁 Loaded {len(data['jobs'])} jobs from JSON database")
                return data['jobs']
        except FileNotFoundError:
            print("❌ Jobs JSON file not found!")
            return []
        except Exception as e:
            print(f"❌ Error loading jobs from JSON: {e}")
            return []
    
    def _load_json_candidates(self):
        """Load candidates from JSON file (temporary during migration)"""
        try:
            file_path = os.path.join(self.data_folder, "candidates.json")
            with open(file_path, 'r') as file:
                data = json.load(file)
                print(f"📁 Loaded {len(data['candidates'])} candidates from JSON database")
                return data['candidates']
        except FileNotFoundError:
            print("❌ Candidates JSON file not found!")
            return []
        except Exception as e:
            print(f"❌ Error loading candidates from JSON: {e}")
            return []
    
    def load_jobs(self):
        """Get all jobs (from JSON during transition)"""
        return self._load_json_jobs()
    
    def load_candidates(self):
        """Get all candidates (from JSON during transition)"""
        return self._load_json_candidates()
    
    def add_job(self, job_data):
        """Add a new job to the database"""
        try:
            jobs = self.load_jobs()
            
            # Create new ID
            new_id = max([job['id'] for job in jobs]) + 1 if jobs else 1
            job_data['id'] = new_id
            
            # Add to list
            jobs.append(job_data)
            
            # Save back to JSON file
            file_path = os.path.join(self.data_folder, "jobs.json")
            with open(file_path, 'w') as file:
                json.dump({"jobs": jobs}, file, indent=2)
            
            print(f"✅ Added new job: {job_data['title']} (ID: {new_id})")
            return new_id
            
        except Exception as e:
            print(f"❌ Error adding job: {e}")
            return None
    
    def add_candidate(self, candidate_data):
        """Add a new candidate to both JSON and Chroma DB"""
        try:
            candidates = self.load_candidates()
            
            # Create new ID
            new_id = max([candidate['id'] for candidate in candidates]) + 1 if candidates else 1
            candidate_data['id'] = new_id
            
            # Add to JSON database
            candidates.append(candidate_data)
            file_path = os.path.join(self.data_folder, "candidates.json")
            with open(file_path, 'w') as file:
                json.dump({"candidates": candidates}, file, indent=2)
            
            # Add to Chroma vector database
            vector_db.add_candidate(candidate_data)
            
            print(f"✅ Added new candidate to both databases: {candidate_data['name']} (ID: {new_id})")
            return new_id
            
        except Exception as e:
            print(f"❌ Error adding candidate: {e}")
            return None
    
    def get_vector_db_stats(self):
        """Get statistics about the vector database"""
        return {
            'candidates_in_vector_db': vector_db.get_candidate_count(),
            'candidates_in_json': len(self.load_candidates()),
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
    
    print(f"📝 Sample Job: {jobs[0]['title'] if jobs else 'None'}")
    print(f"👤 Sample Candidate: {candidates[0]['name'] if candidates else 'None'}")