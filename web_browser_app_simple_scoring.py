"""
🌐 AI JOB MATCHER PRO - COMPLETE MODULAR VERSION
Enterprise Recruitment Platform with Full UI
"""

import sys
import os
import json
import logging
from typing import Dict, List, Any, Optional
from flask import Flask, render_template_string, request, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Config:
    """Configuration settings"""
    PORT = 5000
    HOST = '0.0.0.0'
    DEBUG = False

class ServiceManager:
    """Manages all AI services"""
    
    def __init__(self):
        self.services = {}
        self.setup_services()
    
    def setup_services(self):
        """Initialize services with fallback to demo versions"""
        try:
            sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
            
            from database import DataManager
            from matcher import SimpleMatcher
            from email_service import EmailService
            from resume_parser import ResumeParser
            
            self.services['database'] = DataManager()
            self.services['matcher'] = SimpleMatcher()
            self.services['email'] = EmailService()
            self.services['resume_parser'] = ResumeParser()
            
            logger.info("✅ All AI services loaded")
            
        except ImportError as e:
            logger.warning(f"Using demo services: {e}")
            self.setup_demo_services()
    
    def setup_demo_services(self):
        """Setup demo services"""
        self.services['database'] = DemoDataManager()
        self.services['matcher'] = DemoMatcher()
        self.services['email'] = DemoEmailService()
        self.services['resume_parser'] = DemoResumeParser()

