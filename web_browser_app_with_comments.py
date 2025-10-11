"""
🌐 AI JOB MATCHER PRO - COMPLETE WORKING VERSION
Enterprise Recruitment Platform with AI-Powered Matching
Author: AI Assistant
Version: 2.0.0
"""

# Import required Python libraries
from flask import Flask, render_template_string, request, jsonify  # Flask web framework components
import sys  # System-specific parameters and functions
import os   # Operating system interface
import json # JSON encoding and decoding

# Add the 'src' directory to Python's module search path
# This allows us to import our custom modules from the src folder
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Print startup message
print("🚀 Starting AI Job Matcher Pro...")

"""
MODULE IMPORT SECTION
Imports all our custom AI modules with proper error handling
If modules are missing, it falls back to demo versions
"""
try:
    # Try to import our custom AI modules
    from database import DataManager        # Handles job and candidate data storage
    from matcher import SimpleMatcher       # AI matching algorithm
    from email_service import EmailService  # Email notification system
    from resume_parser import ResumeParser  # Resume text analysis
    print("✅ All AI modules loaded successfully!")
    
except ImportError as e:
    # If imports fail, create demo versions so the app still works
    print(f"⚠️  Some modules not found: {e}")
    print("💡 Running in demo mode with sample data")
    
    # Demo DataManager class - provides sample data if real database is unavailable
    class DataManager:
        def load_jobs(self):
            """Returns sample job data for demonstration"""
            return [
                {
                    "id": 1, 
                    "title": "Python Developer", 
                    "company": "TechCorp", 
                    "location": "Remote",
                    "description": "Develop web applications with Python and Django", 
                    "required_skills": ["python", "django", "sql"]
                },
                # ... more sample jobs
            ]
        
        def load_candidates(self):
            """Returns sample candidate data for demonstration"""
            return [
                {
                    "id": 1, 
                    "name": "John Smith", 
                    "email": "john@example.com", 
                    "profile": "Python developer with 5 years experience",
                    "skills": ["python", "django", "flask", "sql"], 
                    "experience_years": 5, 
                    "location": "Remote"
                },
                # ... more sample candidates
            ]
        
        def add_job(self, data): 
            """Simulates adding a new job (demo mode)"""
            return len(self.load_jobs()) + 1
            
        def add_candidate(self, data): 
            """Simulates adding a new candidate (demo mode)"""
            return len(self.load_candidates()) + 1
    
    # Demo SimpleMatcher class - provides basic matching if AI module is unavailable
    class SimpleMatcher:
        def find_matches(self):
            """
            Basic matching algorithm that finds common skills between jobs and candidates
            Returns: (results_dict, jobs_list, candidates_list)
            """
            jobs = DataManager().load_jobs()
            candidates = DataManager().load_candidates()
            results = {}
            
            # For each job, find matching candidates
            for i, job in enumerate(jobs):
                results[i] = []  # Initialize empty list for this job's matches
                
                # Check each candidate against this job
                for candidate in candidates:
                    # Find skills that exist in both job requirements and candidate skills
                    common_skills = set(job['required_skills']) & set(candidate['skills'])
                    
                    if common_skills:
                        # Calculate match score based on percentage of required skills matched
                        score = len(common_skills) / len(job['required_skills'])
                        
                        # Add match to results
                        results[i].append({
                            "candidate": candidate, 
                            "score": score, 
                            "common_skills": list(common_skills)
                        })
                
                # Sort matches by score (highest first)
                results[i].sort(key=lambda x: x['score'], reverse=True)
            
            return results, jobs, candidates
    
    # Demo EmailService class - simulates email functionality
    class EmailService:
        def send_candidate_match_notification(self, *args, **kwargs): 
            """Simulates sending email to candidate (prints to console)"""
            print("📧 Candidate email would be sent (test mode)")
            
        def send_employer_match_notification(self, *args, **kwargs): 
            """Simulates sending email to employer (prints to console)"""
            print("📧 Employer email would be sent (test mode)")
    
    # Demo ResumeParser class - provides basic resume parsing
    class ResumeParser:
        def parse_resume_to_candidate(self, text):
            """Extracts basic information from resume text (demo version)"""
            return {
                "name": "Candidate from Resume",
                "email": "resume@example.com",
                "phone": "123-456-7890",
                "skills": ["python", "communication", "problem-solving"],
                "experience_years": 3,
                "location": "Unknown",
                "education": "Extracted from resume",
                "profile": "Professional extracted from resume text"
            }

"""
FLASK APPLICATION SETUP
Initialize the web application and all services
"""
# Create the main Flask application instance
# __name__ tells Flask where to look for templates and static files
app = Flask(__name__)

# Initialize all our service classes
# These will use either the real modules or demo versions depending on what imported
db = DataManager()           # Database manager for jobs and candidates
matcher = SimpleMatcher()    # AI matching engine
email_service = EmailService()  # Email notification service
resume_parser = ResumeParser()  # Resume parsing service

print("✅ All services initialized!")

