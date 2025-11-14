import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from resume_parser import ResumeParser

# Use a different candidate with clear cultural signals
test_candidate_text = """
Jane Wilson
Email: jane.wilson@email.com
Phone: (555) 987-6543

Summary:
Innovative software engineer with 4 years in fast-paced startup environments. 
I thrive in collaborative team settings and enjoy creative problem-solving.
Strong customer focus with experience in agile development teams.

I prefer remote work arrangements and enjoy dynamic, innovative environments.

Experience:
Senior Software Engineer - TechStart Inc (2 years)
- Developed applications using Python and React
- Collaborated with cross-functional teams in agile environment
- Focused on customer experience and user satisfaction

Software Developer - CodeLabs (2 years)
- Built REST APIs and worked in team settings
- Participated in creative brainstorming sessions

Skills:
Python, JavaScript, React, Team Collaboration, Problem Solving, Innovation

Education:
Bachelor of Computer Science - State University
"""

parser = ResumeParser()
result = parser.parse_resume_to_candidate(test_candidate_text)

print("🔍 CULTURAL EXTRACTION TEST - JANE WILSON:")
print(f"Name: {result['name']}")
print(f"Cultural Attributes: {result.get('cultural_attributes', 'MISSING!')}")

# Test direct extraction
direct_result = parser.extract_cultural_attributes(test_candidate_text)
print(f"Direct extraction result: {direct_result}")

# Check if it's empty
if not result.get('cultural_attributes'):
    print("❌ CULTURAL ATTRIBUTES ARE EMPTY - BUG CONFIRMED")
else:
    print("✅ Cultural attributes extracted successfully")
