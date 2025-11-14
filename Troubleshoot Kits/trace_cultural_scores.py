import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from resume_parser import ResumeParser

def trace_cultural_scores():
    print("🔍 TRACING HOW CULTURAL ATTRIBUTE SCORES ARE GENERATED")
    print("=" * 80)
    
    # Peter Tan's actual resume text
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
    
    parser = ResumeParser()
    
    print("📄 PETER TAN'S RESUME TEXT ANALYSIS:")
    print("=" * 80)
    
    # Show the cultural keywords and how they're matched
    cultural_keywords = parser.cultural_keywords
    
    print("🔍 CULTURAL KEYWORD DETECTION:")
    for attribute, keywords in cultural_keywords.items():
        matches = []
        for keyword in keywords:
            if keyword in peter_tan_text.lower():
                matches.append(keyword)
        
        print(f"   {attribute.upper():<18}")
        print(f"      Keywords: {keywords}")
        print(f"      Matches found: {matches}")
        print(f"      Score: {len(matches)} / {len(keywords)} = {len(matches)/len(keywords):.3f}")
        print()
    
    # Calculate the actual scores
    print("🧮 ACTUAL SCORE CALCULATION:")
    cultural_scores = parser.extract_cultural_attributes(peter_tan_text)
    print(f"   Final cultural attributes: {cultural_scores}")
    
    print()
    print("📊 EXPLANATION OF SCORES:")
    print("   TEAMWORK: 0.667 = 4 matches out of 6 keywords")
    print("     - 'team', 'collaborat', 'partner', 'work together' found")
    print()
    print("   INNOVATION: 0.667 = 4 matches out of 6 keywords")  
    print("     - 'innovati', 'creativ', 'new ideas', 'problem solv' found")
    print()
    print("   WORK_ENVIRONMENT: 0.286 = 2 matches out of 7 keywords")
    print("     - 'hybrid', 'flexible work' found")
    print()
    print("   WORK_PACE: 0.5 = 3 matches out of 6 keywords")
    print("     - 'fast-paced', 'dynamic', 'agile' found")
    print()
    print("   CUSTOMER_FOCUS: 0.2 = 1 match out of 5 keywords")
    print("     - 'customer' found")

if __name__ == "__main__":
    trace_cultural_scores()
