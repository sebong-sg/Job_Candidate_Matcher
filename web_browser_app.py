# 🌐 REAL WEB BROWSER INTERFACE - CORRECTED VERSION
# Beautiful web app that runs in your browser!

from flask import Flask, render_template_string, request, jsonify
import sys
import os
import json
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database import DataManager
from matcher import SimpleMatcher
from email_service import EmailService
from resume_parser import ResumeParser

# Create Flask app
app = Flask(__name__)

# Initialize services
db = DataManager()
matcher = SimpleMatcher()
email_service = EmailService()
resume_parser = ResumeParser()

# HTML Template for the web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Job Matcher Pro</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
            margin-bottom: 30px;
        }
        
        .header h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .header p {
            color: #666;
            font-size: 1.2em;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 15px;
        }
        
        .stat-item {
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            margin: 5px;
            transition: transform 0.2s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .btn-secondary {
            background: #6c757d;
        }
        
        .btn-success {
            background: #28a745;
        }
        
        .matches-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
        }
        
        .match-card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
        }
        
        .match-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .match-score {
            background: #28a745;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }
        
        .skills {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 10px 0;
        }
        
        .skill-tag {
            background: #e9ecef;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.9em;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        
        .form-group input, .form-group textarea, .form-group select {
            width: 100%;
            padding: 10px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 1em;
        }
        
        .form-group textarea {
            height: 100px;
            resize: vertical;
        }
        
        .tab-container {
            margin-top: 20px;
        }
        
        .tabs {
            display: flex;
            margin-bottom: 20px;
        }
        
        .tab {
            padding: 12px 25px;
            background: #f8f9fa;
            border: none;
            cursor: pointer;
            margin-right: 5px;
            border-radius: 8px 8px 0 0;
        }
        
        .tab.active {
            background: white;
            font-weight: bold;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .notification {
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .email-preview {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 4px solid #007bff;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 AI Job Matcher Pro</h1>
            <p>Intelligent Recruitment Platform Powered by AI</p>
        </div>
        
        <div class="dashboard">
            <div class="card">
                <h2>📊 Quick Stats</h2>
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-number" id="jobs-count">0</div>
                        <div class="stat-label">Total Jobs</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number" id="candidates-count">0</div>
                        <div class="stat-label">Total Candidates</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number" id="matches-count">0</div>
                        <div class="stat-label">Matches Made</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number" id="success-rate">0%</div>
                        <div class="stat-label">Success Rate</div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>⚡ Quick Actions</h2>
                <div style="margin-top: 20px;">
                    <button class="btn" onclick="runMatching()">🤖 Run AI Matching</button>
                    <button class="btn btn-secondary" onclick="showTab('add-job')">📝 Add New Job</button>
                    <button class="btn btn-secondary" onclick="showTab('add-candidate')">👤 Add Candidate</button>
                    <button class="btn btn-success" onclick="showTab('resume-upload')">📄 Parse Resume</button>
                </div>
            </div>
        </div>
        
        <div class="tab-container">
            <div class="tabs">
                <button class="tab active" onclick="showTab('matches')">🎯 Matches</button>
                <button class="tab" onclick="showTab('add-job')">📋 Jobs</button>
                <button class="tab" onclick="showTab('add-candidate')">👥 Candidates</button>
                <button class="tab" onclick="showTab('resume-upload')">📄 Resume Parser</button>
                <button class="tab" onclick="showTab('email-demo')">📧 Email Demo</button>
                <button class="tab" onclick="showTab('analytics')">📈 Analytics</button>
            </div>
            
            <!-- Matches Tab -->
            <div id="matches" class="tab-content active">
                <div class="card">
                    <h2>🎯 AI-Powered Matches</h2>
                    <div id="matches-results">
                        <p>Click "Run AI Matching" to see results...</p>
                    </div>
                </div>
            </div>
            
            <!-- Add Job Tab -->
            <div id="add-job" class="tab-content">
                <div class="card">
                    <h2>📝 Add New Job</h2>
                    <form onsubmit="addNewJob(event)">
                        <div class="form-group">
                            <label>Job Title</label>
                            <input type="text" id="job-title" required>
                        </div>
                        <div class="form-group">
                            <label>Company</label>
                            <input type="text" id="job-company" required>
                        </div>
                        <div class="form-group">
                            <label>Location</label>
                            <input type="text" id="job-location" required>
                        </div>
                        <div class="form-group">
                            <label>Description</label>
                            <textarea id="job-description" required></textarea>
                        </div>
                        <div class="form-group">
                            <label>Required Skills (comma separated)</label>
                            <input type="text" id="job-skills" placeholder="python, django, aws" required>
                        </div>
                        <button type="submit" class="btn">Add Job</button>
                    </form>
                </div>
            </div>
            
            <!-- Resume Parser Tab -->
            <div id="resume-upload" class="tab-content">
                <div class="card">
                    <h2>📄 AI Resume Parser</h2>
                    <div class="form-group">
                        <label>Paste Resume Text</label>
                        <textarea id="resume-text" placeholder="Paste resume content here..." style="height: 200px;"></textarea>
                    </div>
                    <button class="btn" onclick="parseResume()">Parse Resume</button>
                    
                    <div id="resume-results" style="margin-top: 20px;"></div>
                </div>
            </div>
            
            <!-- Email Demo Tab -->
            <div id="email-demo" class="tab-content">
                <div class="card">
                    <h2>📧 Email Notification Demo</h2>
                    <p>Test the email notification system (runs in test mode - no real emails sent)</p>
                    
                    <div style="margin: 20px 0;">
                        <button class="btn" onclick="testCandidateEmail()">Test Candidate Email</button>
                        <button class="btn btn-success" onclick="testEmployerEmail()">Test Employer Email</button>
                    </div>
                    
                    <div id="email-results"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            
            // Update tab buttons
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
        }
        
        async function runMatching() {
            const response = await fetch('/api/run-matching');
            const data = await response.json();
            
            let matchesHtml = '<h3>🤖 Matching Results</h3>';
            
            data.matches.forEach(match => {
                matchesHtml += `
                    <div class="match-card">
                        <div class="match-header">
                            <h3>${match.job_title} at ${match.company}</h3>
                            <span class="match-score">${(match.top_score * 100).toFixed(1)}% Match</span>
                        </div>
                        <p><strong>Top Candidate:</strong> ${match.top_candidate}</p>
                        <p><strong>Common Skills:</strong> ${match.common_skills.join(', ')}</p>
                        <button class="btn btn-success" onclick="sendNotification(${match.job_id}, ${match.candidate_id})">
                            📧 Send Notification
                        </button>
                    </div>
                `;
            });
            
            document.getElementById('matches-results').innerHTML = matchesHtml;
            updateStats(data.stats);
        }
        
        async function addNewJob(event) {
            event.preventDefault();
            
            const jobData = {
                title: document.getElementById('job-title').value,
                company: document.getElementById('job-company').value,
                location: document.getElementById('job-location').value,
                description: document.getElementById('job-description').value,
                skills: document.getElementById('job-skills').value.split(',').map(s => s.trim())
            };
            
            const response = await fetch('/api/add-job', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(jobData)
            });
            
            const result = await response.json();
            alert(result.message);
        }
        
        async function parseResume() {
            const resumeText = document.getElementById('resume-text').value;
            
            if (!resumeText) {
                alert('Please paste some resume text first!');
                return;
            }
            
            const response = await fetch('/api/parse-resume', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({resume_text: resumeText})
            });
            
            const result = await response.json();
            
            let resultsHtml = `
                <div class="notification">
                    <strong>✅ Resume Parsed Successfully!</strong>
                </div>
                <div class="match-card">
                    <h3>👤 ${result.candidate_data.name}</h3>
                    <p><strong>Email:</strong> ${result.candidate_data.email}</p>
                    <p><strong>Phone:</strong> ${result.candidate_data.phone}</p>
                    <p><strong>Experience:</strong> ${result.candidate_data.experience_years} years</p>
                    <p><strong>Education:</strong> ${result.candidate_data.education}</p>
                    <p><strong>Summary:</strong> ${result.candidate_data.profile}</p>
                    <div class="skills">
                        ${result.candidate_data.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                    </div>
                    <button class="btn" onclick="addParsedCandidate()">Add to Database</button>
                </div>
            `;
            
            document.getElementById('resume-results').innerHTML = resultsHtml;
        }
        
        async function testCandidateEmail() {
            const response = await fetch('/api/test-candidate-email');
            const result = await response.json();
            
            document.getElementById('email-results').innerHTML = `
                <div class="email-preview">
                    <h4>📧 Candidate Email Test</h4>
                    <p><strong>Status:</strong> ${result.status}</p>
                    <p><strong>Message:</strong> ${result.message}</p>
                    <p><em>Check your terminal/console for the full email preview</em></p>
                </div>
            `;
        }
        
        async function testEmployerEmail() {
            const response = await fetch('/api/test-employer-email');
            const result = await response.json();
            
            document.getElementById('email-results').innerHTML = `
                <div class="email-preview">
                    <h4>📧 Employer Email Test</h4>
                    <p><strong>Status:</strong> ${result.status}</p>
                    <p><strong>Message:</strong> ${result.message}</p>
                    <p><em>Check your terminal/console for the full email preview</em></p>
                </div>
            `;
        }
        
        function updateStats(stats) {
            document.getElementById('jobs-count').textContent = stats.total_jobs;
            document.getElementById('candidates-count').textContent = stats.total_candidates;
            document.getElementById('matches-count').textContent = stats.total_matches;
            document.getElementById('success-rate').textContent = stats.success_rate + '%';
        }
        
        // Load initial stats
        fetch('/api/stats').then(r => r.json()).then(updateStats);
    </script>
</body>
</html>
'''

# Flask Routes
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stats')
def get_stats():
    jobs = db.load_jobs()
    candidates = db.load_candidates()
    
    return jsonify({
        'total_jobs': len(jobs),
        'total_candidates': len(candidates),
        'total_matches': len(jobs) * len(candidates),  # Simplified
        'success_rate': 95  # Placeholder
    })

@app.route('/api/run-matching', methods=['POST'])
def run_matching():
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
                'common_skills': top_match['common_skills'][:5]
            })
    
    return jsonify({
        'matches': matches,
        'stats': {
            'total_jobs': len(jobs),
            'total_candidates': len(candidates),
            'total_matches': len(matches),
            'success_rate': 95
        }
    })

@app.route('/api/add-job', methods=['POST'])
def add_job():
    job_data = request.json
    job_id = db.add_job(job_data)
    
    return jsonify({
        'success': job_id is not None,
        'message': f"Job '{job_data['title']}' added successfully!" if job_id else "Failed to add job"
    })

@app.route('/api/parse-resume', methods=['POST'])
def parse_resume():
    resume_text = request.json.get('resume_text', '')
    candidate_data = resume_parser.parse_resume_to_candidate(resume_text)
    
    return jsonify({
        'success': True,
        'candidate_data': candidate_data
    })

@app.route('/api/test-candidate-email', methods=['POST'])
def test_candidate_email():
    try:
        # Test candidate email
        email_service.send_candidate_match_notification(
            candidate_email="test.candidate@example.com",
            candidate_name="Test Candidate",
            job_title="Senior Python Developer", 
            company="TechCorp Inc",
            match_score=0.85
        )
        return jsonify({
            'status': 'success',
            'message': 'Candidate email test completed! Check terminal for preview.'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed: {str(e)}'
        })

@app.route('/api/test-employer-email', methods=['POST'])
def test_employer_email():
    try:
        # Test employer email
        email_service.send_employer_match_notification(
            employer_email="hr@techcorp.com",
            job_title="Python Developer",
            top_candidates=[
                {
                    'name': 'John Smith',
                    'score': 0.85,
                    'skills': ['Python', 'Django', 'Flask'],
                    'experience_years': 5
                },
                {
                    'name': 'Sarah Johnson', 
                    'score': 0.78,
                    'skills': ['Python', 'Machine Learning'],
                    'experience_years': 4
                }
            ]
        )
        return jsonify({
            'status': 'success', 
            'message': 'Employer email test completed! Check terminal for preview.'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed: {str(e)}'
        })

if __name__ == '__main__':
    print("🌐 Starting AI Job Matcher Web Server...")
    print("📍 Open your browser and go to: http://localhost:5000")
    print("📧 Email service is running in TEST MODE - no real emails sent")
    print("🛑 Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)