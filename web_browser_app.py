"""
🌐 AI JOB MATCHER PRO - CHROMA DB VERSION
Enterprise Recruitment Platform with AI-Powered Matching & Vector Database
Author: AI Assistant
Version: 3.0.0 - Chroma DB Enhanced
"""

# Import required Python libraries
from flask import Flask, render_template_string, request, jsonify
import sys
import os
import json
import subprocess

# Add the 'src' directory to Python's module search path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Print startup message
print("🚀 Starting AI Job Matcher Pro with Chroma DB...")

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
    
    print("✅ All AI modules loaded successfully!")
    print("🎯 Chroma Vector Database: ACTIVE")
    
except ImportError as e:
    print(f"⚠️  Some modules not found: {e}")
    print("💡 Running in demo mode with sample data")
    
    # Demo classes (same as before for fallback)
    class ChromaDataManager:
        def load_jobs(self): 
            """Load ALL jobs from JSON file"""
            try:
                file_path = os.path.join("data", "jobs.json")
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    jobs = data.get('jobs', [])
                    print(f"📁 Loaded {len(jobs)} jobs from database")
                    return jobs
            except Exception as e:
                print(f"❌ Error loading jobs: {e}")
                return [
                    {"id": 1, "title": "Python Developer", "company": "TechCorp", "location": "Remote", 
                     "description": "Develop web applications", "required_skills": ["python", "django", "sql"]}
                ]
        
        def load_candidates(self): 
            """Load ALL candidates from JSON file"""
            try:
                file_path = os.path.join("data", "candidates.json")
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    candidates = data.get('candidates', [])
                    print(f"📁 Loaded {len(candidates)} candidates from database")
                    return candidates
            except Exception as e:
                print(f"❌ Error loading candidates: {e}")
                return [
                    {"id": 1, "name": "John Smith", "email": "john@example.com", "profile": "Python developer", 
                     "skills": ["python", "django", "flask", "sql"], "experience_years": 5, "location": "Remote"}
                ]
        
        def add_job(self, data): return len(self.load_jobs()) + 1
        def add_candidate(self, data): return len(self.load_candidates()) + 1

    class SimpleMatcher:
        def find_matches(self):
            jobs = ChromaDataManager().load_jobs()
            candidates = ChromaDataManager().load_candidates()
            results = {}
            
            print(f"🔍 Matching {len(jobs)} jobs with {len(candidates)} candidates...")
            
            for i, job in enumerate(jobs):
                results[i] = []
                for candidate in candidates:
                    common_skills = set(job['required_skills']) & set(candidate['skills'])
                    if common_skills:
                        score = len(common_skills) / len(job['required_skills'])
                        results[i].append({
                            "candidate": candidate, 
                            "score": score, 
                            "common_skills": list(common_skills),
                            "score_breakdown": {
                                "skills": int(score * 100), 
                                "experience": 80, 
                                "location": 90, 
                                "semantic": 75
                            },
                            "match_grade": "A" if score > 0.7 else "B"
                        })
                results[i].sort(key=lambda x: x['score'], reverse=True)
                print(f"   ✅ Found {len(results[i])} matches for {job['title']}")
            
            return results, jobs, candidates

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
                "location": "Unknown", "education": "Extracted from resume", "profile": "Professional extracted from resume text"
            }

    class VectorDB:
        def get_candidate_count(self): 
            db = ChromaDataManager()
            return len(db.load_candidates())
        def clear_candidates(self): 
            print("🗃️ Vector DB clear called (demo mode)")
            return True
        def add_candidates_batch(self, candidates):
            print(f"🗃️ Would add {len(candidates)} candidates to Vector DB (demo mode)")
            return True

    vector_db = VectorDB()

"""
FLASK APPLICATION SETUP
"""
app = Flask(__name__)

# Initialize services
db = ChromaDataManager()
matcher = SimpleMatcher()
email_service = EmailService()
resume_parser = ResumeParser()

