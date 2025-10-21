# 🗃️ DATABASE MANAGER
# Handles loading and saving job and candidate data

import sqlite3
import json
import os

class Database:
    def __init__(self, db_path='job_matcher.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        self.create_scoring_tables()
    
    def create_tables(self):
        """Create main tables for jobs and candidates"""
        tables = [
            '''CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT,
                location TEXT,
                description TEXT,
                required_skills TEXT,
                preferred_skills TEXT,
                experience_required INTEGER,
                salary_range TEXT,
                job_type TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )''',
            '''CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                skills TEXT,
                experience INTEGER,
                education TEXT,
                location TEXT,
                resume_text TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )'''
        ]
        
        for table in tables:
            self.conn.execute(table)
        self.conn.commit()
        print("✅ Main database tables created")
    
    def create_scoring_tables(self):
        """Create tables for user-based scoring profiles"""
        tables = [
            '''CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )''',
            '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies(id)
            )''',
            '''CREATE TABLE IF NOT EXISTS scoring_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                profile_name TEXT NOT NULL,
                is_default BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )''',
            '''CREATE TABLE IF NOT EXISTS scoring_criteria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                weight DECIMAL(3,2) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (profile_id) REFERENCES scoring_profiles(id)
            )''',
            '''CREATE TABLE IF NOT EXISTS scoring_thresholds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                value DECIMAL(5,2) NOT NULL,
                FOREIGN KEY (profile_id) REFERENCES scoring_profiles(id)
            )''',
            '''CREATE TABLE IF NOT EXISTS scoring_mappings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                key TEXT NOT NULL,
                value INTEGER NOT NULL,
                FOREIGN KEY (profile_id) REFERENCES scoring_profiles(id)
            )''',
            '''CREATE TABLE IF NOT EXISTS job_level_keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                level TEXT NOT NULL,
                keywords TEXT NOT NULL,
                FOREIGN KEY (profile_id) REFERENCES scoring_profiles(id)
            )'''
        ]
        
        for table in tables:
            self.conn.execute(table)
        self.conn.commit()
        print("✅ Scoring database tables created")

# Temporary compatibility layer - will be removed later

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