import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chroma_data_manager import ChromaDataManager
from job_parser import JobDescriptionParser

def restore_jobs_with_cultural():
    print("🔄 RESTORING JOBS WITH ENHANCED CULTURAL ATTRIBUTES...")
    
    db = ChromaDataManager()
    job_parser = JobDescriptionParser()
    
    # Jobs with rich cultural descriptions for better extraction
    jobs_data = [
        {
            "title": "Senior Python Developer",
            "company": "TechCorp Inc", 
            "location": "Remote",
            "description": "Join our collaborative team at TechCorp! We're looking for a Python developer who thrives in our fast-paced, innovative environment. We value teamwork and creative problem-solving. Our remote-first culture focuses on work-life balance while maintaining strong team connections through virtual collaboration.",
            "required_skills": ["python", "django", "flask", "rest api", "sql"],
            "experience_required": 0,
            "job_type": "Full-time"
        },
        {
            "title": "Machine Learning Engineer", 
            "company": "AI Innovations",
            "location": "San Francisco",
            "description": "At AI Innovations, we push the boundaries of what's possible! Our fast-paced research environment encourages groundbreaking thinking and creative solutions. We collaborate closely across teams to solve complex problems. Join us in our San Francisco office where innovation meets execution.",
            "required_skills": ["python", "machine learning", "tensorflow", "pytorch", "data analysis"],
            "experience_required": 3,
            "job_type": "Full-time"
        },
        {
            "title": "Frontend React Developer",
            "company": "WebSolutions Ltd", 
            "location": "San Francisco",
            "description": "WebSolutions values collaborative teamwork in our creative office environment. We're looking for developers who enjoy pair programming and cross-functional collaboration. Our hybrid model offers 3 days in our vibrant SF office and 2 days remote flexibility.",
            "required_skills": ["javascript", "react", "html", "css", "web development"],
            "experience_required": 2,
            "job_type": "Full-time"
        },
        {
            "title": "Senior Software Engineer",
            "company": "Tech Giants Inc",
            "location": "New York", 
            "description": "Join our established, stable engineering team at Tech Giants. We value methodical approaches and structured processes. Our New York office provides a professional environment for focused, individual work with regular team syncs. Customer satisfaction drives our development priorities.",
            "required_skills": ["python", "java", "aws", "docker", "kubernetes"],
            "experience_required": 5,
            "job_type": "Full-time"
        },
        {
            "title": "Data Analyst",
            "company": "Data Insights Co",
            "location": "Remote", 
            "description": "Fully remote position at Data Insights! We're customer-obsessed and value team members who understand user needs. Our distributed team collaborates asynchronously with flexible hours. We focus on data-driven insights that directly impact customer experience.",
            "required_skills": ["sql", "python", "excel", "tableau", "statistics"],
            "experience_required": 2,
            "job_type": "Full-time"
        },
        {
            "title": "DevOps Engineer", 
            "company": "Cloud Solutions Ltd",
            "location": "Austin",
            "description": "Fast-paced startup environment in Austin! We move quickly and value automation and innovation. Our team collaborates closely to build robust infrastructure. Join our dynamic office culture where new ideas are celebrated and implemented rapidly.",
            "required_skills": ["aws", "docker", "jenkins", "terraform", "linux"],
            "experience_required": 3,
            "job_type": "Full-time"
        },
        {
            "title": "Innovation Lead - Python",
            "company": "CreativeTech Labs", 
            "location": "Remote",
            "description": "Lead innovation at CreativeTech! We're looking for creative thinkers who thrive on new ideas and outside-the-box solutions. Our fully remote team collaborates across time zones with a focus on innovation and user-centric design. We value autonomy and creative freedom.",
            "required_skills": ["python", "innovation", "research", "prototyping", "team leadership"],
            "experience_required": 4,
            "job_type": "Full-time"
        },
        {
            "title": "Customer-Focused Python Developer",
            "company": "UserFirst Tech", 
            "location": "Hybrid",
            "description": "Join our customer-obsessed team! Every line of code we write focuses on user experience and customer satisfaction. Our hybrid model balances office collaboration with remote flexibility. We work closely with customers to understand their needs and deliver exceptional solutions.",
            "required_skills": ["python", "django", "customer development", "user testing", "feedback loops"],
            "experience_required": 3,
            "job_type": "Full-time"
        }
    ]
    
    print(f"Creating {len(jobs_data)} jobs with enhanced cultural attributes...")
    
    for i, job_data in enumerate(jobs_data, 1):
        # Parse the job to generate cultural attributes
        parsed_job = job_parser.parse_job_description(job_data['description'])
        
        # Create the job with parsed data including cultural attributes
        job_id = db.add_job({
            'title': job_data['title'],
            'company': job_data['company'],
            'location': job_data['location'],
            'description': job_data['description'],
            'required_skills': job_data['required_skills'],
            'experience_required': job_data['experience_required'],
            'employment_type': job_data['job_type'],
            'cultural_attributes': parsed_job.get('cultural_attributes', {})
        })
        
        print(f"✅ {i}. {job_data['title']} at {job_data['company']} (ID: {job_id})")
        if parsed_job.get('cultural_attributes'):
            print(f"   Cultural: {parsed_job['cultural_attributes']}")
    
    print(f"🎉 Successfully created {len(jobs_data)} jobs with cultural attributes!")

if __name__ == "__main__":
    restore_jobs_with_cultural()
