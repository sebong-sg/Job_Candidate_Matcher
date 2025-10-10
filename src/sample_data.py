# 🎲 SAMPLE DATA GENERATOR
# Automatically creates sample jobs and candidates for testing

from database import DataManager
import random

class SampleDataGenerator:
    def __init__(self):
        self.db = DataManager()
    
    def generate_sample_jobs(self, count=5):
        """Generate sample job data"""
        sample_jobs = [
            {
                "title": "Senior Software Engineer",
                "description": "Develop and maintain scalable software solutions using modern technologies.",
                "required_skills": ["python", "java", "aws", "docker", "kubernetes"],
                "company": "Tech Giants Inc",
                "location": "San Francisco"
            },
            {
                "title": "Data Analyst", 
                "description": "Analyze complex datasets and provide actionable insights to stakeholders.",
                "required_skills": ["sql", "python", "excel", "tableau", "statistics"],
                "company": "Data Insights Co",
                "location": "Remote"
            },
            {
                "title": "DevOps Engineer",
                "description": "Manage cloud infrastructure and CI/CD pipelines for development teams.",
                "required_skills": ["aws", "docker", "jenkins", "terraform", "linux"],
                "company": "Cloud Solutions Ltd", 
                "location": "Austin"
            },
            {
                "title": "Frontend Developer",
                "description": "Create responsive web applications using modern JavaScript frameworks.",
                "required_skills": ["javascript", "react", "css", "html", "typescript"],
                "company": "Web Creators Inc",
                "location": "New York"
            },
            {
                "title": "AI Research Scientist",
                "description": "Research and develop cutting-edge artificial intelligence algorithms.",
                "required_skills": ["python", "pytorch", "machine learning", "research", "mathematics"],
                "company": "AI Research Lab",
                "location": "Boston"
            }
        ]
        
        added_count = 0
        for job in sample_jobs[:count]:
            job_id = self.db.add_job(job)
            if job_id:
                added_count += 1
                print(f"✅ Added sample job: {job['title']}")
        
        print(f"🎉 Successfully added {added_count} sample jobs!")
        return added_count

def main():
    """Generate sample data"""
    print("🎲 SAMPLE DATA GENERATOR")
    print("========================")
    print("This will add sample jobs to your database.")
    
    generator = SampleDataGenerator()
    count = generator.generate_sample_jobs(3)  # Add 3 sample jobs
    
    print(f"\n📊 Now you have more data to test with!")
    print("Run 'python web_app.py' to see the new jobs in action!")

if __name__ == "__main__":
    main()