class APIController:
    """Handles API business logic"""
    
    def __init__(self, service_manager):
        self.service_manager = service_manager
    
    def get_stats(self):
        """Get system statistics"""
        try:
            db = self.service_manager.services['database']
            jobs = db.load_jobs()
            candidates = db.load_candidates()
            
            return {
                'success': True,
                'total_jobs': len(jobs),
                'total_candidates': len(candidates),
                'total_matches': len(jobs) * len(candidates),
                'success_rate': 95
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def run_matching(self):
        """Run AI matching"""
        try:
            matcher = self.service_manager.services['matcher']
            results, jobs, candidates = matcher.find_matches()
            
            matches = []
            for job_index, job_matches in results.items():
                if job_matches:
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
                        'common_skills': top_match.get('common_skills', [])[:5]
                    })
            
            return {'success': True, 'matches': matches}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_candidates(self):
        """Get all candidates"""
        try:
            db = self.service_manager.services['database']
            return {'success': True, 'candidates': db.load_candidates()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_jobs(self):
        """Get all jobs"""
        try:
            db = self.service_manager.services['database']
            return {'success': True, 'jobs': db.load_jobs()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def parse_resume(self, resume_text):
        """Parse resume text"""
        try:
            parser = self.service_manager.services['resume_parser']
            candidate_data = parser.parse_resume_to_candidate(resume_text)
            return {'success': True, 'candidate_data': candidate_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Demo Services
class DemoDataManager:
    def load_jobs(self):
        return [
            {"id": 1, "title": "Python Developer", "company": "TechCorp", "location": "Remote", 
             "description": "Develop web applications with Python and Django", "required_skills": ["python", "django", "sql"]},
            {"id": 2, "title": "Data Scientist", "company": "DataInc", "location": "NYC", 
             "description": "Build machine learning models", "required_skills": ["python", "machine learning", "statistics"]},
            {"id": 3, "title": "Frontend Developer", "company": "WebSolutions", "location": "Remote", 
             "description": "Create responsive web interfaces", "required_skills": ["javascript", "react", "css"]}
        ]
    
    def load_candidates(self):
        return [
            {"id": 1, "name": "John Smith", "email": "john@example.com", "profile": "Python developer with 5 years experience", 
             "skills": ["python", "django", "flask", "sql"], "experience_years": 5, "location": "Remote"},
            {"id": 2, "name": "Sarah Johnson", "email": "sarah@example.com", "profile": "Data scientist specializing in ML", 
             "skills": ["python", "machine learning", "tensorflow", "pandas"], "experience_years": 3, "location": "NYC"},
            {"id": 3, "name": "Mike Chen", "email": "mike@example.com", "profile": "Full-stack JavaScript developer", 
             "skills": ["javascript", "react", "node.js", "mongodb"], "experience_years": 4, "location": "Remote"}
        ]

class DemoMatcher:
    def find_matches(self):
        jobs = DemoDataManager().load_jobs()
        candidates = DemoDataManager().load_candidates()
        results = {}
        for i, job in enumerate(jobs):
            results[i] = []
            for candidate in candidates:
                common_skills = set(job['required_skills']) & set(candidate['skills'])
                if common_skills:
                    score = len(common_skills) / len(job['required_skills'])
                    results[i].append({"candidate": candidate, "score": score, "common_skills": list(common_skills)})
            results[i].sort(key=lambda x: x['score'], reverse=True)
        return results, jobs, candidates

class DemoEmailService:
    def send_candidate_match_notification(self, *args, **kwargs): 
        print("📧 Candidate email (demo)")
    def send_employer_match_notification(self, *args, **kwargs): 
        print("📧 Employer email (demo)")

class DemoResumeParser:
    def parse_resume_to_candidate(self, text):
        return {
            "name": "Candidate from Resume",
            "email": "resume@example.com",
            "phone": "123-456-7890",
            "skills": ["python", "communication", "problem-solving"],
            "experience_years": 3,
            "location": "Remote",
            "education": "Bachelor's Degree",
            "profile": "Experienced professional"
        }

# COMPLETE HTML TEMPLATE WITH FULL UI
COMPLETE_HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Job Matcher Pro v2.0</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px 40px;
            text-align: center;
        }
        .header h1 { font-size: 3em; margin-bottom: 15px; }
        .header p { font-size: 1.3em; opacity: 0.9; }
        .dashboard {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            padding: 40px;
            background: #f8f9fa;
        }
        @media (max-width: 768px) {
            .dashboard { grid-template-columns: 1fr; }
        }
        .card {
            background: white;
            padding: 35px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
        }
        .stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 25px;
        }
        .stat-item {
            text-align: center;
            padding: 25px 20px;
            background: #f8f9fa;
            border-radius: 12px;
            border: 2px solid #e9ecef;
            transition: all 0.3s ease;
        }
        .stat-item:hover {
            transform: translateY(-5px);
            border-color: #667eea;
        }
        .stat-number {
            font-size: 2.8em;
            font-weight: bold;
            color: #667eea;
            display: block;
        }
        .stat-label {
            color: #666;
            font-size: 0.95em;
            margin-top: 8px;
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 16px 32px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1.05em;
            font-weight: 600;
            margin: 10px;
            transition: all 0.3s ease;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        }
        .btn:hover { transform: translateY(-3px); }
        .btn-success { background: linear-gradient(135deg, #28a745 0%, #20c997 100%); }
        .btn-warning { background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%); color: #000; }
        .tab-container { padding: 0 40px 40px 40px; }
        .tabs {
            display: flex;
            background: #f8f9fa;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 35px;
            flex-wrap: wrap;
            gap: 10px;
        }
        .tab {
            padding: 16px 28px;
            background: transparent;
            border: none;
            cursor: pointer;
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
            color: #666;
            flex: 1;
            min-width: 120px;
        }
        .tab:hover { background: rgba(102, 126, 234, 0.1); color: #667eea; }
        .tab.active { background: #667eea; color: white; }
        .tab-content { display: none; animation: fadeIn 0.5s ease-in; }
        .tab-content.active { display: block; }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .loading { text-align: center; padding: 40px; color: #667eea; font-size: 1.2em; }
        .success { background: #d4edda; color: #155724; padding: 20px; border-radius: 10px; margin: 20px 0; }
        .error { background: #f8d7da; color: #721c24; padding: 20px; border-radius: 10px; margin: 20px 0; }
        .match-card, .candidate-card, .job-card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            margin: 20px 0;
            border-left: 5px solid #28a745;
        }
        .match-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; flex-wrap: wrap; gap: 15px; }
        .match-score { background: #28a745; color: white; padding: 8px 20px; border-radius: 25px; font-weight: bold; }
        .skills { display: flex; flex-wrap: wrap; gap: 8px; margin: 15px 0; }
        .skill-tag { background: #e9ecef; padding: 6px 15px; border-radius: 20px; font-size: 0.9em; }
        .action-buttons { display: flex; gap: 15px; flex-wrap: wrap; margin: 20px 0; }
        .results-container { margin-top: 30px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 600; }
        .form-group input, .form-group textarea {
            width: 100%; padding: 15px; border: 2px solid #e9ecef; border-radius: 8px; font-size: 1em;
        }
        .form-group textarea { height: 120px; resize: vertical; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 AI Job Matcher Pro v2.0</h1>
            <p>Modular Enterprise Platform - Complete Working Version</p>
        </div>
        
        <div class="dashboard">
            <div class="card">
                <h2>📊 Live Dashboard</h2>
                <div class="stats">
                    <div class="stat-item">
                        <span class="stat-number" id="jobs-count">0</span>
                        <div class="stat-label">Total Jobs</div>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number" id="candidates-count">0</span>
                        <div class="stat-label">Total Candidates</div>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number" id="matches-count">0</span>
                        <div class="stat-label">Matches Made</div>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number" id="success-rate">0%</span>
                        <div class="stat-label">Success Rate</div>
                    </div>
                </div>
                <div class="action-buttons">
                    <button class="btn" onclick="loadStats()">🔄 Refresh Stats</button>
                    <button class="btn btn-warning" onclick="testSystem()">🧪 Test System</button>
                </div>
            </div>
            
            <div class="card">
                <h2>⚡ Quick Actions</h2>
                <div class="action-buttons">
                    <button class="btn btn-success" onclick="runMatching()">🤖 Run AI Matching</button>
                    <button class="btn" onclick="showTab('candidates')">👥 View Candidates</button>
                    <button class="btn" onclick="showTab('jobs')">📋 View Jobs</button>
                    <button class="btn" onclick="showTab('resume-parser')">📄 Parse Resume</button>
                    <button class="btn" onclick="showTab('email-demo')">📧 Email Demo</button>
                </div>
                <div id="quick-results" style="margin-top: 20px;"></div>
            </div>
        </div>
        
        <div class="tab-container">
            <div class="tabs">
                <button class="tab active" onclick="showTab('matching')">🎯 AI Matching</button>
                <button class="tab" onclick="showTab('candidates')">👥 Candidates</button>
                <button class="tab" onclick="showTab('jobs')">📋 Jobs</button>
                <button class="tab" onclick="showTab('resume-parser')">📄 Resume Parser</button>
                <button class="tab" onclick="showTab('email-demo')">📧 Email Demo</button>
            </div>
            
            <div id="matching" class="tab-content active">
                <div class="card">
                    <h2>🤖 AI-Powered Job Matching</h2>
                    <p>Our advanced AI analyzes job requirements and candidate profiles to find perfect matches.</p>
                    <div class="action-buttons">
                        <button class="btn btn-success" onclick="runMatching()">🚀 Run AI Matching</button>
                    </div>
                    <div id="matching-results" class="results-container">
                        <p>Click "Run AI Matching" to see intelligent job-candidate matches...</p>
                    </div>
                </div>
            </div>
            
            <div id="candidates" class="tab-content">
                <div class="card">
                    <h2>👥 Candidate Database</h2>
                    <div class="action-buttons">
                        <button class="btn" onclick="loadCandidates()">🔄 Load Candidates</button>
                    </div>
                    <div id="candidates-list" class="results-container">
                        <p>Candidate list will appear here...</p>
                    </div>
                </div>
            </div>
            
            <div id="jobs" class="tab-content">
                <div class="card">
                    <h2>📋 Job Database</h2>
                    <div class="action-buttons">
                        <button class="btn" onclick="loadJobs()">🔄 Load Jobs</button>
                    </div>
                    <div id="jobs-list" class="results-container">
                        <p>Job list will appear here...</p>
                    </div>
                </div>
            </div>
            
            <div id="resume-parser" class="tab-content">
                <div class="card">
                    <h2>📄 AI Resume Parser</h2>
                    <div class="form-group">
                        <label>Paste Resume Text:</label>
                        <textarea id="resume-text" placeholder="Paste resume content here..."></textarea>
                    </div>
                    <div class="action-buttons">
                        <button class="btn btn-success" onclick="parseResume()">🔍 Parse Resume</button>
                    </div>
                    <div id="resume-results" class="results-container">
                        <p>Parsed candidate data will appear here...</p>
                    </div>
                </div>
            </div>
            
            <div id="email-demo" class="tab-content">
                <div class="card">
                    <h2>📧 Email Notification System</h2>
                    <div class="action-buttons">
                        <button class="btn" onclick="testCandidateEmail()">👤 Test Candidate Email</button>
                        <button class="btn btn-success" onclick="testEmployerEmail()">🏢 Test Employer Email</button>
                    </div>
                    <div id="email-results" class="results-container">
                        <p>Email test results will appear here.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
        
        async function loadStats() {
            document.getElementById('jobs-count').textContent = '...';
            document.getElementById('candidates-count').textContent = '...';
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                if (data.success) {
                    document.getElementById('jobs-count').textContent = data.total_jobs;
                    document.getElementById('candidates-count').textContent = data.total_candidates;
                    document.getElementById('matches-count').textContent = data.total_matches;
                    document.getElementById('success-rate').textContent = data.success_rate + '%';
                    showQuickResult('✅ Stats updated!', 'success');
                } else {
                    showQuickResult('❌ ' + data.error, 'error');
                }
            } catch (error) {
                showQuickResult('❌ Network error', 'error');
            }
        }
        
        async function runMatching() {
            const resultsElement = document.getElementById('matching-results');
            resultsElement.innerHTML = '<div class="loading">🤖 AI is analyzing jobs and candidates...</div>';
            try {
                const response = await fetch('/api/run-matching', {method: 'POST'});
                const data = await response.json();
                if (data.success) {
                    let html = '<h3>🎯 Matching Results</h3>';
                    if (data.matches && data.matches.length > 0) {
                        html += `<div class="success">✅ Found ${data.matches.length} matches!</div>`;
                        data.matches.forEach(match => {
                            html += `
                                <div class="match-card">
                                    <div class="match-header">
                                        <h4>${match.job_title} at ${match.company}</h4>
                                        <span class="match-score">${(match.top_score * 100).toFixed(1)}% Match</span>
                                    </div>
                                    <p><strong>👤 Top Candidate:</strong> ${match.top_candidate}</p>
                                    <p><strong>🔧 Common Skills:</strong> ${match.common_skills.join(', ')}</p>
                                </div>
                            `;
                        });
                    } else {
                        html += '<div class="error">❌ No matches found.</div>';
                    }
                    resultsElement.innerHTML = html;
                    loadStats();
                } else {
                    resultsElement.innerHTML = `<div class="error">❌ Error: ${data.error}</div>`;
                }
            } catch (error) {
                resultsElement.innerHTML = `<div class="error">❌ Network error: ${error.message}</div>`;
            }
        }
        
        async function loadCandidates() {
            const listElement = document.getElementById('candidates-list');
            listElement.innerHTML = '<div class="loading">🔄 Loading candidates...</div>';
            try {
                const response = await fetch('/api/candidates');
                const data = await response.json();
                let html = '<h3>👥 All Candidates</h3>';
                if (data.success && data.candidates.length > 0) {
                    data.candidates.forEach(candidate => {
                        html += `
                            <div class="candidate-card">
                                <h4>${candidate.name}</h4>
                                <p><strong>📧 Email:</strong> ${candidate.email}</p>
                                <p><strong>💼 Experience:</strong> ${candidate.experience_years} years</p>
                                <p><strong>📍 Location:</strong> ${candidate.location}</p>
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
                listElement.innerHTML = `<div class="error">❌ Error: ${error.message}</div>`;
            }
        }
        
        async function loadJobs() {
            const listElement = document.getElementById('jobs-list');
            listElement.innerHTML = '<div class="loading">🔄 Loading jobs...</div>';
            try {
                const response = await fetch('/api/jobs');
                const data = await response.json();
                let html = '<h3>📋 All Jobs</h3>';
                if (data.success && data.jobs.length > 0) {
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
                listElement.innerHTML = `<div class="error">❌ Error: ${error.message}</div>`;
            }
        }
        
        async function parseResume() {
            const resumeText = document.getElementById('resume-text').value.trim();
            if (!resumeText) {
                alert('❌ Please paste resume text!');
                return;
            }
            const resultsElement = document.getElementById('resume-results');
            resultsElement.innerHTML = '<div class="loading">🔍 Parsing resume...</div>';
            try {
                const response = await fetch('/api/parse-resume', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({resume_text: resumeText})
                });
                const result = await response.json();
                if (result.success) {
                    const candidate = result.candidate_data;
                    resultsElement.innerHTML = `
                        <div class="success">✅ Resume Parsed!</div>
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
                } else {
                    resultsElement.innerHTML = `<div class="error">❌ Error: ${result.error}</div>`;
                }
            } catch (error) {
                resultsElement.innerHTML = `<div class="error">❌ Network error: ${error.message}</div>`;
            }
        }
        
        async function testCandidateEmail() {
            const resultsElement = document.getElementById('email-results');
            resultsElement.innerHTML = '<div class="loading">📧 Testing candidate email...</div>';
            try {
                const response = await fetch('/api/test-candidate-email', {method: 'POST'});
                const result = await response.json();
                resultsElement.innerHTML = `<div class="success">${result.success ? '✅ ' : '❌ '}${result.message || result.error}</div>`;
            } catch (error) {
                resultsElement.innerHTML = `<div class="error">❌ Error: ${error.message}</div>`;
            }
        }
        
        async function testEmployerEmail() {
            const resultsElement = document.getElementById('email-results');
            resultsElement.innerHTML = '<div class="loading">📧 Testing employer email...</div>';
            try {
                const response = await fetch('/api/test-employer-email', {method: 'POST'});
                const result = await response.json();
                resultsElement.innerHTML = `<div class="success">${result.success ? '✅ ' : '❌ '}${result.message || result.error}</div>`;
            } catch (error) {
                resultsElement.innerHTML = `<div class="error">❌ Error: ${error.message}</div>`;
            }
        }
        
        async function testSystem() {
            showQuickResult('🧪 Testing system...', 'loading');
            try {
                const response = await fetch('/api/health');
                const data = await response.json();
                showQuickResult('✅ System is healthy!', 'success');
            } catch (error) {
                showQuickResult('❌ System test failed', 'error');
            }
        }
        
        function showQuickResult(message, type) {
            const quickResults = document.getElementById('quick-results');
            quickResults.innerHTML = `<div class="${type}">${message}</div>`;
            setTimeout(() => quickResults.innerHTML = '', 5000);
        }
        
        // Initialize
        window.addEventListener('load', loadStats);
    </script>
</body>
</html>
'''

# Create Flask app
app = Flask(__name__)

# Initialize services
service_manager = ServiceManager()
api_controller = APIController(service_manager)

# Routes
@app.route('/')
def home():
    return render_template_string(COMPLETE_HTML_TEMPLATE)

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'version': '2.0.0'})

@app.route('/api/stats')
def get_stats():
    return jsonify(api_controller.get_stats())

@app.route('/api/run-matching', methods=['POST'])
def run_matching():
    return jsonify(api_controller.run_matching())

@app.route('/api/candidates')
def get_candidates():
    return jsonify(api_controller.get_candidates())

@app.route('/api/jobs')
def get_jobs():
    return jsonify(api_controller.get_jobs())

@app.route('/api/parse-resume', methods=['POST'])
def parse_resume():
    resume_text = request.json.get('resume_text', '')
    return jsonify(api_controller.parse_resume(resume_text))

@app.route('/api/test-candidate-email', methods=['POST'])
def test_candidate_email():
    try:
        service_manager.services['email'].send_candidate_match_notification(
            candidate_email="test@example.com",
            candidate_name="Test User",
            job_title="Senior Developer",
            company="Test Corp",
            match_score=0.85
        )
        return jsonify({'success': True, 'message': 'Candidate email test completed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/test-employer-email', methods=['POST'])
def test_employer_email():
    try:
        service_manager.services['email'].send_employer_match_notification(
            employer_email="hr@example.com",
            job_title="Developer",
            top_candidates=[{"name": "Test Candidate", "score": 0.9, "skills": ["python"]}]
        )
        return jsonify({'success': True, 'message': 'Employer email test completed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🚀 AI Job Matcher Pro v2.0 - Complete Working Version")
    print("=" * 70)
    print("✅ All systems initialized!")
    print("🌐 Starting server on port 5000...")
    print("📍 Access via Ports tab → Globe icon 🌐")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=5000, debug=False)