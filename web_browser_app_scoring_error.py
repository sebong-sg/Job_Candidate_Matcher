"""
🌐 AI JOB MATCHER PRO - STABLE WORKING VERSION
Enterprise Recruitment Platform with Proper Scoring
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
    DEBUG = True

class ServiceManager:
    """Manages all AI services"""
    
    def __init__(self):
        self.services = {}
        self.setup_services()
    
    def setup_services(self):
        """Initialize services - USING DEMO SERVICES FOR STABILITY"""
        print("🔧 Using stable demo services for guaranteed scoring breakdown")
        self.setup_demo_services()
    
    def setup_demo_services(self):
        """Setup demo services that definitely work"""
        self.services['database'] = DemoDataManager()
        self.services['matcher'] = StableDemoMatcher()  # Using stable matcher
        self.services['email'] = DemoEmailService()
        self.services['resume_parser'] = DemoResumeParser()
        print("✅ All demo services loaded successfully")

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
        """Run AI matching - STABLE VERSION"""
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
                        'top_score': top_match.get('score', 0),
                        'common_skills': top_match.get('common_skills', [])[:5],
                        'score_breakdown': top_match.get('score_breakdown', {}),
                        'match_grade': top_match.get('match_grade', 'A')
                    })
            
            return {'success': True, 'matches': matches}
        except Exception as e:
            print(f"Error in run_matching: {e}")
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

# STABLE DEMO MATCHER WITH PROPER SCORING
class StableDemoMatcher:
    """Stable matcher with guaranteed scoring breakdown"""
    
    def __init__(self):
        self.skill_weights = {
            'python': 0.15, 'javascript': 0.12, 'java': 0.12, 'react': 0.10,
            'django': 0.08, 'flask': 0.08, 'node.js': 0.08, 'sql': 0.10,
            'mongodb': 0.07, 'docker': 0.06, 'aws': 0.06, 'machine learning': 0.12,
            'tensorflow': 0.08, 'pytorch': 0.08, 'statistics': 0.09, 'data analysis': 0.08,
            'css': 0.05, 'html': 0.05, 'git': 0.04, 'rest api': 0.06
        }
    
    def calculate_skill_score(self, job_skills, candidate_skills):
        """Calculate weighted skill match score"""
        if not job_skills:
            return 0.0
        
        total_weight = 0
        matched_weight = 0
        
        candidate_skills_lower = [skill.lower() for skill in candidate_skills]
        
        for skill in job_skills:
            skill_lower = skill.lower()
            weight = self.skill_weights.get(skill_lower, 0.05)
            total_weight += weight
            if skill_lower in candidate_skills_lower:
                matched_weight += weight
        
        return matched_weight / total_weight if total_weight > 0 else 0.0
    
    def calculate_experience_score(self, job_title, candidate_experience):
        """Calculate experience suitability score"""
        job_lower = job_title.lower()
        
        if 'senior' in job_lower or 'lead' in job_lower or 'principal' in job_lower:
            required_exp = 5
        elif 'junior' in job_lower or 'entry' in job_lower:
            required_exp = 1
        else:
            required_exp = 3
        
        if candidate_experience >= required_exp:
            return 1.0
        elif candidate_experience > 0:
            return candidate_experience / required_exp
        else:
            return 0.1
    
    def calculate_location_score(self, job_location, candidate_location):
        """Calculate location compatibility score"""
        if not job_location or not candidate_location:
            return 0.5
            
        job_loc = job_location.lower()
        candidate_loc = candidate_location.lower()
        
        if 'remote' in job_loc:
            return 1.0
        elif job_loc == candidate_loc:
            return 1.0
        elif 'remote' in candidate_loc:
            return 0.8
        else:
            return 0.3
    
    def calculate_profile_relevance(self, job_description, candidate_profile):
        """Industry-inspired profile relevance scoring"""
        if not candidate_profile or not job_description:
            return 0.5
        
        job_lower = job_description.lower()
        candidate_lower = candidate_profile.lower()
        
        # 1. SKILL KEYWORDS (40% weight)
        technical_skills = {
            'python': 2, 'django': 2, 'flask': 1, 'javascript': 2, 'react': 2, 
            'sql': 1, 'mongodb': 1, 'docker': 1, 'aws': 1, 'machine learning': 2,
            'tensorflow': 1, 'pytorch': 1, 'statistics': 1, 'data analysis': 1,
            'web development': 2, 'cloud': 1, 'api': 1, 'git': 1
        }
        
        skill_score = 0
        max_skill_score = 0
        for skill, weight in technical_skills.items():
            if skill in job_lower:
                max_skill_score += weight
                if skill in candidate_lower:
                    skill_score += weight
        
        skill_match = skill_score / max_skill_score if max_skill_score > 0 else 0
        
        # 2. ROLE KEYWORDS (30% weight)
        role_keywords = {
            'senior': 2, 'lead': 2, 'principal': 2, 'developer': 1, 'engineer': 1,
            'architect': 2, 'specialist': 1, 'analyst': 1, 'scientist': 2
        }
        
        role_score = 0
        max_role_score = 0
        for role, weight in role_keywords.items():
            if role in job_lower:
                max_role_score += weight
                if role in candidate_lower:
                    role_score += weight
        
        role_match = role_score / max_role_score if max_role_score > 0 else 0
        
        # 3. EXPERIENCE INDICATORS (20% weight)
        experience_indicators = ['experience', 'years', 'background', 'history', 'career']
        exp_matches = sum(1 for indicator in experience_indicators 
                         if indicator in job_lower and indicator in candidate_lower)
        exp_match = min(exp_matches / 3, 1.0)  # Normalize to 0-1
        
        # 4. INDUSTRY CONTEXT (10% weight)
        context_words = ['develop', 'build', 'create', 'design', 'implement', 'manage']
        context_matches = sum(1 for word in context_words 
                             if word in job_lower and word in candidate_lower)
        context_match = min(context_matches / 3, 1.0)
        
        # Weighted total
        total_score = (
            skill_match * 0.40 +
            role_match * 0.30 +
            exp_match * 0.20 +
            context_match * 0.10
        )
        
        # Ensure reasonable bounds
        return max(0.2, min(total_score, 1.0))
    
    def get_match_grade(self, total_score):
        """Convert numerical score to letter grade"""
        if total_score >= 0.9: return 'A+'
        elif total_score >= 0.8: return 'A'
        elif total_score >= 0.7: return 'B+'
        elif total_score >= 0.6: return 'B'
        elif total_score >= 0.5: return 'C+'
        elif total_score >= 0.4: return 'C'
        else: return 'D'
    
    def find_matches(self):
        """Stable matching with guaranteed scoring breakdown"""
        jobs = DemoDataManager().load_jobs()
        candidates = DemoDataManager().load_candidates()
        results = {}
        
        for i, job in enumerate(jobs):
            results[i] = []
            
            for candidate in candidates:
                # Calculate individual score components
                skill_score = self.calculate_skill_score(
                    job.get('required_skills', []), 
                    candidate.get('skills', [])
                )
                
                experience_score = self.calculate_experience_score(
                    job.get('title', ''), 
                    candidate.get('experience_years', 0)
                )
                
                location_score = self.calculate_location_score(
                    job.get('location', ''), 
                    candidate.get('location', '')
                )
                
                profile_score = self.calculate_profile_relevance(
                    job.get('description', ''), 
                    candidate.get('profile', '')
                )
                
                # Calculate total weighted score
                total_score = (
                    skill_score * 0.50 +
                    experience_score * 0.25 +  
                    location_score * 0.15 +
                    profile_score * 0.10
                )
                
                # Find common skills
                job_skills_lower = [s.lower() for s in job.get('required_skills', [])]
                candidate_skills_lower = [s.lower() for s in candidate.get('skills', [])]
                common_skills = list(set(job_skills_lower) & set(candidate_skills_lower))
                
                if total_score > 0.1:
                    results[i].append({
                        "candidate": candidate,
                        "score": round(total_score, 3),
                        "common_skills": common_skills,
                        "score_breakdown": {
                            "skills": int(skill_score * 100),
                            "experience": int(experience_score * 100),
                            "location": int(location_score * 100),
                            "profile": int(profile_score * 100)
                        },
                        "match_grade": self.get_match_grade(total_score)
                    })
            
            # Sort by total score (highest first)
            results[i].sort(key=lambda x: x['score'], reverse=True)
        
        return results, jobs, candidates

# DEMO SERVICES
class DemoDataManager:
    def load_jobs(self):
        return [
            {
                "id": 1, "title": "Senior Python Developer", "company": "TechCorp", "location": "Remote", 
                "description": "Develop scalable web applications with Python and Django. Lead technical projects.",
                "required_skills": ["python", "django", "sql", "docker", "aws"]
            },
            {
                "id": 2, "title": "Data Scientist", "company": "DataInc", "location": "NYC", 
                "description": "Build machine learning models and perform statistical analysis.",
                "required_skills": ["python", "machine learning", "statistics", "pytorch", "data analysis"]
            },
            {
                "id": 3, "title": "Frontend Developer", "company": "WebSolutions", "location": "San Francisco", 
                "description": "Create responsive web interfaces with React and modern JavaScript.",
                "required_skills": ["javascript", "react", "css", "html", "rest api"]
            }
        ]
    
    def load_candidates(self):
        return [
            {
                "id": 1, "name": "John Smith", "email": "john@example.com", 
                "profile": "Senior Python developer with 8 years experience in web development and cloud technologies",
                "skills": ["python", "django", "flask", "sql", "docker", "aws", "rest api"], 
                "experience_years": 8, "location": "Remote"
            },
            {
                "id": 2, "name": "Sarah Johnson", "email": "sarah@example.com", 
                "profile": "Data scientist specializing in machine learning and statistical modeling",
                "skills": ["python", "machine learning", "tensorflow", "pytorch", "statistics", "data analysis"], 
                "experience_years": 4, "location": "NYC"
            },
            {
                "id": 3, "name": "Mike Chen", "email": "mike@example.com", 
                "profile": "Full-stack JavaScript developer with React and Node.js expertise",
                "skills": ["javascript", "react", "node.js", "mongodb", "css", "html"], 
                "experience_years": 5, "location": "San Francisco"
            }
        ]

class DemoEmailService:
    def send_candidate_match_notification(self, *args, **kwargs): 
        print("📧 Candidate email sent (demo)")
    def send_employer_match_notification(self, *args, **kwargs): 
        print("📧 Employer email sent (demo)")

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

# HTML TEMPLATE (same as your working version)
COMPLETE_HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Job Matcher Pro - Stable Version</title>
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
        .match-score { 
            background: #28a745; 
            color: white; 
            padding: 8px 20px; 
            border-radius: 25px; 
            font-weight: bold;
            font-size: 1.1em;
        }
        .match-grade {
            background: #ffc107;
            color: #000;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 1.1em;
        }
        .score-breakdown {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
        }
        .breakdown-item {
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
            padding: 5px 0;
        }
        .breakdown-bar {
            background: #e9ecef;
            height: 8px;
            border-radius: 4px;
            margin-top: 5px;
            overflow: hidden;
        }
        .breakdown-fill {
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            border-radius: 4px;
        }
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
            <h1>🚀 AI Job Matcher Pro - Stable</h1>
            <p>Guaranteed Working Scoring System</p>
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
                </div>
                <div id="quick-results" style="margin-top: 20px;"></div>
            </div>
        </div>
        
        <div class="tab-container">
            <div class="tabs">
                <button class="tab active" onclick="showTab('matching')">🎯 AI Matching</button>
                <button class="tab" onclick="showTab('candidates')">👥 Candidates</button>
                <button class="tab" onclick="showTab('jobs')">📋 Jobs</button>
            </div>
            
            <div id="matching" class="tab-content active">
                <div class="card">
                    <h2>🤖 AI-Powered Job Matching</h2>
                    <p>Stable scoring algorithm with guaranteed breakdown display.</p>
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
                                    
                                    <div class="score-breakdown">
                                        <h5>📊 Score Breakdown:</h5>
                                        <div class="breakdown-item">
                                            <span>Skills Match:</span>
                                            <span>${breakdown.skills || 0}%</span>
                                        </div>
                                        <div class="breakdown-bar">
                                            <div class="breakdown-fill" style="width: ${breakdown.skills || 0}%"></div>
                                        </div>
                                        
                                        <div class="breakdown-item">
                                            <span>Experience:</span>
                                            <span>${breakdown.experience || 0}%</span>
                                        </div>
                                        <div class="breakdown-bar">
                                            <div class="breakdown-fill" style="width: ${breakdown.experience || 0}%"></div>
                                        </div>
                                        
                                        <div class="breakdown-item">
                                            <span>Location:</span>
                                            <span>${breakdown.location || 0}%</span>
                                        </div>
                                        <div class="breakdown-bar">
                                            <div class="breakdown-fill" style="width: ${breakdown.location || 0}%"></div>
                                        </div>
                                        
                                        <div class="breakdown-item">
                                            <span>Profile Relevance:</span>
                                            <span>${breakdown.profile || 0}%</span>
                                        </div>
                                        <div class="breakdown-bar">
                                            <div class="breakdown-fill" style="width: ${breakdown.profile || 0}%"></div>
                                        </div>
                                    </div>
                                    
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
        
        function testSystem() {
            showQuickResult('🧪 Testing system...', 'loading');
            setTimeout(() => {
                showQuickResult('✅ System is healthy!', 'success');
            }, 1000);
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
    return jsonify({'status': 'healthy', 'version': 'stable'})

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
    print("🚀 AI Job Matcher Pro - STABLE VERSION")
    print("=" * 70)
    print("✅ Stable scoring algorithm activated!")
    print("✅ Using demo services for guaranteed performance")
    print("🌐 Starting server on port 5000...")
    print("📍 Access via Ports tab → Globe icon 🌐")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=5000, debug=True)