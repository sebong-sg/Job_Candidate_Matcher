import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from resume_parser import ResumeParser
from chroma_data_manager import ChromaDataManager

# Peter Tan's resume text
peter_tan_text = """
Peter Tan
Email: peter.tan@email.com
Phone: (555) 123-4567

Summary:
Experienced Python developer with 5 years in fast-paced startup environments. I thrive in collaborative team settings and enjoy working with cross-functional partners to build innovative solutions. Strong focus on customer experience and user satisfaction.

I prefer hybrid work arrangements with flexible remote options. Enjoy dynamic work environments that encourage creativity and new ideas.

Experience:
Senior Python Developer - StartupXYZ (3 years)
- Developed web applications using Django and Flask
- Worked in agile teams building customer-focused products
- Collaborated with design and product teams

Python Developer - TechSolutions (2 years)  
- Built REST APIs and backend systems
- Participated in team code reviews and pair programming

Skills:
Python, Django, Flask, JavaScript, REST API, Team Collaboration, Problem Solving

Education:
Bachelor of Computer Science - University of Technology
"""

print("🔄 RELOADING PETER TAN WITH FIXED CODE")
print("=" * 50)

# Parse the resume
parser = ResumeParser()
candidate_data = parser.parse_resume_to_candidate(peter_tan_text)

print(f"📄 Parsed cultural attributes: {candidate_data.get('cultural_attributes')}")

# Save to database
db = ChromaDataManager()
candidate_id = db.add_candidate(candidate_data)

print(f"✅ Peter Tan reloaded with ID: {candidate_id}")
print("🎯 Now check if cultural attributes are stored in database...")
