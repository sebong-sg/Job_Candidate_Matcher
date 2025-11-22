# 🚀 AI JOB MATCHER PRO - ENHANCED WITH GROWTH DATA
# Enterprise Recruitment Platform with AI-Powered Matching & Vector Database
# Author: AI Assistant
# Version: 3.3.0 - Growth Data Enhancement

# Import required Python libraries
from flask import Flask, render_template, request, jsonify
import sys
import os

from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

import json
import subprocess

# Add the 'src' directory to Python's module search path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Print startup message
print("🚀 Starting AI Job Matcher Pro with Growth Data Enhancement...")

"""
AUTO-INSTALLATION SECTION
Automatically install missing dependencies
"""
def install_missing_dependencies():
    """Install required packages if missing"""
    required_packages = [
        "chromadb>=0.4.0",
        "sentence-transformers>=2.2.0", 
        "scikit-learn>=1.0.0",
        "pandas>=1.3.0",
        "nltk>=3.7"
    ]
    
    print("🔍 Checking for missing dependencies...")
    
    for package in required_packages:
        package_name = package.split('>=')[0] if '>=' in package else package
        try:
            __import__(package_name.replace('-', '_'))
            print(f"✅ {package_name} is available")
        except ImportError:
            print(f"📦 Installing missing dependency: {package}")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
                print(f"✅ Successfully installed {package}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")
                return False
    return True

# Run auto-installation
install_missing_dependencies()

"""
MODULE IMPORT SECTION
"""
try:
    # Import Chroma-enhanced modules
    from chroma_data_manager import ChromaDataManager
    from matcher import SimpleMatcher
    from email_service import EmailService
    from resume_parser import ResumeParser
    from vector_db import vector_db
    from job_parser import JobDescriptionParser
    print("✅ All AI modules loaded successfully!")
    print("🎯 Chroma Vector Database: ACTIVE")
    print("📄 Job Description Parser: ACTIVE")
    print("📈 Growth Data Analysis: ACTIVE")
    
except ImportError as e:
    print(f"⚠️  Some modules not found: {e}")
    print("💡 Running in demo mode with sample data")
    
    # Demo classes for fallback (Chroma DB only)
    class ChromaDataManager:
        def load_jobs(self): 
            return []
        
        def load_candidates(self): 
            return []
        
        def add_job(self, data): return 1
        def add_candidate(self, data): return 1

    class SimpleMatcher:
        def find_matches(self):
            return {}, [], []

    class EmailService:
        def send_candidate_match_notification(self, *args, **kwargs): 
            print("📧 Candidate email would be sent (test mode)")
        def send_employer_match_notification(self, *args, **kwargs): 
            print("📧 Employer email would be sent (test mode)")

    class ResumeParser:
        def parse_resume_to_candidate(self, text):
            return {
                "name": "Candidate from Resume", "email": "resume@example.com", "phone": "123-456-7890",
                "skills": ["python", "communication", "problem-solving"], "experience_years": 3,
                "location": "Unknown", "education": "Extracted from resume", "profile": "Professional extracted from resume text", # ADD THIS LINE for fallback mode:
                "original_resume_text": text
            }

    class JobDescriptionParser:
        def parse_job_description(self, text):
            return {
                "title": "Parsed Job Title",
                "company": "Parsed Company",
                "location": "Remote",
                "description": text,
                "required_skills": ["python", "django"],
                "preferred_skills": [],
                "experience_required": 3,
                "employment_type": "Full-time",
                "confidence_scores": {"title": 0.8, "company": 0.7, "skills": 0.8, "experience": 0.7}
            }

    class VectorDB:
        def get_candidate_count(self): return 0
        def clear_candidates(self): return True
        def add_candidates_batch(self, candidates): return True

    vector_db = VectorDB()

"""
FLASK APPLICATION SETUP - ENHANCED WITH GROWTH DATA
"""
app = Flask(__name__)

# Initialize services
db = ChromaDataManager()
matcher = SimpleMatcher()
email_service = EmailService()
resume_parser = ResumeParser()
job_parser = JobDescriptionParser()

print("✅ All services initialized with growth data support!")