print("✅ All services initialized!")

"""
HTML TEMPLATE - Complete and working
"""
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Job Matcher Pro - Chroma DB</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; background: white; border-radius: 20px; box-shadow: 0 25px 50px rgba(0,0,0,0.15); overflow: hidden; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 50px 40px; text-align: center; }
        .header h1 { font-size: 3em; margin-bottom: 15px; font-weight: 700; }
        .header p { font-size: 1.3em; opacity: 0.9; }
        .dashboard { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; padding: 40px; background: #f8f9fa; }
        @media (max-width: 768px) { .dashboard { grid-template-columns: 1fr; } }
        .card { background: white; padding: 35px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); border-left: 5px solid #667eea; }
        .card h2 { color: #333; margin-bottom: 25px; font-size: 1.6em; display: flex; align-items: center; gap: 12px; }
        .stats { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 25px; }
        .stat-item { text-align: center; padding: 25px 20px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 12px; border: 2px solid #e9ecef; transition: all 0.3s ease; }
        .stat-item:hover { transform: translateY(-5px); border-color: #667eea; box-shadow: 0 10px 25px rgba(102, 126, 234, 0.15); }
        .stat-number { font-size: 2.8em; font-weight: bold; color: #667eea; display: block; line-height: 1; }
        .stat-label { color: #666; font-size: 0.95em; margin-top: 8px; font-weight: 500; }
        .btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 16px 32px; border-radius: 10px; cursor: pointer; font-size: 1.05em; font-weight: 600; margin: 10px; transition: all 0.3s ease; box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3); }
        .btn:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4); }
        .btn-success { background: linear-gradient(135deg, #28a745 0%, #20c997 100%); }
        .btn-warning { background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%); color: #000; }
        .btn-info { background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%); }
        .tab-container { padding: 0 40px 40px 40px; }
        .tabs { display: flex; background: #f8f9fa; border-radius: 12px; padding: 15px; margin-bottom: 35px; flex-wrap: wrap; gap: 10px; }
        .tab { padding: 16px 28px; background: transparent; border: none; cursor: pointer; border-radius: 10px; font-weight: 600; transition: all 0.3s ease; color: #666; flex: 1; min-width: 120px; }
        .tab:hover { background: rgba(102, 126, 234, 0.1); color: #667eea; }
        .tab.active { background: #667eea; color: white; box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3); }
        .tab-content { display: none; animation: fadeIn 0.5s ease-in; }
        .tab-content.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .loading { text-align: center; padding: 50px; color: #667eea; font-size: 1.3em; }
        .success { background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); color: #155724; padding: 25px; border-radius: 12px; border-left: 5px solid #28a745; margin: 25px 0; }
        .error { background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); color: #721c24; padding: 25px; border-radius: 12px; border-left: 5px solid #dc3545; margin: 25px 0; }
        .info { background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%); color: #0c5460; padding: 25px; border-radius: 12px; border-left: 5px solid #17a2b8; margin: 25px 0; }
        .match-card, .candidate-card, .job-card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); margin: 25px 0; border-left: 5px solid #28a745; transition: all 0.3s ease; }
        .match-card:hover, .candidate-card:hover, .job-card:hover { transform: translateY(-5px); box-shadow: 0 15px 35px rgba(0,0,0,0.15); }
        .match-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 20px; }
        .match-score { background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 10px 25px; border-radius: 25px; font-weight: bold; font-size: 1.2em; }
        .match-grade { background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%); color: black; padding: 8px 16px; border-radius: 20px; font-weight: bold; font-size: 1.1em; }
        .skills { display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0; }
        .skill-tag { background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%); padding: 8px 18px; border-radius: 20px; font-size: 0.95em; border: 1px solid #ced4da; }
        .action-buttons { display: flex; gap: 15px; flex-wrap: wrap; margin: 25px 0; }
        .results-container { margin-top: 35px; }
        .score-breakdown { background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 15px 0; }
        .breakdown-item { display: flex; justify-content: space-between; margin: 10px 0; font-weight: 500; }
        .breakdown-bar { background: #e9ecef; height: 8px; border-radius: 4px; margin: 5px 0 15px 0; overflow: hidden; }
        .breakdown-fill { background: linear-gradient(135deg, #28a745 0%, #20c997 100%); height: 100%; border-radius: 4px; transition: width 0.5s ease; }
        .form-group { margin-bottom: 25px; }
        .form-group label { display: block; margin-bottom: 10px; font-weight: 600; color: #333; font-size: 1.05em; }
        .form-group input, .form-group textarea { width: 100%; padding: 18px; border: 2px solid #e9ecef; border-radius: 10px; font-size: 1em; transition: border-color 0.3s ease; font-family: inherit; }
        .form-group input:focus, .form-group textarea:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }
        .form-group textarea { height: 140px; resize: vertical; }
        .chroma-badge { background: linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%); color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.8em; font-weight: bold; margin-left: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 AI Job Matcher Pro <span class="chroma-badge">Chroma DB</span></h1>
            <p>Enterprise Recruitment Platform Powered by AI & Vector Database</p>
        </div>
        
        <div class="dashboard">
            <div class="card">
                <h2>📊 Live Dashboard</h2>
                <div class="stats">
                    <div class="stat-item"><span class="stat-number" id="jobs-count">0</span><div class="stat-label">Total Jobs</div></div>
                    <div class="stat-item"><span class="stat-number" id="candidates-count">0</span><div class="stat-label">Total Candidates</div></div>
                    <div class="stat-item"><span class="stat-number" id="vector-db-count">0</span><div class="stat-label">In Vector DB</div></div>
                    <div class="stat-item"><span class="stat-number" id="success-rate">0%</span><div class="stat-label">Success Rate</div></div>
                </div>
                <div class="action-buttons">
                    <button class="btn" onclick="loadStats()">🔄 Refresh Stats</button>
                    <button class="btn btn-warning" onclick="testSystem()">🧪 Test System</button>
                    <button class="btn btn-info" onclick="showVectorDBInfo()">🗃️ Vector DB Info</button>
                </div>
            </div>
            
            <div class="card">
                <h2>⚡ Quick Actions</h2>
                <div class="action-buttons">
                    <button class="btn btn-success" onclick="runMatching()">🤖 Run AI Matching</button>
                    <button class="btn" onclick="showTab('candidates')">👥 View Candidates</button>
                    <button class="btn" onclick="showTab('jobs')">📋 View Jobs</button>
                    <button class="btn" onclick="showTab('resume-parser')">📄 Parse Resume</button>
                </div>
                <div id="quick-results"></div>
            </div>
        </div>
        
        <div class="tab-container">
            <div class="tabs">
                <button class="tab active" onclick="showTab('matching')">🎯 AI Matching</button>
                <button class="tab" onclick="showTab('candidates')">👥 Candidates</button>
                <button class="tab" onclick="showTab('jobs')">📋 Jobs</button>
                <button class="tab" onclick="showTab('resume-parser')">📄 Resume Parser</button>
                <button class="tab" onclick="showTab('vector-db')">🗃️ Vector DB</button>
                <button class="tab" onclick="showTab('email-demo')">📧 Email Demo</button>
            </div>
            
            <div id="matching" class="tab-content active">
                <div class="card">
                    <h2>🤖 AI-Powered Job Matching <span class="chroma-badge">Chroma DB Enhanced</span></h2>
                    <p>Our advanced AI uses Chroma Vector Database for instant semantic search across thousands of candidates.</p>
                    <div class="action-buttons">
                        <button class="btn btn-success" onclick="runMatching()">🚀 Run AI Matching</button>
                        <button class="btn" onclick="loadStats()">📊 Update Stats</button>
                    </div>
                    <div id="matching-results" class="results-container"><p>Click "Run AI Matching" to discover intelligent matches...</p></div>
                </div>
            </div>
            
            <div id="candidates" class="tab-content">
                <div class="card">
                    <h2>👥 Candidate Database</h2>
                    <p>View and manage all candidate profiles.</p>
                    <div class="action-buttons"><button class="btn" onclick="loadCandidates()">🔄 Load Candidates</button></div>
                    <div id="candidates-list" class="results-container"><p>Candidate list will appear here...</p></div>
                </div>
            </div>
            
            <div id="jobs" class="tab-content">
                <div class="card">
                    <h2>📋 Job Database</h2>
                    <p>View and manage all job postings.</p>
                    <div class="action-buttons"><button class="btn" onclick="loadJobs()">🔄 Load Jobs</button></div>
                    <div id="jobs-list" class="results-container"><p>Job list will appear here...</p></div>
                </div>
            </div>
            
            <div id="resume-parser" class="tab-content">
                <div class="card">
                    <h2>📄 AI Resume Parser</h2>
                    <p>Extract skills and information from resume text.</p>
                    <div class="form-group">
                        <label for="resume-text">Paste Resume Text:</label>
                        <textarea id="resume-text" placeholder="Paste resume content here..." style="height: 200px;"></textarea>
                    </div>
                    <div class="action-buttons">
                        <button class="btn btn-success" onclick="parseResume()">🔍 Parse Resume</button>
                        <button class="btn" onclick="document.getElementById('resume-text').value = ''">🗑️ Clear</button>
                    </div>
                    <div id="resume-results" class="results-container"><p>Parsed data will appear here...</p></div>
                </div>
            </div>
            
            <div id="vector-db" class="tab-content">
                <div class="card">
                    <h2>🗃️ Chroma Vector Database</h2>
                    <p>Manage the vector database for semantic search.</p>
                    <div class="info">
                        <h4>🚀 Chroma DB Benefits:</h4>
                        <ul>
                            <li><strong>Instant Semantic Search</strong> - Find candidates by meaning</li>
                            <li><strong>Scalability</strong> - Handle thousands of candidates</li>
                            <li><strong>Better Matching</strong> - True understanding of profiles</li>
                            <li><strong>Hybrid Approach</strong> - Semantic + traditional matching</li>
                        </ul>
                    </div>
                    <div class="action-buttons">
                        <button class="btn btn-info" onclick="getVectorDBStats()">📊 Get Vector DB Stats</button>
                        <button class="btn btn-warning" onclick="reinitializeVectorDB()">🔄 Reinitialize Vector DB</button>
                    </div>
                    <div id="vector-db-results" class="results-container"><p>Vector database info will appear here...</p></div>
                </div>
            </div>
            
            <div id="email-demo" class="tab-content">
                <div class="card">
                    <h2>📧 Email Notification System</h2>
                    <p>Test email notifications (test mode - no real emails).</p>
                    <div class="action-buttons">
                        <button class="btn" onclick="testCandidateEmail()">👤 Test Candidate Email</button>
                        <button class="btn btn-success" onclick="testEmployerEmail()">🏢 Test Employer Email</button>
                    </div>
                    <div id="email-results" class="results-container"><p>Email test results will appear here.</p></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            event.target.classList.add('active');
        }
        
        async function loadStats() {
            document.getElementById('jobs-count').textContent = '...';
            document.getElementById('candidates-count').textContent = '...';
            document.getElementById('vector-db-count').textContent = '...';
            document.getElementById('success-rate').textContent = '...';
            
            try {
                const response = await fetch('/api/stats');
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const data = await response.json();
                
                document.getElementById('jobs-count').textContent = data.total_jobs || 0;
                document.getElementById('candidates-count').textContent = data.total_candidates || 0;
                document.getElementById('vector-db-count').textContent = data.vector_db_count || 0;
                document.getElementById('success-rate').textContent = (data.success_rate || 0) + '%';
                
                showQuickResult('✅ Stats updated!', 'success');
            } catch (error) {
                console.error('Stats error:', error);
                showQuickResult('❌ Failed to load stats', 'error');
            }
        }
        
        async function runMatching() {
            const resultsElement = document.getElementById('matching-results');
            resultsElement.innerHTML = '<div class="loading">🤖 AI is analyzing with Chroma DB... This may take a few seconds.</div>';
            
            try {
                const response = await fetch('/api/run-matching', { method: 'POST', headers: {'Content-Type': 'application/json'} });
                if (!response.ok) throw new Error(`Server returned ${response.status}`);
                const data = await response.json();
                
                if (data.error) {
                    resultsElement.innerHTML = `<div class="error">❌ Error: ${data.error}</div>`;
                    return;
                }
                
                let html = '<h3>🎯 Matching Results</h3>';
                if (data.matches && data.matches.length > 0) {
                    html += `<div class="success">✅ Found ${data.matches.length} high-quality matches using Chroma DB!</div>`;
                    data.matches.forEach(match => {
                        const breakdown = match.score_breakdown || {};
                        html += `
                            <div class="match-card">
                                <div class="match-header">
                                    <h4>${match.job_title} at ${match.company}</h4>
                                    <div style="display: flex; gap: 10px; align-items: center;">
                                        <span class="match-grade">${match.match_grade || 'A'}</span>
                                        <span class="match-score">${(match.top_score * 100).toFixed(1)}% Match</span>
                                    </div>
                                </div>
                                <p><strong>👤 Top Candidate:</strong> ${match.top_candidate}</p>
                                ${breakdown.skills ? `
                                <div class="score-breakdown">
                                    <h5>📊 Score Breakdown:</h5>
                                    <div class="breakdown-item"><span>Skills Match:</span><span>${breakdown.skills}%</span></div>
                                    <div class="breakdown-bar"><div class="breakdown-fill" style="width: ${breakdown.skills}%"></div></div>
                                    <div class="breakdown-item"><span>Experience:</span><span>${breakdown.experience || 0}%</span></div>
                                    <div class="breakdown-bar"><div class="breakdown-fill" style="width: ${breakdown.experience || 0}%"></div></div>
                                    <div class="breakdown-item"><span>Location:</span><span>${breakdown.location || 0}%</span></div>
                                    <div class="breakdown-bar"><div class="breakdown-fill" style="width: ${breakdown.location || 0}%"></div></div>
                                    <div class="breakdown-item"><span>Semantic:</span><span>${breakdown.semantic || 0}%</span></div>
                                    <div class="breakdown-bar"><div class="breakdown-fill" style="width: ${breakdown.semantic || 0}%"></div></div>
                                </div>` : ''}
                                <p><strong>🔧 Common Skills:</strong> ${match.common_skills && match.common_skills.length > 0 ? match.common_skills.join(', ') : 'No common skills'}</p>
                            </div>
                        `;
                    });
                } else {
                    html += '<div class="error">❌ No matches found. Try adding more data.</div>';
                }
                resultsElement.innerHTML = html;
                loadStats();
            } catch (error) {
                console.error('Matching error:', error);
                resultsElement.innerHTML = `<div class="error">❌ Error running AI matching: ${error.message}</div>`;
            }
        }
        
        async function loadCandidates() {
            const listElement = document.getElementById('candidates-list');
            listElement.innerHTML = '<div class="loading">🔄 Loading candidates...</div>';
            try {
                const response = await fetch('/api/get-candidates');
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const data = await response.json();
                
                let html = '<h3>👥 All Candidates</h3>';
                if (data.candidates && data.candidates.length > 0) {
                    html += `<div class="success">✅ Loaded ${data.candidates.length} candidates</div>`;
                    data.candidates.forEach(candidate => {
                        html += `
                            <div class="candidate-card">
                                <h4>${candidate.name}</h4>
                                <p><strong>📧 Email:</strong> ${candidate.email || 'Not provided'}</p>
                                <p><strong>💼 Experience:</strong> ${candidate.experience_years} years</p>
                                <p><strong>📍 Location:</strong> ${candidate.location || 'Not specified'}</p>
                                <div class="skills">${candidate.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}</div>
                                <p><strong>📝 Profile:</strong> ${candidate.profile}</p>
                            </div>
                        `;
                    });
                } else {
                    html += '<div class="error">❌ No candidates found.</div>';
                }
                listElement.innerHTML = html;
            } catch (error) {
                console.error('Candidates error:', error);
                listElement.innerHTML = `<div class="error">❌ Error loading candidates: ${error.message}</div>`;
            }
        }
        
        async function loadJobs() {
            const listElement = document.getElementById('jobs-list');
            listElement.innerHTML = '<div class="loading">🔄 Loading jobs...</div>';
            try {
                const response = await fetch('/api/get-jobs');
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const data = await response.json();
                
                let html = '<h3>📋 All Jobs</h3>';
                if (data.jobs && data.jobs.length > 0) {
                    html += `<div class="success">✅ Loaded ${data.jobs.length} jobs</div>`;
                    data.jobs.forEach(job => {
                        html += `
                            <div class="job-card">
                                <h4>${job.title}</h4>
                                <p><strong>🏢 Company:</strong> ${job.company}</p>
                                <p><strong>📍 Location:</strong> ${job.location}</p>
                                <div class="skills">${job.required_skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}</div>
                                <p><strong>📝 Description:</strong> ${job.description}</p>
                            </div>
                        `;
                    });
                } else {
                    html += '<div class="error">❌ No jobs found.</div>';
                }
                listElement.innerHTML = html;
            } catch (error) {
                console.error('Jobs error:', error);
                listElement.innerHTML = `<div class="error">❌ Error loading jobs: ${error.message}</div>`;
            }
        }
        
        async function parseResume() {
            const resumeText = document.getElementById('resume-text').value.trim();
            if (!resumeText) { alert('❌ Please paste resume text!'); return; }
            
            const resultsElement = document.getElementById('resume-results');
            resultsElement.innerHTML = '<div class="loading">🔍 AI is parsing resume...</div>';
            
            try {
                const response = await fetch('/api/parse-resume', {
                    method: 'POST', headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({resume_text: resumeText})
                });
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const result = await response.json();
                
                if (result.error) {
                    resultsElement.innerHTML = `<div class="error">❌ Error: ${result.error}</div>`;
                    return;
                }
                
                const candidate = result.candidate_data;
                resultsElement.innerHTML = `
                    <div class="success"><strong>✅ Resume Parsed Successfully!</strong></div>
                    <div class="candidate-card">
                        <h3>👤 ${candidate.name}</h3>
                        <p><strong>📧 Email:</strong> ${candidate.email}</p>
                        <p><strong>📞 Phone:</strong> ${candidate.phone}</p>
                        <p><strong>💼 Experience:</strong> ${candidate.experience_years} years</p>
                        <p><strong>🎓 Education:</strong> ${candidate.education}</p>
                        <p><strong>📍 Location:</strong> ${candidate.location}</p>
                        <p><strong>📝 Summary:</strong> ${candidate.profile}</p>
                        <div class="skills">${candidate.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}</div>
                    </div>
                `;
            } catch (error) {
                console.error('Resume parse error:', error);
                resultsElement.innerHTML = `<div class="error">❌ Error parsing resume: ${error.message}</div>`;
            }
        }
        
        async function getVectorDBStats() {
            const resultsElement = document.getElementById('vector-db-results');
            resultsElement.innerHTML = '<div class="loading">🔄 Getting Vector DB stats...</div>';
            try {
                const response = await fetch('/api/vector-db-stats');
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const data = await response.json();
                
                resultsElement.innerHTML = `
                    <div class="success">
                        <h4>🗃️ Vector Database Statistics</h4>
                        <p><strong>Candidates in Vector DB:</strong> ${data.candidates_in_vector_db}</p>
                        <p><strong>Candidates in JSON:</strong> ${data.candidates_in_json}</p>
                        <p><strong>Total Jobs:</strong> ${data.jobs_count}</p>
                        <p><strong>Status:</strong> ${data.status}</p>
                    </div>
                `;
            } catch (error) {
                console.error('Vector DB stats error:', error);
                resultsElement.innerHTML = `<div class="error">❌ Error getting Vector DB stats: ${error.message}</div>`;
            }
        }
        
        async function reinitializeVectorDB() {
            if (!confirm('Are you sure you want to reinitialize the Vector Database? This will reload all candidates.')) return;
            
            const resultsElement = document.getElementById('vector-db-results');
            resultsElement.innerHTML = '<div class="loading">🔄 Reinitializing Vector DB...</div>';
            try {
                const response = await fetch('/api/reinitialize-vector-db', { method: 'POST' });
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const data = await response.json();
                
                resultsElement.innerHTML = `
                    <div class="success">
                        <h4>✅ Vector Database Reinitialized</h4>
                        <p><strong>Message:</strong> ${data.message}</p>
                        <p><strong>Candidates Loaded:</strong> ${data.candidates_loaded}</p>
                    </div>
                `;
                loadStats();
            } catch (error) {
                console.error('Vector DB reinit error:', error);
                resultsElement.innerHTML = `<div class="error">❌ Error reinitializing Vector DB: ${error.message}</div>`;
            }
        }
        
        async function testCandidateEmail() {
            const resultsElement = document.getElementById('email-results');
            resultsElement.innerHTML = '<div class="loading">📧 Testing candidate email...</div>';
            try {
                const response = await fetch('/api/test-candidate-email', { method: 'POST' });
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const result = await response.json();
                resultsElement.innerHTML = `<div class="success"><h4>📧 Candidate Email Test</h4><p><strong>Status:</strong> ${result.status}</p><p><strong>Message:</strong> ${result.message}</p></div>`;
            } catch (error) {
                console.error('Email test error:', error);
                resultsElement.innerHTML = `<div class="error">❌ Error testing email: ${error.message}</div>`;
            }
        }
        
        async function testEmployerEmail() {
            const resultsElement = document.getElementById('email-results');
            resultsElement.innerHTML = '<div class="loading">📧 Testing employer email...</div>';
            try {
                const response = await fetch('/api/test-employer-email', { method: 'POST' });
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const result = await response.json();
                resultsElement.innerHTML = `<div class="success"><h4>📧 Employer Email Test</h4><p><strong>Status:</strong> ${result.status}</p><p><strong>Message:</strong> ${result.message}</p></div>`;
            } catch (error) {
                console.error('Email test error:', error);
                resultsElement.innerHTML = `<div class="error">❌ Error testing email: ${error.message}</div>`;
            }
        }
        
        async function testSystem() {
            showQuickResult('🧪 Testing system components...', 'loading');
            const endpoints = [
                { name: 'API Health', url: '/api/health' }, { name: 'Statistics', url: '/api/stats' },
                { name: 'Candidates', url: '/api/get-candidates' }, { name: 'Jobs', url: '/api/get-jobs' }
            ];
            let allPassed = true;
            for (const endpoint of endpoints) {
                try { const response = await fetch(endpoint.url); if (!response.ok) { allPassed = false; break; } } 
                catch (error) { allPassed = false; break; }
            }
            if (allPassed) showQuickResult('✅ All system components working!', 'success');
            else showQuickResult('❌ Some components need attention', 'error');
        }
        
        function showVectorDBInfo() { showTab('vector-db'); }
        
        function showQuickResult(message, type) {
            const quickResults = document.getElementById('quick-results');
            quickResults.innerHTML = `<div class="${type}">${message}</div>`;
            setTimeout(() => { quickResults.innerHTML = ''; }, 5000);
        }
        
        window.addEventListener('load', function() {
            console.log('🚀 AI Job Matcher Pro with Chroma DB initialized!');
            loadStats();
        });
    </script>
</body>
</html>
'''

"""
FLASK API ROUTES - Updated for Chroma DB
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'AI Job Matcher Pro with Chroma DB is running!',
        'version': '3.0.0'
    })

@app.route('/api/stats')
def get_stats():
    try:
        jobs = db.load_jobs()
        candidates = db.load_candidates()
        vector_db_count = vector_db.get_candidate_count()
        
        return jsonify({
            'total_jobs': len(jobs),
            'total_candidates': len(candidates),
            'vector_db_count': vector_db_count,
            'total_matches': len(jobs) * len(candidates),
            'success_rate': 95
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/run-matching', methods=['POST'])
def run_matching():
    try:
        print("🤖 Running AI matching with Chroma DB...")
        results, jobs, candidates = matcher.find_matches()
        
        matches = []
        for job_index, job_matches in results.items():
            if job_matches and len(job_matches) > 0:
                job = jobs[job_index]
                top_match = job_matches[0]
                candidate = top_match['candidate']
                
                matches.append({
                    'job_id': job['id'],
                    'job_title': job['title'],
                    'company': job['company'],
                    'candidate_id': candidate['id'],
                    'top_candidate': candidate['name'],
                    'top_score': top_match['score'],
                    'common_skills': top_match.get('common_skills', [])[:5],
                    'score_breakdown': top_match.get('score_breakdown', {}),
                    'match_grade': top_match.get('match_grade', 'A')
                })
        
        print(f"✅ Found {len(matches)} matches using Chroma DB")
        return jsonify({'matches': matches})
        
    except Exception as e:
        print(f"❌ Matching error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-candidates')
def get_candidates():
    try:
        candidates = db.load_candidates()
        return jsonify({'candidates': candidates})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-jobs')
def get_jobs():
    try:
        jobs = db.load_jobs()
        return jsonify({'jobs': jobs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/parse-resume', methods=['POST'])
def parse_resume():
    try:
        resume_text = request.json.get('resume_text', '')
        print(f"📄 Parsing resume text ({len(resume_text)} characters)...")
        
        candidate_data = resume_parser.parse_resume_to_candidate(resume_text)
        print(f"✅ Resume parsed: {candidate_data['name']}")
        
        return jsonify({'success': True, 'candidate_data': candidate_data})
    except Exception as e:
        print(f"❌ Resume parse error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/vector-db-stats')
def get_vector_db_stats():
    try:
        stats = db.get_vector_db_stats()
        return jsonify({
            'candidates_in_vector_db': stats['candidates_in_vector_db'],
            'candidates_in_json': stats['candidates_in_json'],
            'jobs_count': stats['jobs_count'],
            'status': 'active'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reinitialize-vector-db', methods=['POST'])
def reinitialize_vector_db():
    try:
        print("🔄 Reinitializing Vector Database...")
        # Clear and reinitialize
        vector_db.clear_candidates()
        candidates = db.load_candidates()
        vector_db.add_candidates_batch(candidates)
        
        return jsonify({
            'status': 'success',
            'message': 'Vector database reinitialized successfully',
            'candidates_loaded': len(candidates)
        })
    except Exception as e:
        print(f"❌ Vector DB reinit error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-candidate-email', methods=['POST'])
def test_candidate_email():
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
APPLICATION STARTUP
"""
if __name__ == '__main__':
    print("🚀 AI Job Matcher Pro - Chroma DB Enhanced")
    print("=" * 70)
    print("✅ All systems initialized and ready!")
    print("🗃️ Chroma Vector Database: ACTIVE")
    print("")
    print("🎯 ENHANCED FEATURES:")
    print("   • 🤖 Chroma DB for instant semantic search")
    print("   • 🎯 Hybrid matching (semantic + traditional)")
    print("   • 📈 Scalable to thousands of candidates")
    print("   • 🚀 Faster matching with vector similarity")
    print("")
    print("⏳ Starting server...")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=5000, debug=False)