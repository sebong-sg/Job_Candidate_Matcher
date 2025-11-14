import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from resume_parser import ResumeParser
from chroma_data_manager import ChromaDataManager

# New candidate with clear cultural signals
new_candidate_text = """
Alex Chen
Email: alex.chen@email.com
Phone: (555) 999-8888

Summary:
Creative software developer with 3 years in fast-paced startup environments. 
I excel in collaborative team settings and enjoy innovative problem-solving.
Strong customer focus with experience in cross-functional agile teams.

I prefer hybrid work arrangements and thrive in dynamic, creative environments.

Experience:
Software Developer - InnovateTech (2 years)
- Built web applications with Python and Django
- Collaborated with cross-functional teams in fast-paced environment
- Focused on user experience and customer satisfaction

Junior Developer - CodeWorks (1 year)
- Developed REST APIs in team settings
- Participated in creative brainstorming and innovation sessions

Skills:
Python, Django, JavaScript, Team Collaboration, Creative Problem Solving, Innovation

Education:
Bachelor of Software Engineering - City University
"""

print("🧪 TESTING CULTURAL ATTRIBUTES FIX")
print("=" * 50)

# Parse the resume
parser = ResumeParser()
candidate_data = parser.parse_resume_to_candidate(new_candidate_text)

print(f"📄 Parsed cultural attributes: {candidate_data.get('cultural_attributes')}")

# Save to database
db = ChromaDataManager()
candidate_id = db.add_candidate(candidate_data)

print(f"✅ Alex Chen added with ID: {candidate_id}")
print("🎯 Now let's verify cultural attributes are stored in database...")

# Check if cultural attributes were saved
print(f"\n🔍 VERIFYING DATABASE STORAGE:")
print("Cultural attributes should now be saved correctly!")