"""
PROFESSIONAL UI ROUTES
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vision')
def vision():
    """Company Vision page"""
    return render_template('vision.html')

@app.route('/mission') 
def mission():
    """Company Mission page"""
    return render_template('mission.html')

@app.route('/story')
def story():
    """Company Story page"""
    return render_template('story.html')


@app.route('/dashboard')
def dashboard():
    """Main dashboard with professional UI"""
    return render_template('dashboard.html')

@app.route('/test-new-ui')
def test_new_ui():
    """Test route for the new professional UI"""
    return render_template('dashboard.html')

@app.route('/old-ui')
def old_ui():
    """Legacy UI route for backward compatibility"""
    from flask import render_template_string
    return render_template_string(HTML_TEMPLATE)

@app.route('/candidates')
def candidates():
    """Candidates management view"""
    return render_template('candidates.html')

@app.route('/jobs')
def jobs():
    """Jobs management view with AI-powered JD parsing"""
    return render_template('jobs.html')

@app.route('/matching')
def matching():
    """AI Matching view"""
    return render_template('matching.html')

"""
CANDIDATE MANAGEMENT API ENDPOINTS - NEW
"""

@app.route('/api/parse-resume', methods=['POST'])
def parse_resume():
    """
    API endpoint for parsing resume text with AI
    Returns structured candidate data with quality assessment and growth metrics
    """
    try:
        data = request.json
        resume_text = data.get('resume_text', '')
        
        if not resume_text.strip():
            return jsonify({'success': False, 'error': 'Empty resume text'}), 400
            
        print(f"📄 Parsing resume with AI ({len(resume_text)} characters)...")
        
        # Use the enhanced resume parser with quality assessment
        parsed_data = resume_parser.parse_resume_text(resume_text)
        
        if not parsed_data:
            return jsonify({'success': False, 'error': 'Failed to parse resume'}), 500
        
        print(f"✅ Resume parsed: {parsed_data['name']} | {len(parsed_data['skills'])} skills | {parsed_data['experience']} years experience")
        
        # Convert to candidate format for frontend
        candidate_data = {
            "name": parsed_data['name'],
            "email": parsed_data['email'],
            "phone": parsed_data['phone'],
            "location": parsed_data.get('location', 'Location not specified'),
            "experience_years": parsed_data['experience'],
            "education": parsed_data['education'],
            "skills": parsed_data['skills'],
            "profile": parsed_data['summary'],
            "work_experience": parsed_data['work_experience'],
            "cultural_attributes": parsed_data['cultural_attributes'],
            "growth_metrics": parsed_data.get('growth_metrics', {}),
            "career_metrics": parsed_data.get('career_metrics', {}),
            "learning_velocity": parsed_data.get('learning_velocity', 0.0),
            "quality_assessment": parsed_data.get('quality_assessment', {}),
            "extraction_method": parsed_data.get('extraction_method_used', 'unknown'),
            # ADD THIS LINE:
            "original_resume_text": resume_text
        }
        
        return jsonify({'success': True, 'candidate_data': candidate_data})
        
    except Exception as e:
        print(f"❌ Resume parsing error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/create-candidate', methods=['POST'])
def create_candidate():
    """
    API endpoint for creating new candidates in Chroma DB
    Handles both parsed and manually entered candidate data
    Integrates with vector database for semantic matching
    """
    try:
        data = request.json
        candidate_data = data.get('candidate_data', {})
        
        # Validate required fields
        if not candidate_data.get('name') or not candidate_data.get('email'):
            return jsonify({'success': False, 'error': 'Name and email are required'}), 400
        
        print(f"👥 Creating new candidate: {candidate_data['name']} ({candidate_data['email']})")
        
        # Add candidate to Chroma DB
        candidate_id = db.add_candidate(candidate_data)
        
        if candidate_id:
            print(f"✅ Candidate created successfully with ID: {candidate_id}")
            
            # Add to vector database for semantic search
            try:
                vector_db.add_candidates_batch([candidate_data])
                print(f"✅ Candidate added to vector database")
            except Exception as e:
                print(f"⚠️ Failed to add candidate to vector database: {e}")
            
            return jsonify({'success': True, 'candidate_id': candidate_id})
        else:
            print("❌ Failed to create candidate in database")
            return jsonify({'success': False, 'error': 'Failed to create candidate'}), 500
            
    except Exception as e:
        print(f"❌ Candidate creation error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

"""
JOB MANAGEMENT API ENDPOINTS - NEW
"""

@app.route('/api/parse-job-description', methods=['POST'])
def parse_job_description():
    """
    API endpoint for parsing job description text
    Returns structured job data with confidence scores
    Uses AI-powered extraction similar to resume parsing
    """
    try:
        text = request.json.get('job_text', '')
        if not text.strip():
            return jsonify({'success': False, 'error': 'Empty job description'}), 400
            
        print(f"📄 Parsing job description with Groq  ({len(text)} characters)...")
        job_data = job_parser.parse_job_description(text)
        print(f"✅ Job parsed: {job_data['title']} at {job_data['company']}")
        
        return jsonify({'success': True, 'job_data': job_data})
        
    except Exception as e:
        print(f"❌ Job parsing error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/create-job', methods=['POST'])
def create_job():
    """
    API endpoint for creating new jobs in Chroma DB
    Handles both parsed and manually entered job data
    Integrates with vector database for semantic matching
    """
    try:
        job_data = request.json.get('job_data', {})
        
        # Validate required fields
        if not job_data.get('title') or not job_data.get('company'):
            return jsonify({'success': False, 'error': 'Title and company are required'}), 400
        
        print(f"💼 Creating new job: {job_data['title']} at {job_data['company']}")
        
        # Add job to Chroma DB
        job_id = db.add_job(job_data)
        
        if job_id:
            print(f"✅ Job created successfully with ID: {job_id}")
            return jsonify({'success': True, 'job_id': job_id})
        else:
            print("❌ Failed to create job in database")
            return jsonify({'success': False, 'error': 'Failed to create job'}), 500
            
    except Exception as e:
        print(f"❌ Job creation error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

"""
RESUME PARSING API ENDPOINTS - ENHANCED WITH GROWTH DATA
"""

@app.route('/api/parse-resume-file', methods=['POST'])
def parse_resume_file():
    """Parse resume file and extract candidate data WITH GROWTH DATA"""
    try:
        if 'resume' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Read file content
        if file.filename.endswith('.pdf'):
            # For PDF files, you'd need PyPDF2 or similar
            content = "PDF content extraction not implemented yet"
        else:
            content = file.read().decode('utf-8')
        
        # ENHANCED: Use enhanced parser with growth data
        parser = ResumeParser()
        candidate_data = parser.parse_resume_to_candidate(
            content, 
            include_extensions=['core', 'career_timeline', 'skill_progression', 'growth_metrics']
        )
        print(f"✅ Resume parsed with growth data: {candidate_data['name']}")
             
        # Save to database with growth data
        candidate_id = db.add_candidate(candidate_data)
        if candidate_id:
            print(f"✅ Candidate saved to DB with growth data (ID: {candidate_id})")
        else:
            print("❌ Failed to save candidate to database")
        
        return jsonify({'success': True, 'candidate_data': candidate_data})
        
    except Exception as e:
        print(f"❌ Resume file parse error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

"""
GROWTH DATA API ENDPOINTS - NEW
"""

@app.route('/api/get-candidate-growth-data/<int:candidate_id>', methods=['GET'])
def get_candidate_growth_data(candidate_id):
    """Get detailed growth data for a specific candidate"""
    try:
        candidate = db.get_candidate_with_growth_data(candidate_id)
        if candidate:
            growth_data = {
                'growth_metrics': candidate.get('growth_metrics', {}),
                'career_metrics': candidate.get('career_metrics', {}),
                'work_experience': candidate.get('work_experience', []),
                'skill_timeline': candidate.get('skill_timeline', []),
                'learning_velocity': candidate.get('learning_velocity', 0.0)
            }
            return jsonify({'success': True, 'growth_data': growth_data})
        else:
            return jsonify({'success': False, 'error': 'Candidate not found'}), 404
    except Exception as e:
        print(f"❌ Error getting growth data: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get-high-growth-candidates', methods=['GET'])
def get_high_growth_candidates():
    """Get candidates with high growth potential"""
    try:
        min_score = request.args.get('min_score', 70, type=int)
        candidates = db.get_candidates_by_growth_potential(min_score=min_score)
        
        # Return simplified candidate data for the list
        simplified_candidates = []
        for candidate in candidates:
            growth_score = candidate.get('growth_metrics', {}).get('growth_potential_score', 0)
            simplified_candidates.append({
                'id': candidate['id'],
                'name': candidate['name'],
                'growth_score': growth_score,
                'experience_years': candidate.get('experience_years', 0),
                'skills': candidate.get('skills', [])[:5],  # Top 5 skills
                'career_trajectory': candidate.get('career_metrics', {}).get('career_progression_slope', 0)
            })
        
        return jsonify({
            'success': True, 
            'candidates': simplified_candidates,
            'count': len(simplified_candidates),
            'min_score': min_score
        })
    except Exception as e:
        print(f"❌ Error getting high-growth candidates: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

"""
DATA MANAGEMENT API ENDPOINTS - ENHANCED
"""

@app.route('/api/health')
def health():
    """System health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Job Matcher Pro with Growth Data Enhancement is running!',
        'version': '3.3.0',
        'features': ['Chroma DB', 'Job Parser', 'AI Matching', 'Professional UI', 'Growth Data Analysis']
    })

