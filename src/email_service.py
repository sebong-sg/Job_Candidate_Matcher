# 📧 EMAIL NOTIFICATION SERVICE - CORRECTED IMPORTS
# Sends beautiful emails to candidates and employers

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

class EmailService:
    def __init__(self):
        # For testing, we'll use a fake SMTP server
        # In production, you'd use real email credentials
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.test_mode = True  # Set to False for real emails
        
        print("✅ Email service initialized! (Test mode: Send to console)")
    
    def send_candidate_match_notification(self, candidate_email, candidate_name, job_title, company, match_score, hiring_manager=None):
        """Send email to candidate when they get matched with a job"""
        
        subject = f"🎯 Great News! You're a Top Match for {job_title} at {company}"
        
        # Beautiful HTML email template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .match-score {{ background: #28a745; color: white; padding: 10px 20px; border-radius: 20px; display: inline-block; font-weight: bold; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                .button {{ background: #007bff; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎯 Job Match Found!</h1>
                    <p>Your profile perfectly matches an exciting opportunity</p>
                </div>
                <div class="content">
                    <h2>Hello {candidate_name}!</h2>
                    
                    <p>Our AI matching system has identified you as a <strong>top candidate</strong> for:</p>
                    
                    <div style="background: white; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea;">
                        <h3 style="margin-top: 0;">{job_title}</h3>
                        <p><strong>Company:</strong> {company}</p>
                        <p><strong>Match Score:</strong> <span class="match-score">{match_score:.1%}</span></p>
                    </div>
                    
                    <p>This means your skills and experience are <strong>highly relevant</strong> for this position!</p>
                    
                    <div style="text-align: center;">
                        <a href="#" class="button">View Job Details</a>
                    </div>
                    
                    <p><strong>Next Steps:</strong></p>
                    <ul>
                        <li>The employer will review your profile</li>
                        <li>You may be contacted for an interview</li>
                        <li>Keep your profile updated for more matches</li>
                    </ul>
                    
                    <p>Best regards,<br>AI Job Matcher Team</p>
                </div>
                <div class="footer">
                    <p>This email was sent by AI Job Matcher • {datetime.now().strftime('%Y-%m-%d')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version for email clients that don't support HTML
        text_content = f"""
        JOB MATCH NOTIFICATION
        
        Hello {candidate_name}!
        
        Great news! You've been matched with a job opportunity:
        
        Position: {job_title}
        Company: {company}
        Match Score: {match_score:.1%}
        
        The employer will review your profile and may contact you for an interview.
        
        Best regards,
        AI Job Matcher Team
        {datetime.now().strftime('%Y-%m-%d')}
        """
        
        if self.test_mode:
            # In test mode, just print to console
            print("\n" + "="*60)
            print("📧 EMAIL NOTIFICATION (TEST MODE)")
            print("="*60)
            print(f"To: {candidate_email}")
            print(f"Subject: {subject}")
            print(f"Body:\n{text_content}")
            print("="*60)
            return True
        else:
            # Real email sending code (commented out for safety)
            try:
                # You would implement real email sending here
                # msg = MIMEMultipart()
                # msg['From'] = self.email_from
                # msg['To'] = candidate_email
                # msg['Subject'] = subject
                # 
                # # Add HTML and plain text versions
                # text_part = MIMEText(text_content, 'plain')
                # html_part = MIMEText(html_content, 'html')
                # msg.attach(text_part)
                # msg.attach(html_part)
                # 
                # # Send email
                # server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                # server.starttls()
                # server.login(self.email_username, self.email_password)
                # server.send_message(msg)
                # server.quit()
                
                print(f"📧 Real email would be sent to: {candidate_email}")
                return True
            except Exception as e:
                print(f"❌ Failed to send email: {e}")
                return False
    
    def send_employer_match_notification(self, employer_email, job_title, top_candidates):
        """Send email to employer with top candidate matches"""
        
        subject = f"🏆 Top Candidates Found for {job_title}"
        
        candidates_list = ""
        for candidate in top_candidates[:3]:  # Top 3 candidates
            candidates_list += f"""
            <div style="background: white; margin: 10px 0; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
                <h4 style="margin: 0 0 10px 0;">{candidate['name']}</h4>
                <p><strong>Match Score:</strong> {candidate['score']:.1%}</p>
                <p><strong>Skills:</strong> {', '.join(candidate['skills'][:5])}</p>
                <p><strong>Experience:</strong> {candidate.get('experience_years', 'N/A')} years</p>
            </div>
            """
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏆 Top Candidates Found!</h1>
                    <p>AI-powered matching for {job_title}</p>
                </div>
                <div class="content">
                    <h2>Hello Hiring Manager!</h2>
                    
                    <p>Our AI system has identified <strong>excellent candidates</strong> for your position:</p>
                    <h3>"{job_title}"</h3>
                    
                    <div style="margin: 20px 0;">
                        {candidates_list}
                    </div>
                    
                    <p><strong>Next Steps:</strong></p>
                    <ul>
                        <li>Review candidate profiles in your dashboard</li>
                        <li>Schedule interviews with top matches</li>
                        <li>Contact candidates directly</li>
                    </ul>
                    
                    <div style="text-align: center; margin: 20px 0;">
                        <a href="#" style="background: #007bff; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">View Dashboard</a>
                    </div>
                    
                    <p>Best regards,<br>AI Job Matcher Team</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        text_content = f"""
        TOP CANDIDATES FOUND FOR {job_title}
        
        Hello Hiring Manager!
        
        Our AI system has found excellent candidates for your position "{job_title}":
        
        """
        
        for i, candidate in enumerate(top_candidates[:3], 1):
            text_content += f"""
        Candidate {i}: {candidate['name']}
        Match Score: {candidate['score']:.1%}
        Skills: {', '.join(candidate['skills'][:5])}
        Experience: {candidate.get('experience_years', 'N/A')} years
        
        """
        
        text_content += f"""
        Next Steps:
        - Review candidate profiles in your dashboard
        - Schedule interviews with top matches
        - Contact candidates directly
        
        Best regards,
        AI Job Matcher Team
        {datetime.now().strftime('%Y-%m-%d')}
        """
        
        if self.test_mode:
            print("\n" + "="*60)
            print("📧 EMPLOYER NOTIFICATION (TEST MODE)")
            print("="*60)
            print(f"To: {employer_email}")
            print(f"Subject: {subject}")
            print(f"Body:\n{text_content}")
            print("="*60)
            return True
        else:
            print(f"📧 Real employer email would be sent to: {employer_email}")
            return True

def main():
    """Test the email service"""
    email_service = EmailService()
    
    # Test candidate notification
    email_service.send_candidate_match_notification(
        candidate_email="candidate@example.com",
        candidate_name="John Smith", 
        job_title="Senior Python Developer",
        company="TechCorp Inc",
        match_score=0.85
    )
    
    # Test employer notification
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

if __name__ == "__main__":
    main()