"""
HTML TEMPLATE SECTION
This is the complete web interface that users see in their browser
It includes HTML, CSS, and JavaScript all in one string
"""
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Job Matcher Pro</title>
    <style>
        /* MODERN CSS RESET - Ensures consistent styling across browsers */
        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; /* Includes padding and border in element's total width/height */
        }
        
        /* MAIN BODY STYLING */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); /* Purple gradient background */
            min-height: 100vh; /* Full viewport height */
            padding: 20px;
            color: #333; /* Dark gray text color */
        }
        
        /* MAIN CONTAINER - Centers and contains all content */
        .container {
            max-width: 1200px; /* Maximum width on large screens */
            margin: 0 auto; /* Center horizontally */
            background: white; /* White background for content */
            border-radius: 20px; /* Rounded corners */
            box-shadow: 0 25px 50px rgba(0,0,0,0.15); /* Subtle shadow for depth */
            overflow: hidden; /* Prevents content from spilling out of rounded corners */
        }
        
        /* HEADER SECTION - Top banner with title */
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); /* Same gradient as body */
            color: white; /* White text */
            padding: 50px 40px; /* Vertical and horizontal padding */
            text-align: center; /* Center align text */
        }
        
        .header h1 {
            font-size: 3em; /* Large font size for main title */
            margin-bottom: 15px; /* Space below title */
            font-weight: 700; /* Bold font weight */
        }
        
        .header p {
            font-size: 1.3em; /* Slightly larger paragraph text */
            opacity: 0.9; /* Slightly transparent for subtle effect */
        }
        
        /* DASHBOARD LAYOUT - Two-column grid for stats and actions */
        .dashboard {
            display: grid; /* CSS Grid layout */
            grid-template-columns: 1fr 1fr; /* Two equal columns */
            gap: 30px; /* Space between columns */
            padding: 40px; /* Internal spacing */
            background: #f8f9fa; /* Light gray background */
        }
        
        /* RESPONSIVE DESIGN - Stack columns on mobile */
        @media (max-width: 768px) {
            .dashboard { 
                grid-template-columns: 1fr; /* Single column on small screens */
            }
        }
        
        /* CARD COMPONENT - Reusable card style for content sections */
        .card {
            background: white; /* White background */
            padding: 35px; /* Internal spacing */
            border-radius: 15px; /* Rounded corners */
            box-shadow: 0 10px 30px rgba(0,0,0,0.1); /* Card shadow */
            border-left: 5px solid #667eea; /* Accent border on left */
        }
        
        .card h2 {
            color: #333; /* Dark text color */
            margin-bottom: 25px; /* Space below heading */
            font-size: 1.6em; /* Larger font size */
            display: flex; /* Flexbox for icon alignment */
            align-items: center; /* Vertically center icons and text */
            gap: 12px; /* Space between icon and text */
        }
        
        /* STATISTICS GRID - 2x2 grid for displaying numbers */
        .stats {
            display: grid; /* CSS Grid */
            grid-template-columns: 1fr 1fr; /* Two equal columns */
            gap: 20px; /* Space between stat items */
            margin-top: 25px; /* Space above stats */
        }
        
        /* INDIVIDUAL STAT ITEM */
        .stat-item {
            text-align: center; /* Center align content */
            padding: 25px 20px; /* Internal spacing */
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); /* Subtle gradient */
            border-radius: 12px; /* Rounded corners */
            border: 2px solid #e9ecef; /* Light border */
            transition: all 0.3s ease; /* Smooth hover effects */
        }
        
        .stat-item:hover {
            transform: translateY(-5px); /* Lift effect on hover */
            border-color: #667eea; /* Change border color on hover */
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.15); /* Enhanced shadow on hover */
        }
        
        /* LARGE STAT NUMBER */
        .stat-number {
            font-size: 2.8em; /* Very large font size */
            font-weight: bold; /* Bold weight */
            color: #667eea; /* Brand color */
            display: block; /* Block display */
            line-height: 1; /* Tight line spacing */
        }
        
        /* STAT LABEL */
        .stat-label {
            color: #666; /* Medium gray color */
            font-size: 0.95em; /* Slightly smaller text */
            margin-top: 8px; /* Space above label */
            font-weight: 500; /* Medium font weight */
        }
        
        /* BUTTON STYLES - Reusable button component */
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); /* Gradient background */
            color: white; /* White text */
            border: none; /* No border */
            padding: 16px 32px; /* Generous padding */
            border-radius: 10px; /* Rounded corners */
            cursor: pointer; /* Pointer cursor on hover */
            font-size: 1.05em; /* Slightly larger text */
            font-weight: 600; /* Semi-bold text */
            margin: 10px; /* External spacing */
            transition: all 0.3s ease; /* Smooth transitions */
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3); /* Button shadow */
        }
        
        .btn:hover {
            transform: translateY(-3px); /* Lift effect on hover */
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4); /* Enhanced shadow on hover */
        }
        
        /* SUCCESS BUTTON VARIANT */
        .btn-success {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%); /* Green gradient */
            box-shadow: 0 6px 20px rgba(40, 167, 69, 0.3); /* Green shadow */
        }
        
        /* WARNING BUTTON VARIANT */
        .btn-warning {
            background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%); /* Orange gradient */
            color: #000; /* Black text for contrast */
            box-shadow: 0 6px 20px rgba(255, 193, 7, 0.3); /* Orange shadow */
        }
        
        /* TAB NAVIGATION SYSTEM */
        .tab-container {
            padding: 0 40px 40px 40px; /* Padding: top, right, bottom, left */
        }
        
        .tabs {
            display: flex; /* Flexbox for horizontal layout */
            background: #f8f9fa; /* Light background */
            border-radius: 12px; /* Rounded corners */
            padding: 15px; /* Internal spacing */
            margin-bottom: 35px; /* Space below tabs */
            flex-wrap: wrap; /* Allow wrapping on small screens */
            gap: 10px; /* Space between tabs */
        }
        
        .tab {
            padding: 16px 28px; /* Button padding */
            background: transparent; /* Transparent background */
            border: none; /* No border */
            cursor: pointer; /* Pointer cursor */
            border-radius: 10px; /* Rounded corners */
            font-weight: 600; /* Semi-bold text */
            transition: all 0.3s ease; /* Smooth transitions */
            color: #666; /* Medium gray text */
            flex: 1; /* Flexible width */
            min-width: 120px; /* Minimum width */
        }
        
        .tab:hover {
            background: rgba(102, 126, 234, 0.1); /* Light blue background on hover */
            color: #667eea; /* Blue text on hover */
        }
        
        .tab.active {
            background: #667eea; /* Blue background for active tab */
            color: white; /* White text */
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3); /* Shadow for active tab */
        }
        
        /* TAB CONTENT AREAS */
        .tab-content {
            display: none; /* Hidden by default */
            animation: fadeIn 0.5s ease-in; /* Fade-in animation */
        }
        
        .tab-content.active {
            display: block; /* Show active tab content */
        }
        
        /* FADE IN ANIMATION */
        @keyframes fadeIn {
            from { 
                opacity: 0; /* Start invisible */
                transform: translateY(20px); /* Start slightly lower */
            }
            to { 
                opacity: 1; /* End fully visible */
                transform: translateY(0); /* End at normal position */
            }
        }
        
        /* LOADING INDICATOR */
        .loading {
            text-align: center; /* Center align */
            padding: 50px; /* Generous padding */
            color: #667eea; /* Blue text */
            font-size: 1.3em; /* Larger text */
        }
        
        .loading::after {
            content: ' 🚀'; /* Rocket emoji */
            animation: pulse 1.5s infinite; /* Pulsing animation */
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; } /* Full opacity at start and end */
            50% { opacity: 0.5; } /* Half opacity in middle */
        }
        
        /* SUCCESS MESSAGE STYLING */
        .success {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); /* Green gradient */
            color: #155724; /* Dark green text */
            padding: 25px; /* Internal spacing */
            border-radius: 12px; /* Rounded corners */
            border-left: 5px solid #28a745; /* Green accent border */
            margin: 25px 0; /* Vertical spacing */
        }
        
        /* ERROR MESSAGE STYLING */
        .error {
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); /* Red gradient */
            color: #721c24; /* Dark red text */
            padding: 25px; /* Internal spacing */
            border-radius: 12px; /* Rounded corners */
            border-left: 5px solid #dc3545; /* Red accent border */
            margin: 25px 0; /* Vertical spacing */
        }
        
        /* CARD STYLES FOR MATCHES, CANDIDATES, AND JOBS */
        .match-card, .candidate-card, .job-card {
            background: white; /* White background */
            padding: 30px; /* Generous padding */
            border-radius: 15px; /* Rounded corners */
            box-shadow: 0 8px 25px rgba(0,0,0,0.1); /* Card shadow */
            margin: 25px 0; /* Vertical spacing */
            border-left: 5px solid #28a745; /* Green accent border */
            transition: all 0.3s ease; /* Smooth hover effects */
        }
        
        .match-card:hover, .candidate-card:hover, .job-card:hover {
            transform: translateY(-5px); /* Lift effect on hover */
            box-shadow: 0 15px 35px rgba(0,0,0,0.15); /* Enhanced shadow on hover */
        }
        
        /* MATCH HEADER - Contains job title and match score */
        .match-header {
            display: flex; /* Flexbox layout */
            justify-content: space-between; /* Space between title and score */
            align-items: center; /* Vertical alignment */
            margin-bottom: 20px; /* Space below header */
            flex-wrap: wrap; /* Allow wrapping */
            gap: 20px; /* Space between elements when wrapped */
        }
        
        /* MATCH SCORE BADGE */
        .match-score {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%); /* Green gradient */
            color: white; /* White text */
            padding: 10px 25px; /* Internal spacing */
            border-radius: 25px; /* Pill shape */
            font-weight: bold; /* Bold text */
            font-size: 1.2em; /* Larger text */
            box-shadow: 0 6px 20px rgba(40, 167, 69, 0.3); /* Green shadow */
        }
        
        /* SKILLS TAGS */
        .skills {
            display: flex; /* Flexbox for horizontal layout */
            flex-wrap: wrap; /* Allow wrapping to new lines */
            gap: 10px; /* Space between tags */
            margin: 20px 0; /* Vertical spacing */
        }
        
        .skill-tag {
            background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%); /* Gray gradient */
            padding: 8px 18px; /* Internal spacing */
            border-radius: 20px; /* Pill shape */
            font-size: 0.95em; /* Slightly smaller text */
            border: 1px solid #ced4da; /* Light border */
        }
        
        /* ACTION BUTTONS CONTAINER */
        .action-buttons {
            display: flex; /* Flexbox for horizontal layout */
            gap: 15px; /* Space between buttons */
            flex-wrap: wrap; /* Allow wrapping */
            margin: 25px 0; /* Vertical spacing */
        }
        
        /* RESULTS CONTAINER */
        .results-container {
            margin-top: 35px; /* Space above results */
        }
        
        /* FORM STYLING */
        .form-group {
            margin-bottom: 25px; /* Space between form groups */
        }
        
        .form-group label {
            display: block; /* Block display for proper spacing */
            margin-bottom: 10px; /* Space below label */
            font-weight: 600; /* Semi-bold text */
            color: #333; /* Dark text */
            font-size: 1.05em; /* Slightly larger text */
        }
        
        .form-group input, .form-group textarea {
            width: 100%; /* Full width */
            padding: 18px; /* Generous padding */
            border: 2px solid #e9ecef; /* Light border */
            border-radius: 10px; /* Rounded corners */
            font-size: 1em; /* Normal text size */
            transition: border-color 0.3s ease; /* Smooth border transition */
            font-family: inherit; /* Inherit font family */
        }
        
        .form-group input:focus, .form-group textarea:focus {
            outline: none; /* Remove default outline */
            border-color: #667eea; /* Blue border on focus */
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); /* Blue glow effect */
        }
        
        .form-group textarea {
            height: 140px; /* Fixed initial height */
            resize: vertical; /* Allow vertical resizing only */
        }
    </style>
