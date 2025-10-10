# 🗃️ DATABASE MANAGER
# Handles loading and saving job and candidate data

import json
import os

class DataManager:
    def __init__(self, data_folder="data"):
        self.data_folder = data_folder
        print(f"✅ Database manager initialized. Data folder: {data_folder}")
    
    def load_jobs(self):
        """Load all jobs from JSON file"""
        try:
            file_path = os.path.join(self.data_folder, "jobs.json")
            with open(file_path, 'r') as file:
                data = json.load(file)
                print(f"📁 Loaded {len(data['jobs'])} jobs from database")
                return data['jobs']
        except FileNotFoundError:
            print("❌ Jobs database file not found!")
            return []
        except Exception as e:
            print(f"❌ Error loading jobs: {e}")
            return []
    
    def load_candidates(self):
        """Load all candidates from JSON file"""
        try:
            file_path = os.path.join(self.data_folder, "candidates.json")
            with open(file_path, 'r') as file:
                data = json.load(file)
                print(f"📁 Loaded {len(data['candidates'])} candidates from database")
                return data['candidates']
        except FileNotFoundError:
            print("❌ Candidates database file not found!")
            return []
        except Exception as e:
            print(f"❌ Error loading candidates: {e}")
            return []
    
    def add_job(self, job_data):
        """Add a new job to the database"""
        try:
            jobs = self.load_jobs()
            
            # Create new ID
            new_id = max([job['id'] for job in jobs]) + 1 if jobs else 1
            job_data['id'] = new_id
            
            # Add to list
            jobs.append(job_data)
            
            # Save back to file
            file_path = os.path.join(self.data_folder, "jobs.json")
            with open(file_path, 'w') as file:
                json.dump({"jobs": jobs}, file, indent=2)
            
            print(f"✅ Added new job: {job_data['title']} (ID: {new_id})")
            return new_id
            
        except Exception as e:
            print(f"❌ Error adding job: {e}")
            return None
    
    def add_candidate(self, candidate_data):
        """Add a new candidate to the database"""
        try:
            candidates = self.load_candidates()
            
            # Create new ID
            new_id = max([candidate['id'] for candidate in candidates]) + 1 if candidates else 1
            candidate_data['id'] = new_id
            
            # Add to list
            candidates.append(candidate_data)
            
            # Save back to file
            file_path = os.path.join(self.data_folder, "candidates.json")
            with open(file_path, 'w') as file:
                json.dump({"candidates": candidates}, file, indent=2)
            
            print(f"✅ Added new candidate: {candidate_data['name']} (ID: {new_id})")
            return new_id
            
        except Exception as e:
            print(f"❌ Error adding candidate: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Test the database manager
    db = DataManager()
    
    jobs = db.load_jobs()
    candidates = db.load_candidates()
    
    print(f"\n📊 Database Stats:")
    print(f"   Jobs: {len(jobs)}")
    print(f"   Candidates: {len(candidates)}")
    
    if jobs:
        print(f"\n📝 Sample Job: {jobs[0]['title']}")
        print(f"   Skills: {', '.join(jobs[0]['required_skills'])}")
    
    if candidates:
        print(f"\n👤 Sample Candidate: {candidates[0]['name']}")
        print(f"   Skills: {', '.join(candidates[0]['skills'])}")