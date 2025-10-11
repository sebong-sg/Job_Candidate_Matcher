# 🌐 SIMPLE WEB INTERFACE
# No HTML required - we use a simple library!

from database import DataManager
from matcher import SimpleMatcher
import json

class WebInterface:
    def __init__(self):
        self.db = DataManager()
        self.matcher = SimpleMatcher()
        print("✅ Web interface ready!")
    
    def show_dashboard(self):
        """Show a simple text-based dashboard"""
        print("\n" + "="*70)
        print("🎯 JOB MATCHER DASHBOARD")
        print("="*70)
        
        # Load data
        jobs = self.db.load_jobs()
        candidates = self.db.load_candidates()
        
        print(f"\n📊 OVERVIEW:")
        print(f"   📋 Total Jobs: {len(jobs)}")
        print(f"   👤 Total Candidates: {len(candidates)}")
        
        # Show recent jobs
        print(f"\n📝 RECENT JOBS:")
        for job in jobs[-3:]:  # Last 3 jobs
            print(f"   • {job['title']} at {job['company']}")
        
        # Show recent candidates  
        print(f"\n👥 RECENT CANDIDATES:")
        for candidate in candidates[-3:]:  # Last 3 candidates
            print(f"   • {candidate['name']} ({candidate['experience_years']} years experience)")
        
        return jobs, candidates
    
    def run_matching_and_show_results(self):
        """Run matching and display beautiful results"""
        print("\n" + "🔍" * 35)
        print("🤖 RUNNING AI MATCHING...")
        print("🔍" * 35)
        
        # Run the matcher
        results, jobs, candidates = self.matcher.find_matches()
        
        print("\n🎯 MATCHING RESULTS")
        print("="*70)
        
        best_matches = []
        
        for job_index, job_matches in results.items():
            job = jobs[job_index]
            
            if job_matches:  # If there are matches
                best_match = job_matches[0]  # Top match
                candidate = best_match['candidate']
                
                best_matches.append({
                    'job_title': job['title'],
                    'company': job['company'],
                    'candidate_name': candidate['name'],
                    'score': best_match['score'],
                    'common_skills': best_match['common_skills']
                })
                
                print(f"\n🏆 BEST MATCH FOR: {job['title']}")
                print(f"   👑 Top Candidate: {candidate['name']}")
                print(f"   ⭐ Match Score: {best_match['score']:.3f}")
                print(f"   🔧 Common Skills: {', '.join(best_match['common_skills'][:3])}")
                print(f"   🏢 Company: {job['company']}")
                print(f"   📍 Location: {job['location']} → {candidate['location']}")
        
        return best_matches
    
    def add_new_job_interactive(self):
        """Interactive form to add new job"""
        print("\n" + "➕" * 35)
        print("📝 ADD NEW JOB")
        print("➕" * 35)
        
        title = input("Job Title: ")
        company = input("Company: ")
        location = input("Location: ")
        description = input("Description: ")
        skills_input = input("Required Skills (comma separated): ")
        
        skills = [skill.strip() for skill in skills_input.split(",")]
        
        new_job = {
            "title": title,
            "company": company, 
            "location": location,
            "description": description,
            "required_skills": skills
        }
        
        job_id = self.db.add_job(new_job)
        if job_id:
            print(f"✅ Successfully added job ID: {job_id}")
        else:
            print("❌ Failed to add job")
        
        return job_id

def main():
    """Run the web interface"""
    interface = WebInterface()
    
    while True:
        print("\n" + "="*70)
        print("🚀 MAIN MENU - Choose an option:")
        print("1. 📊 View Dashboard")
        print("2. 🤖 Run AI Matching")  
        print("3. 📝 Add New Job")
        print("4. 👤 Add New Candidate")
        print("5. ❌ Exit")
        print("="*70)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            interface.show_dashboard()
        elif choice == "2":
            interface.run_matching_and_show_results()
        elif choice == "3":
            interface.add_new_job_interactive()
        elif choice == "4":
            print("👤 (Candidate feature coming soon!)")
        elif choice == "5":
            print("👋 Thank you for using Job Matcher! Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()