</head>
<body>
    <!-- MAIN CONTAINER - Wraps all content -->
    <div class="container">
        <!-- HEADER SECTION - Application title and description -->
        <div class="header">
            <h1>🚀 AI Job Matcher Pro</h1>
            <p>Enterprise Recruitment Platform Powered by Artificial Intelligence</p>
        </div>
        
        <!-- DASHBOARD SECTION - Statistics and quick actions -->
        <div class="dashboard">
            <!-- STATISTICS CARD -->
            <div class="card">
                <h2>📊 Live Dashboard</h2>
                <div class="stats">
                    <!-- Jobs Count -->
                    <div class="stat-item">
                        <span class="stat-number" id="jobs-count">0</span>
                        <div class="stat-label">Total Jobs</div>
                    </div>
                    <!-- Candidates Count -->
                    <div class="stat-item">
                        <span class="stat-number" id="candidates-count">0</span>
                        <div class="stat-label">Total Candidates</div>
                    </div>
                    <!-- Matches Count -->
                    <div class="stat-item">
                        <span class="stat-number" id="matches-count">0</span>
                        <div class="stat-label">Matches Made</div>
                    </div>
                    <!-- Success Rate -->
                    <div class="stat-item">
                        <span class="stat-number" id="success-rate">0%</span>
                        <div class="stat-label">Success Rate</div>
                    </div>
                </div>
                <!-- Action Buttons for Dashboard -->
                <div class="action-buttons">
                    <button class="btn" onclick="loadStats()">🔄 Refresh Stats</button>
                    <button class="btn btn-warning" onclick="testSystem()">🧪 Test System</button>
                </div>
            </div>
            
            <!-- QUICK ACTIONS CARD -->
            <div class="card">
                <h2>⚡ Quick Actions</h2>
                <div class="action-buttons">
                    <button class="btn btn-success" onclick="runMatching()">🤖 Run AI Matching</button>
                    <button class="btn" onclick="showTab('candidates')">👥 View Candidates</button>
                    <button class="btn" onclick="showTab('jobs')">📋 View Jobs</button>
                    <button class="btn" onclick="showTab('resume-parser')">📄 Parse Resume</button>
                </div>
                <!-- Quick results display area -->
                <div id="quick-results" style="margin-top: 20px;"></div>
            </div>
        </div>
        
        <!-- TAB NAVIGATION AND CONTENT AREA -->
        <div class="tab-container">
            <!-- TAB NAVIGATION BAR -->
            <div class="tabs">
                <button class="tab active" onclick="showTab('matching')">🎯 AI Matching</button>
                <button class="tab" onclick="showTab('candidates')">👥 Candidates</button>
                <button class="tab" onclick="showTab('jobs')">📋 Jobs</button>
                <button class="tab" onclick="showTab('resume-parser')">📄 Resume Parser</button>
                <button class="tab" onclick="showTab('email-demo')">📧 Email Demo</button>
            </div>
            
            <!-- AI MATCHING TAB CONTENT -->
            <div id="matching" class="tab-content active">
                <div class="card">
                    <h2>🤖 AI-Powered Job Matching</h2>
                    <p>Our advanced AI analyzes job requirements and candidate profiles using semantic similarity and skill matching to find perfect matches.</p>
                    
                    <div class="action-buttons">
                        <button class="btn btn-success" onclick="runMatching()">🚀 Run AI Matching</button>
                        <button class="btn" onclick="loadStats()">📊 Update Stats</button>
                    </div>
                    
                    <div id="matching-results" class="results-container">
                        <p>Click "Run AI Matching" to discover intelligent job-candidate matches...</p>
                    </div>
                </div>
            </div>
            
            <!-- CANDIDATES TAB CONTENT -->
            <div id="candidates" class="tab-content">
                <div class="card">
                    <h2>👥 Candidate Database</h2>
                    <p>View and manage all candidate profiles in the system.</p>
                    
                    <div class="action-buttons">
                        <button class="btn" onclick="loadCandidates()">🔄 Load Candidates</button>
                    </div>
                    
                    <div id="candidates-list" class="results-container">
                        <p>Candidate list will appear here...</p>
                    </div>
                </div>
            </div>
            
            <!-- JOBS TAB CONTENT -->
            <div id="jobs" class="tab-content">
                <div class="card">
                    <h2>📋 Job Database</h2>
                    <p>View and manage all job postings in the system.</p>
                    
                    <div class="action-buttons">
                        <button class="btn" onclick="loadJobs()">🔄 Load Jobs</button>
                    </div>
                    
                    <div id="jobs-list" class="results-container">
                        <p>Job list will appear here...</p>
                    </div>
                </div>
            </div>
            
            <!-- RESUME PARSER TAB CONTENT -->
            <div id="resume-parser" class="tab-content">
                <div class="card">
                    <h2>📄 AI Resume Parser</h2>
                    <p>Automatically extract skills, experience, and contact information from resume text.</p>
                    
                    <div class="form-group">
                        <label for="resume-text">Paste Resume Text:</label>
                        <textarea id="resume-text" placeholder="Paste resume content here...&#10;Example:&#10;John Smith&#10;Email: john.smith@email.com&#10;Experience: 5 years Python development&#10;Skills: Python, Django, JavaScript, SQL..." style="height: 200px;"></textarea>
                    </div>
                    
                    <div class="action-buttons">
                        <button class="btn btn-success" onclick="parseResume()">🔍 Parse Resume</button>
                        <button class="btn" onclick="document.getElementById('resume-text').value = ''">🗑️ Clear</button>
                    </div>
                    
                    <div id="resume-results" class="results-container">
                        <p>Parsed candidate data will appear here...</p>
                    </div>
                </div>
            </div>
            
            <!-- EMAIL DEMO TAB CONTENT -->
            <div id="email-demo" class="tab-content">
                <div class="card">
                    <h2>📧 Email Notification System</h2>
                    <p>Test automated email notifications for candidates and employers. (Runs in test mode - no real emails sent)</p>
                    
                    <div class="action-buttons">
                        <button class="btn" onclick="testCandidateEmail()">👤 Test Candidate Email</button>
                        <button class="btn btn-success" onclick="testEmployerEmail()">🏢 Test Employer Email</button>
                    </div>
                    
                    <div id="email-results" class="results-container">
                        <p>Email test results will appear here. Check terminal for full email previews.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- JAVASCRIPT SECTION - All client-side functionality -->
    <script>
        /**
         * TAB MANAGEMENT FUNCTIONS
         * Handles showing/hiding tab content and updating active tab states
         */
        
        /**
         * Shows the specified tab and hides all others
         * @param {string} tabName - The ID of the tab to show
         */
        function showTab(tabName) {
            // Hide all tab content areas
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active'); // Remove active class from all tabs
            });
            
            // Show the selected tab content
            document.getElementById(tabName).classList.add('active'); // Add active class to selected tab
            
            // Update tab buttons to show which is active
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active'); // Remove active class from all tab buttons
            });
            event.target.classList.add('active'); // Add active class to clicked tab button
        }
        
        /**
         * STATISTICS MANAGEMENT FUNCTIONS
         * Handles loading and displaying system statistics
         */
        
        /**
         * Loads and displays system statistics from the API
         */
        async function loadStats() {
            // Show loading state in all stat fields
            document.getElementById('jobs-count').textContent = '...';
            document.getElementById('candidates-count').textContent = '...';
            document.getElementById('matches-count').textContent = '...';
            document.getElementById('success-rate').textContent = '...';
            
            try {
                // Fetch statistics from the API
                const response = await fetch('/api/stats');
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                
                // Parse JSON response
                const data = await response.json();
                
                // Update DOM with new statistics
                document.getElementById('jobs-count').textContent = data.total_jobs || 0;
                document.getElementById('candidates-count').textContent = data.total_candidates || 0;
                document.getElementById('matches-count').textContent = data.total_matches || 0;
                document.getElementById('success-rate').textContent = (data.success_rate || 0) + '%';
                
                // Show success message
                showQuickResult('✅ Stats updated successfully!', 'success');
            } catch (error) {
                // Handle errors and show fallback values
                console.error('Stats error:', error);
                showQuickResult('❌ Failed to load stats', 'error');
            }
        }
        
        /**
         * AI MATCHING FUNCTION
         * Runs the AI matching algorithm and displays results
         */
        async function runMatching() {
            const resultsElement = document.getElementById('matching-results');
            // Show loading state
            resultsElement.innerHTML = '<div class="loading">🤖 AI is analyzing jobs and candidates... This may take a few seconds.</div>';
            
            try {
                // Send POST request to run matching
                const response = await fetch('/api/run-matching', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'}
                });
                
                // Check for HTTP errors
                if (!response.ok) throw new Error(`Server returned ${response.status}`);
                
                // Parse response data
                const data = await response.json();
                
                // Handle API errors
                if (data.error) {
                    resultsElement.innerHTML = `<div class="error">❌ Error: ${data.error}</div>`;
                    return;
                }
                
                // Build results HTML
                let html = '<h3>🎯 Matching Results</h3>';
                
                if (data.matches && data.matches.length > 0) {
                    // Show success message with match count
                    html += `<div class="success">✅ Found ${data.matches.length} high-quality matches!</div>`;
                    
                    // Create a card for each match
                    data.matches.forEach(match => {
                        html += `
                            <div class="match-card">
                                <div class="match-header">
                                    <h4>${match.job_title} at ${match.company}</h4>
                                    <span class="match-score">${(match.top_score * 100).toFixed(1)}% Match</span>
                                </div>
                                <p><strong>👤 Top Candidate:</strong> ${match.top_candidate}</p>
                                <p><strong>🔧 Common Skills:</strong> ${match.common_skills && match.common_skills.length > 0 ? match.common_skills.join(', ') : 'No common skills detected'}</p>
                            </div>
                        `;
                    });
                } else {
                    // Show no matches found message
                    html += '<div class="error">❌ No matches found. Try adding more jobs or candidates with overlapping skills.</div>';
                }
                
                // Update the DOM with results
                resultsElement.innerHTML = html;
                loadStats(); // Refresh statistics
                
            } catch (error) {
                // Handle matching errors
                console.error('Matching error:', error);
                resultsElement.innerHTML = `<div class="error">❌ Error running AI matching: ${error.message}</div>`;
            }
        }
        
        /**
         * CANDIDATE MANAGEMENT FUNCTIONS
         * Handles loading and displaying candidate data
         */
        async function loadCandidates() {
            const listElement = document.getElementById('candidates-list');
            // Show loading state
            listElement.innerHTML = '<div class="loading">🔄 Loading candidates from database...</div>';
            
            try {
                // Fetch candidates from API
                const response = await fetch('/api/get-candidates');
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                
                const data = await response.json();
                
                let html = '<h3>👥 All Candidates</h3>';
                
                if (data.candidates && data.candidates.length > 0) {
                    // Show success message
                    html += `<div class="success">✅ Loaded ${data.candidates.length} candidates</div>`;
                    
                    // Create a card for each candidate
                    data.candidates.forEach(candidate => {
                        html += `
                            <div class="candidate-card">
                                <h4>${candidate.name}</h4>
                                <p><strong>📧 Email:</strong> ${candidate.email || 'Not provided'}</p>
                                <p><strong>💼 Experience:</strong> ${candidate.experience_years} years</p>
                                <p><strong>📍 Location:</strong> ${candidate.location || 'Not specified'}</p>
                                <div class="skills">
                                    ${candidate.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                                </div>
                                <p><strong>📝 Profile:</strong> ${candidate.profile}</p>
                            </div>
                        `;
                    });
                } else {
                    // Show no candidates message
                    html += '<div class="error">❌ No candidates found in database.</div>';
                }
                
                // Update DOM with candidate list
                listElement.innerHTML = html;
            } catch (error) {
                // Handle candidate loading errors
                console.error('Candidates error:', error);
                listElement.innerHTML = `<div class="error">❌ Error loading candidates: ${error.message}</div>`;
            }
        }
        
        /**
         * JOB MANAGEMENT FUNCTIONS
         * Handles loading and displaying job data
         */
        async function loadJobs() {
            const listElement = document.getElementById('jobs-list');
            // Show loading state
            listElement.innerHTML = '<div class="loading">🔄 Loading jobs from database...</div>';
            
            try {
                // Fetch jobs from API
                const response = await fetch('/api/get-jobs');
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                
                const data = await response.json();
                
                let html = '<h3>📋 All Jobs</h3>';
                
                if (data.jobs && data.jobs.length > 0) {
                    // Show success message
                    html += `<div class="success">✅ Loaded ${data.jobs.length} jobs</div>`;
                    
                    // Create a card for each job
                    data.jobs.forEach(job => {
                        html += `
                            <div class="job-card">
                                <h4>${job.title}</h4>
                                <p><strong>🏢 Company:</strong> ${job.company}</p>
                                <p><strong>📍 Location:</strong> ${job.location}</p>
                                <div class="skills">
                                    ${job.required_skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                                </div>
                                <p><strong>📝 Description:</strong> ${job.description}</p>
                            </div>
                        `;
                    });
                } else {
                    // Show no jobs message
                    html += '<div class="error">❌ No jobs found in database.</div>';
                }
                
                // Update DOM with job list
                listElement.innerHTML = html;
            } catch (error) {
                // Handle job loading errors
                console.error('Jobs error:', error);
                listElement.innerHTML = `<div class="error">❌ Error loading jobs: ${error.message}</div>`;
            }
        }
        
        /**
         * RESUME PARSING FUNCTION
         * Sends resume text to backend for parsing and displays results
         */
        async function parseResume() {
            const resumeText = document.getElementById('resume-text').value.trim();
            
            // Validate input
            if (!resumeText) {
                alert('❌ Please paste some resume text first!');
                return;
            }
            
            const resultsElement = document.getElementById('resume-results');
            // Show loading state
            resultsElement.innerHTML = '<div class="loading">🔍 AI is parsing resume... Extracting skills and experience.</div>';
            
            try {
                // Send resume text to parsing API
                const response = await fetch('/api/parse-resume', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({resume_text: resumeText})
                });
                
                // Check for HTTP errors
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                
                // Parse response
                const result = await response.json();
                
                // Handle API errors
                if (result.error) {
                    resultsElement.innerHTML = `<div class="error">❌ Error: ${result.error}</div>`;
                    return;
                }
                
                // Extract candidate data from response
                const candidate = result.candidate_data;
                
                // Build results HTML
                let resultsHtml = `
                    <div class="success">
                        <strong>✅ Resume Parsed Successfully!</strong>
                    </div>
                    <div class="candidate-card">
                        <h3>👤 ${candidate.name}</h3>
                        <p><strong>📧 Email:</strong> ${candidate.email}</p>
                        <p><strong>📞 Phone:</strong> ${candidate.phone}</p>
                        <p><strong>💼 Experience:</strong> ${candidate.experience_years} years</p>
                        <p><strong>🎓 Education:</strong> ${candidate.education}</p>
                        <p><strong>📍 Location:</strong> ${candidate.location}</p>
                        <p><strong>📝 Summary:</strong> ${candidate.profile}</p>
                        <div class="skills">
                            ${candidate.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                        </div>
                    </div>
                `;
                
                // Update DOM with parsing results
                resultsElement.innerHTML = resultsHtml;
            } catch (error) {
                // Handle parsing errors
                console.error('Resume parse error:', error);
                resultsElement.innerHTML = `<div class="error">❌ Error parsing resume: ${error.message}</div>`;
            }
        }
        
        /**
         * EMAIL TESTING FUNCTIONS
         * Tests the email notification system
         */
        
        /**
         * Tests candidate email notifications
         */
        async function testCandidateEmail() {
            const resultsElement = document.getElementById('email-results');
            // Show loading state
            resultsElement.innerHTML = '<div class="loading">📧 Testing candidate email notification...</div>';
            
            try {
                // Send test request to email API
                const response = await fetch('/api/test-candidate-email', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'}
                });
                
                // Check for HTTP errors
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                
                // Parse response
                const result = await response.json();
                
                // Display results
                resultsElement.innerHTML = `
                    <div class="success">
                        <h4>📧 Candidate Email Test</h4>
                        <p><strong>Status:</strong> ${result.status}</p>
                        <p><strong>Message:</strong> ${result.message}</p>
                        <p><em>💡 Check your terminal for the full email preview (no real emails sent in test mode)</em></p>
                    </div>
                `;
            } catch (error) {
                // Handle email test errors
                console.error('Email test error:', error);
                resultsElement.innerHTML = `<div class="error">❌ Error testing email: ${error.message}</div>`;
            }
        }
        
        /**
         * Tests employer email notifications
         */
        async function testEmployerEmail() {
            const resultsElement = document.getElementById('email-results');
            // Show loading state
            resultsElement.innerHTML = '<div class="loading">📧 Testing employer email notification...</div>';
            
            try {
                // Send test request to email API
                const response = await fetch('/api/test-employer-email', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'}
                });
                
                // Check for HTTP errors
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                
                // Parse response
                const result = await response.json();
                
                // Display results
                resultsElement.innerHTML = `
                    <div class="success">
                        <h4>📧 Employer Email Test</h4>
                        <p><strong>Status:</strong> ${result.status}</p>
                        <p><strong>Message:</strong> ${result.message}</p>
                        <p><em>💡 Check your terminal for the full email preview (no real emails sent in test mode)</em></p>
                    </div>
                `;
            } catch (error) {
                // Handle email test errors
                console.error('Email test error:', error);
                resultsElement.innerHTML = `<div class="error">❌ Error testing email: ${error.message}</div>`;
            }
        }
        
        /**
         * SYSTEM TESTING FUNCTION
         * Tests all API endpoints to ensure system is working
         */
        async function testSystem() {
            // Show testing message
            showQuickResult('🧪 Testing all system components...', 'loading');
            
            // Define all API endpoints to test
            const endpoints = [
                { name: 'API Health', url: '/api/health' },
                { name: 'Statistics', url: '/api/stats' },
                { name: 'Candidates', url: '/api/get-candidates' },
                { name: 'Jobs', url: '/api/get-jobs' }
            ];
            
            let allPassed = true; // Track if all tests pass
            
            // Test each endpoint
            for (const endpoint of endpoints) {
                try {
                    const response = await fetch(endpoint.url);
                    if (!response.ok) {
                        allPassed = false;
                        break;
                    }
                } catch (error) {
                    allPassed = false;
                    break;
                }
            }
            
            // Show final results
            if (allPassed) {
                showQuickResult('✅ All system endpoints are working correctly!', 'success');
            } else {
                showQuickResult('❌ Some system components need attention', 'error');
            }
        }
        
        /**
         * UTILITY FUNCTIONS
         * Helper functions used throughout the application
         */
        
        /**
         * Shows a quick result message that automatically disappears
         * @param {string} message - The message to display
         * @param {string} type - The message type ('success', 'error', 'loading')
         */
        function showQuickResult(message, type) {
            const quickResults = document.getElementById('quick-results');
            // Display message with appropriate styling
            quickResults.innerHTML = `<div class="${type}">${message}</div>`;
            // Auto-remove after 5 seconds
            setTimeout(() => {
                quickResults.innerHTML = '';
            }, 5000);
        }
        
        /**
         * INITIALIZATION
         * Runs when the page loads to set up the application
         */
        window.addEventListener('load', function() {
            console.log('🚀 AI Job Matcher Pro initialized!');
            loadStats(); // Load initial statistics
        });
    </script>