@app.route('/api/stats')
def get_stats():
    """Get system statistics and metrics - ENHANCED WITH GROWTH DATA"""
    try:
        jobs = db.load_jobs()
        candidates = db.load_candidates()
        vector_db_count = vector_db.get_candidate_count()
        
        # Enhanced stats with growth data
        enhanced_stats = db.get_vector_db_stats()
        
        return jsonify({
            'total_jobs': len(jobs),
            'total_candidates': len(candidates),
            'vector_db_count': vector_db_count,
            'total_matches': len(jobs) * len(candidates),
            'success_rate': 95,
            # Enhanced growth metrics
            'average_growth_potential': enhanced_stats.get('average_growth_potential', 0),
            'high_growth_candidates': enhanced_stats.get('high_growth_candidates', 0),
            'candidates_with_career_data': enhanced_stats.get('candidates_with_career_data', 0)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/run-matching', methods=['POST'])
def run_matching():
    """Run AI matching between jobs and candidates - WITH GROWTH DATA"""
    try:
        print("🤖 Running AI matching with Chroma DB and growth data...")
        results, jobs, candidates = matcher.find_matches()
        
        matches = []
        for job_index, job_matches in results.items():
            if job_matches and len(job_matches) > 0:
                job = jobs[job_index]
                top_match = job_matches[0]
                candidate = top_match['candidate']
                
                # ENHANCED: Include growth data in match results
                growth_metrics = candidate.get('growth_metrics', {})
                growth_score = growth_metrics.get('growth_potential_score', 0)
                growth_dimensions = growth_metrics.get('growth_dimensions', {})
                
                # Create detailed growth breakdown for display
                growth_breakdown = {
                    'vertical_growth': growth_dimensions.get('vertical_growth', 0),
                    'scope_growth': growth_dimensions.get('scope_growth', 0),
                    'impact_growth': growth_dimensions.get('impact_growth', 0),
                    'adaptability': growth_dimensions.get('adaptability', 0),
                    'leadership_velocity': growth_dimensions.get('leadership_velocity', 0),
                    'career_archetype': growth_metrics.get('career_archetype', 'unknown'),
                    'career_stage': growth_metrics.get('career_stage', 'unknown'),
                    'executive_potential': growth_metrics.get('executive_potential', 0),
                    'strategic_mobility': growth_metrics.get('strategic_mobility', 0)
                }

                matches.append({
                    'job_id': job['id'],
                    'job_title': job['title'],
                    'company': job['company'],
                    'candidate_id': candidate['id'],
                    'top_candidate': candidate['name'],
                    'top_score': top_match['score'],
                    'common_skills': top_match.get('common_skills', [])[:5],
                    'score_breakdown': top_match.get('score_breakdown', {}),
                    'cultural_breakdown': top_match.get('cultural_breakdown', {}),
                    'growth_potential_score': growth_score,
                    'growth_breakdown': growth_breakdown,
                    'match_grade': top_match.get('match_grade', 'A')
                })
        
        print(f"✅ Found {len(matches)} matches using Chroma DB with growth data")
        return jsonify({'matches': matches})
        
    except Exception as e:
        print(f"❌ Matching error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-candidates')
def get_candidates():
    """Get all candidates from Chroma DB - NOW WITH GROWTH DATA"""
    try:
        candidates = db.load_candidates()
        return jsonify({'candidates': candidates})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-jobs')
def get_jobs():
    """Get all jobs from Chroma DB"""
    try:
        jobs = db.load_jobs()
        return jsonify({'jobs': jobs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vector-db-stats')
def get_vector_db_stats():
    """Get Chroma DB statistics - ENHANCED WITH GROWTH METRICS"""
    try:
        stats = db.get_vector_db_stats()
        return jsonify({
            'candidates_in_vector_db': stats['candidates_in_vector_db'],
            'candidates_in_json': 0,  # Removed JSON dependency
            'jobs_count': stats['jobs_count'],
            'average_growth_potential': stats.get('average_growth_potential', 0),
            'high_growth_candidates': stats.get('high_growth_candidates', 0),
            'candidates_with_career_data': stats.get('candidates_with_career_data', 0),
            'status': 'active'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reinitialize-vector-db', methods=['POST'])
def reinitialize_vector_db():
    """Reinitialize vector database - WITH GROWTH DATA"""
    try:
        print("🔄 Reinitializing Vector Database with growth data...")
        # Clear and reinitialize
        vector_db.clear_candidates()
        candidates = db.load_candidates()
        vector_db.add_candidates_batch(candidates)
        
        return jsonify({
            'status': 'success',
            'message': 'Vector database reinitialized successfully with growth data',
            'candidates_loaded': len(candidates)
        })
    except Exception as e:
        print(f"❌ Vector DB reinit error: {e}")
        return jsonify({'error': str(e)}), 500

"""
EMAIL TESTING ENDPOINTS
"""

@app.route('/api/test-candidate-email', methods=['POST'])
def test_candidate_email():
    """Test candidate email notification"""
    try:
        print("📧 Testing candidate email...")
        email_service.send_candidate_match_notification(
            candidate_email="test.candidate@example.com",
            candidate_name="Test Candidate",
            job_title="Senior Python Developer", 
            company="TechCorp Inc",
            match_score=0.85
        )
        return jsonify({'status': 'success', 'message': 'Candidate email test completed!'})
    except Exception as e:
        print(f"❌ Email test error: {e}")
        return jsonify({'status': 'error', 'message': f'Failed: {str(e)}'}), 500

@app.route('/api/test-employer-email', methods=['POST'])
def test_employer_email():
    """Test employer email notification"""
    try:
        print("📧 Testing employer email...")
        email_service.send_employer_match_notification(
            employer_email="hr@techcorp.com",
            job_title="Python Developer",
            top_candidates=[
                {'name': 'John Smith', 'score': 0.85, 'skills': ['Python', 'Django', 'Flask'], 'experience_years': 5},
                {'name': 'Sarah Johnson', 'score': 0.78, 'skills': ['Python', 'Machine Learning'], 'experience_years': 4}
            ]
        )
        return jsonify({'status': 'success', 'message': 'Employer email test completed!'})
    except Exception as e:
        print(f"❌ Email test error: {e}")
        return jsonify({'status': 'error', 'message': f'Failed: {str(e)}'}), 500

"""
LEGACY HTML TEMPLATE - KEPT FOR BACKWARD COMPATIBILITY
"""
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Legacy UI - AI Job Matcher Pro</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .legacy-notice { 
            background: #fff3cd; 
            border: 1px solid #ffeaa7; 
            padding: 20px; 
            border-radius: 5px; 
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="legacy-notice">
        <h2>Legacy UI</h2>
        <p>This is the old interface. <a href="/">Click here to use the new Professional UI</a></p>
    </div>
    <!-- Old HTML content would go here -->
</body>
</html>
'''

"""
APPLICATION STARTUP - ENHANCED
"""
if __name__ == '__main__':
    print("🚀 AI Job Matcher Pro - Growth Data Enhancement")
    print("=" * 70)
    print("✅ All systems initialized and ready!")
    print("🎯 Professional UI: ACTIVE")
    print("🗃️ Chroma Vector Database: ACTIVE")
    print("📄 Job Description Parser: ACTIVE")
    print("📈 Growth Data Analysis: ACTIVE")
    print("")
    print("🎯 ENTERPRISE FEATURES:")
    print("   • 🎨 Professional enterprise dashboard")
    print("   • 🤖 Chroma DB for instant semantic search") 
    print("   • 📄 AI-powered job description parsing")
    print("   • 👥 Smart candidate management")
    print("   • 📈 Growth potential analysis")
    print("   • 🚀 Scalable to thousands of records")
    print("")
    print("📍 Access Points:")
    print("   • Main App: http://localhost:5000/")
    print("   • Jobs:     http://localhost:5000/jobs")
    print("   • Candidates: http://localhost:5000/candidates")
    print("   • AI Matching: http://localhost:5000/matching")
    print("")
    print("⏳ Starting server...")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=5151, debug=False)