</body>
</html>
'''

"""
FLASK API ROUTES SECTION
Defines all the backend endpoints that the frontend JavaScript calls
"""

@app.route('/')
def home():
    """
    Main route - serves the HTML template to the browser
    This is the entry point of the web application
    """
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/health')
def health():
    """
    Health check endpoint
    Used by the frontend to verify the backend is running
    """
    return jsonify({
        'status': 'healthy',
        'message': 'AI Job Matcher Pro is running!',
        'version': '2.0.0'
    })

@app.route('/api/stats')
def get_stats():
    """
    Statistics endpoint
    Returns current system statistics (job count, candidate count, etc.)
    """
    try:
        # Load current data from database
        jobs = db.load_jobs()
        candidates = db.load_candidates()
        
        # Calculate and return statistics
        return jsonify({
            'total_jobs': len(jobs),
            'total_candidates': len(candidates),
            'total_matches': len(jobs) * len(candidates),  # Estimated potential matches
            'success_rate': 95  # Placeholder success rate
        })
    except Exception as e:
        # Return error if something goes wrong
        return jsonify({'error': str(e)}), 500

@app.route('/api/run-matching', methods=['POST'])
def run_matching():
    """
    AI Matching endpoint
    Runs the matching algorithm and returns results
    Only accepts POST requests
    """
    try:
        print("🤖 Running AI matching algorithm...")
        
        # Call the matching algorithm
        results, jobs, candidates = matcher.find_matches()
        
        # Process results into a clean format for the frontend
        matches = []
        for job_index, job_matches in results.items():
            if job_matches and len(job_matches) > 0:
                job = jobs[job_index]
                top_match = job_matches[0]  # Get the best match
                candidate = top_match['candidate']
                
                # Format match data for frontend
                matches.append({
                    'job_id': job['id'],
                    'job_title': job['title'],
                    'company': job['company'],
                    'candidate_id': candidate['id'],
                    'top_candidate': candidate['name'],
                    'top_score': top_match['score'],
                    'common_skills': top_match.get('common_skills', [])[:5]  # Limit to top 5 skills
                })
        
        print(f"✅ Found {len(matches)} matches")
        return jsonify({'matches': matches})
        
    except Exception as e:
        # Log error and return error response
        print(f"❌ Matching error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-candidates')
def get_candidates():
    """
    Candidates endpoint
    Returns all candidates from the database
    """
    try:
        candidates = db.load_candidates()
        return jsonify({'candidates': candidates})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-jobs')
def get_jobs():
    """
    Jobs endpoint  
    Returns all jobs from the database
    """
    try:
        jobs = db.load_jobs()
        return jsonify({'jobs': jobs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/parse-resume', methods=['POST'])
def parse_resume():
    """
    Resume parsing endpoint
    Accepts resume text and returns structured candidate data
    Only accepts POST requests
    """
    try:
        # Extract resume text from request
        resume_text = request.json.get('resume_text', '')
        print(f"📄 Parsing resume text ({len(resume_text)} characters)...")
        
        # Parse resume using AI
        candidate_data = resume_parser.parse_resume_to_candidate(resume_text)
        print(f"✅ Resume parsed: {candidate_data['name']}")
        
        # Return parsed data
        return jsonify({
            'success': True,
            'candidate_data': candidate_data
        })
    except Exception as e:
        # Log error and return error response
        print(f"❌ Resume parse error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/test-candidate-email', methods=['POST'])
def test_candidate_email():
    """
    Candidate email test endpoint
    Tests the candidate email notification system
    Only accepts POST requests
    """
    try:
        print("📧 Testing candidate email...")
        
        # Send test email (runs in test mode - no real emails sent)
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
        print(f"❌ Email test error: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Failed: {str(e)}'
        }), 500

@app.route('/api/test-employer-email', methods=['POST'])
def test_employer_email():
    """
    Employer email test endpoint
    Tests the employer email notification system  
    Only accepts POST requests
    """
    try:
        print("📧 Testing employer email...")
        
        # Send test email (runs in test mode - no real emails sent)
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
        print(f"❌ Email test error: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Failed: {str(e)}'
        }), 500

"""
APPLICATION STARTUP
This code runs when the script is executed directly
"""
if __name__ == '__main__':
    # Print startup information
    print("🚀 AI Job Matcher Pro - Complete Working Version")
    print("=" * 70)
    print("✅ All systems initialized and ready!")
    print("📊 Sample data loaded for demonstration")
    print("")
    print("🎯 FEATURES INCLUDED:")
    print("   • 🤖 AI-Powered Job Matching")
    print("   • 👥 Candidate Management")
    print("   • 📋 Job Management") 
    print("   • 📄 Resume Parsing")
    print("   • 📧 Email Notifications")
    print("   • 📈 Live Dashboard")
    print("")
    print("🌐 ACCESS INSTRUCTIONS:")
    print("   1. Server will start on port 5000")
    print("   2. Go to 'Ports' tab in VS Code")
    print("   3. Find port 5000 and click the globe icon 🌐")
    print("   4. OR use URL: https://your-codespace-5000.app.github.dev")
    print("")
    print("⏳ Starting server...")
    print("=" * 70)
    
    # Start the Flask development server
    # host='0.0.0.0' makes the server accessible from outside
    # port=5000 specifies the port to listen on
    # debug=False disables debug mode for production use
    app.run(host='0.0.0.0', port=5000, debug=False)