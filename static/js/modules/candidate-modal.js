// 🎯 CANDIDATE MODAL MANAGEMENT - Enhanced with Quality Assessment
// Handles candidate creation with quality flags and improvement suggestions

class CandidateModal {
    constructor() {
        this.modal = document.getElementById('addCandidateModal');
        this.currentMethod = 'upload';
        this.parsedData = null;
        this.initialized = false;
    }

    init() {
        if (this.initialized) return;
        
        this.setupEventListeners();
        this.initialized = true;
        console.log('✅ Candidate modal initialized with quality assessment');
    }

    setupEventListeners() {
        // Method tab switching
        document.querySelectorAll('.input-method-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchMethod(e.target.dataset.method);
            });
        });

        // Modal controls
        document.getElementById('closeCandidateModal').addEventListener('click', () => this.close());
        document.getElementById('cancelCandidate').addEventListener('click', () => this.close());
        document.getElementById('saveCandidate').addEventListener('click', () => this.saveCandidate());

        // Parse actions
        document.getElementById('parseResumeText').addEventListener('click', () => this.parseText());
        
        // File upload setup
        this.setupFileUpload();
        
        // Quality improvement actions
        this.setupQualityActions();
    }

    setupQualityActions() {
        // These will be dynamically created in renderQualityWarnings
    }

    switchMethod(method) {
        this.currentMethod = method;
        
        // Update active tab styling
        document.querySelectorAll('.input-method-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.method === method);
        });

        // Show corresponding content
        document.querySelectorAll('.input-method-content').forEach(content => {
            content.classList.toggle('active', content.id === `${method}Method`);
        });

        // Reset parsed data when switching methods
        this.hideParsedReview();
        this.hideQualityWarnings();
    }

    setupFileUpload() {
        const uploadZone = document.getElementById('resumeUploadZone');
        const fileInput = uploadZone.querySelector('.file-input');

        // Click to open file dialog
        uploadZone.addEventListener('click', () => fileInput.click());
        
        // Handle file selection
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFileUpload(e.target.files[0]);
            }
        });

        // Drag and drop handlers
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadZone.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadZone.addEventListener(eventName, () => {
                uploadZone.classList.add('drop-zone--active');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadZone.addEventListener(eventName, () => {
                uploadZone.classList.remove('drop-zone--active');
            }, false);
        });

        // Handle file drop
        uploadZone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileUpload(files[0]);
            }
        }, false);
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    async handleFileUpload(file) {
        if (!file) return;

        // Validate file type
        const validTypes = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain'
        ];
        
        if (!validTypes.includes(file.type) && !file.name.match(/\.(pdf|doc|docx|txt)$/i)) {
            UIUtils.showNotification('Please select a valid PDF, DOC, DOCX, or TXT file', 'error');
            return;
        }

        try {
            UIUtils.showNotification('Reading file...', 'info');
            const content = await this.readFileContent(file);
            this.parseResume(content);
        } catch (error) {
            UIUtils.showNotification('Failed to read file', 'error');
        }
    }

    async parseText() {
        const text = document.getElementById('resumeText').value;
        if (!text.trim()) {
            UIUtils.showNotification('Please enter resume text', 'error');
            return;
        }
        this.parseResume(text);
    }

    async parseResume(text) {
        try {
            UIUtils.showNotification('Parsing resume with AI...', 'info');
            
            const response = await api.post('/api/parse-resume', { resume_text: text });
            
            if (response.success) {
                this.parsedData = response.candidate_data;
                this.showParsedReview();
                
                // Show quality assessment
                this.showQualityAssessment();
                
                UIUtils.showNotification('Resume parsed successfully!', 'success');
            } else {
                throw new Error(response.error);
            }
        } catch (error) {
            console.error('Parsing error:', error);
            UIUtils.showNotification('Failed to parse resume', 'error');
        }
    }

    showParsedReview() {
        document.getElementById('parsedReview').style.display = 'block';
        document.getElementById('saveCandidate').style.display = 'block';
        
        // Populate parsed fields for editing
        const fieldsContainer = document.getElementById('parsedFields');
        fieldsContainer.innerHTML = this.renderParsedFields();
    }

    showQualityAssessment() {
        // Always show quality indicator
        this.renderQualityIndicator();
        
        // Show warnings for low quality resumes
        if (this.parsedData.quality_assessment && 
            (this.parsedData.quality_assessment.quality_level === 'low' || 
             this.parsedData.quality_assessment.quality_level === 'very_low')) {
            this.renderQualityWarnings();
        }
    }

    renderQualityIndicator() {
        const quality = this.parsedData.quality_assessment;
        if (!quality) return;
        
        const indicatorHtml = `
            <div class="quality-indicator quality-indicator--${quality.quality_level}">
                <div class="quality-indicator__header">
                    <span class="quality-indicator__label">Quality Assessment</span>
                    <span class="quality-indicator__score">${Math.round(quality.quality_score * 100)}%</span>
                </div>
                <div class="quality-indicator__level">
                    <span class="quality-badge quality-badge--${quality.quality_level}">
                        ${this.formatQualityLevel(quality.quality_level)}
                    </span>
                </div>
            </div>
        `;
        
        const container = document.getElementById('qualityIndicator');
        if (container) {
            container.innerHTML = indicatorHtml;
            container.style.display = 'block';
        }
    }

    renderQualityWarnings() {
        const quality = this.parsedData.quality_assessment;
        if (!quality || (quality.quality_level !== 'low' && quality.quality_level !== 'very_low')) {
            return;
        }
        
        const warningHtml = `
            <div class="quality-warning quality-warning--${quality.quality_level}">
                <div class="warning-header">
                    <svg class="icon" width="20" height="20" fill="none" stroke="currentColor">
                        <path d="M12 2L2 22h20L12 2z"></path>
                        <path d="M12 8v6"></path>
                        <circle cx="12" cy="17" r="1"></circle>
                    </svg>
                    <h4>Resume Needs Improvement</h4>
                </div>
                <div class="warning-content">
                    <div class="warning-metrics">
                        <div class="warning-metric">
                            <span class="metric-label">Quality Score:</span>
                            <span class="metric-value metric-value--${quality.quality_level}">
                                ${Math.round(quality.quality_score * 100)}%
                            </span>
                        </div>
                        <div class="warning-metric">
                            <span class="metric-label">Issues Found:</span>
                            <span class="metric-value">
                                ${quality.quality_issues.length}
                            </span>
                        </div>
                    </div>
                    
                    ${quality.quality_issues.length > 0 ? `
                    <div class="warning-issues">
                        <h5>Issues Found:</h5>
                        <ul>
                            ${quality.quality_issues.map(issue => `<li>${issue}</li>`).join('')}
                        </ul>
                    </div>
                    ` : ''}
                    
                    <div class="improvement-suggestions">
                        <h5>Suggestions for Improvement:</h5>
                        <ul>
                            ${quality.suggestions_for_improvement.map(suggestion => `<li>${suggestion}</li>`).join('')}
                        </ul>
                    </div>
                </div>
                <div class="warning-actions">
                    <button onclick="candidateModal.showQualityGuide()" class="btn btn--outline">
                        📋 View Quality Guide
                    </button>
                    <button onclick="candidateModal.rewriteResume()" class="btn btn--primary">
                        ✏️ Improve Resume
                    </button>
                    <button onclick="candidateModal.continueAnyway()" class="btn btn--secondary">
                        ➡️ Continue Anyway
                    </button>
                </div>
            </div>
        `;
        
        document.getElementById('qualityWarnings').innerHTML = warningHtml;
        document.getElementById('qualityWarnings').style.display = 'block';
    }

    renderParsedFields() {
        if (!this.parsedData) return '';
        
        const quality = this.parsedData.quality_assessment || {};
        
        return `
            <div class="form-grid">
                <div class="form-group">
                    <label>Full Name</label>
                    <input type="text" value="${this.parsedData.name || ''}" class="form-input" data-field="name">
                    <span class="confidence-indicator ${this.getConfidenceClass(0.8)}">
                        80%
                    </span>
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" value="${this.parsedData.email || ''}" class="form-input" data-field="email">
                    <span class="confidence-indicator ${this.getConfidenceClass(0.9)}">
                        90%
                    </span>
                </div>
                <div class="form-group">
                    <label>Location</label>
                    <input type="text" value="${this.parsedData.location || ''}" class="form-input" data-field="location">
                    <span class="confidence-indicator ${this.getConfidenceClass(0.7)}">
                        70%
                    </span>
                </div>
                <div class="form-group">
                    <label>Years of Experience</label>
                    <input type="number" value="${this.parsedData.experience_years || 0}" class="form-input" min="0" max="50" data-field="experience_years">
                    <span class="confidence-indicator ${this.getConfidenceClass(0.6)}">
                        60%
                    </span>
                </div>
                
                <!-- Enhanced Data Display -->
                ${this.parsedData.growth_metrics ? `
                <div class="form-group full-width">
                    <label>Career & Growth Profile</label>
                    <div class="enhanced-data-display">
                        <div class="enhanced-data-item">
                            <span class="enhanced-label">Career Stage:</span>
                            <span class="enhanced-value">${this.formatCareerStage(this.parsedData.growth_metrics.career_stage)}</span>
                        </div>
                        <div class="enhanced-data-item">
                            <span class="enhanced-label">Growth Potential:</span>
                            <span class="enhanced-value">${Math.round(this.parsedData.growth_metrics.growth_potential_score)}%</span>
                        </div>
                        <div class="enhanced-data-item">
                            <span class="enhanced-label">Role Archetype:</span>
                            <span class="enhanced-value">${this.formatArchetype(this.parsedData.growth_metrics.career_archetype)}</span>
                        </div>
                    </div>
                    <span class="confidence-indicator ${this.getConfidenceClass(0.7)}">
                        Enhanced Data: 70%
                    </span>
                </div>
                ` : ''}
                
                <div class="form-group full-width">
                    <label>Skills</label>
                    <div class="skills-display">
                        ${(this.parsedData.skills || []).map(skill => 
                            `<span class="skill-tag">${skill}</span>`
                        ).join('')}
                        ${(!this.parsedData.skills || this.parsedData.skills.length === 0) ? 
                            '<span class="text-muted">No skills extracted</span>' : ''}
                    </div>
                    <span class="confidence-indicator ${this.getConfidenceClass(0.8)}">
                        ${Math.round((this.parsedData.skills || []).length / 10 * 100)}%
                    </span>
                </div>
                <div class="form-group full-width">
                    <label>Education</label>
                    <input type="text" value="${this.parsedData.education || ''}" class="form-input" data-field="education">
                    <span class="confidence-indicator ${this.getConfidenceClass(0.7)}">
                        70%
                    </span>
                </div>
                <div class="form-group full-width">
                    <label>Professional Profile</label>
                    <textarea class="form-textarea" rows="4" data-field="profile">${this.parsedData.profile || ''}</textarea>
                </div>

                <!-- ADD THIS SECTION: Complete Resume Text Display -->
                ${this.parsedData.original_resume_text ? `
                <div class="form-group full-width">
                    <label>Complete Resume Text</label>
                    <div class="cv-details-content" style="max-height: 200px; overflow-y: auto; font-family: 'Courier New', monospace; font-size: 0.85rem; line-height: 1.5; color: var(--gray-700); white-space: pre-wrap; word-wrap: break-word; padding: 1rem; background: var(--gray-50); border: 1px solid var(--gray-200); border-radius: 6px;">
                        ${this.parsedData.original_resume_text}
                    </div>
                    <span class="confidence-indicator confidence-high">
                        Original Resume
                    </span>
                </div>
                ` : ''}
            </div>
        `;
    }

    getConfidenceClass(score) {
        if (score >= 0.8) return 'confidence-high';
        if (score >= 0.6) return 'confidence-medium';
        return 'confidence-low';
    }

    formatQualityLevel(level) {
        const levels = {
            'very_low': 'Very Low',
            'low': 'Low', 
            'medium': 'Medium',
            'high': 'High'
        };
        return levels[level] || level;
    }

    formatCareerStage(stage) {
        const stages = {
            'early_career': 'Early Career (0-3 years)',
            'mid_career': 'Mid Career (3-8 years)',
            'executive': 'Executive (8+ years)'
        };
        return stages[stage] || stage;
    }

    formatArchetype(archetype) {
        const archetypes = {
            'high_growth_ic': 'High Growth Individual Contributor',
            'strategic_executive': 'Strategic Executive',
            'technical_specialist': 'Technical Specialist',
            'portfolio_leader': 'Portfolio Leader',
            'career_starter': 'Career Starter',
            'growth_track_ic': 'Growth Track IC'
        };
        return archetypes[archetype] || archetype;
    }

    hideParsedReview() {
        document.getElementById('parsedReview').style.display = 'none';
        document.getElementById('saveCandidate').style.display = 'none';
        this.parsedData = null;
    }

    hideQualityWarnings() {
        document.getElementById('qualityWarnings').style.display = 'none';
        document.getElementById('qualityIndicator').style.display = 'none';
    }

    // Quality Improvement Actions
    showQualityGuide() {
        const guideHtml = `
            <div class="quality-guide">
                <div class="guide-header">
                    <h3>📋 Resume Quality Guide</h3>
                    <button onclick="this.parentElement.parentElement.remove()" class="btn-close">×</button>
                </div>
                <div class="guide-content">
                    <div class="guide-section">
                        <h4>✅ Excellent Resume Includes:</h4>
                        <ul>
                            <li>Clear contact information (name, email, phone)</li>
                            <li>500+ characters of detailed content</li>
                            <li>Specific work experience with company names and durations</li>
                            <li>5+ specific technical and soft skills</li>
                            <li>Education background and qualifications</li>
                            <li>Professional summary or objective</li>
                            <li>Clear career progression and achievements</li>
                            <li>Quantifiable results and accomplishments</li>
                        </ul>
                    </div>
                    
                    <div class="guide-section">
                        <h4>❌ Poor Resume Signs:</h4>
                        <ul>
                            <li>Less than 200 characters total</li>
                            <li>Missing contact information</li>
                            <li>No specific work experience listed</li>
                            <li>Fewer than 3 skills mentioned</li>
                            <li>No education information</li>
                            <li>Generic descriptions without specifics</li>
                            <li>Missing dates and durations</li>
                        </ul>
                    </div>
                    
                    <div class="guide-section">
                        <h4>🎯 Best Practices:</h4>
                        <ul>
                            <li>Use specific numbers and metrics (e.g., "Increased efficiency by 30%")</li>
                            <li>Include both technical and soft skills</li>
                            <li>List relevant certifications and education</li>
                            <li>Use action verbs to describe accomplishments</li>
                            <li>Tailor content to target job roles</li>
                            <li>Include keywords from job descriptions</li>
                            <li>Keep formatting clean and professional</li>
                        </ul>
                    </div>
                </div>
                <div class="guide-actions">
                    <button onclick="candidateModal.rewriteResume()" class="btn btn--primary">
                        ✏️ Improve Using This Guide
                    </button>
                    <button onclick="this.parentElement.parentElement.remove()" class="btn btn--secondary">
                        Close Guide
                    </button>
                </div>
            </div>
        `;
        
        // Create overlay for guide
        const overlay = document.createElement('div');
        overlay.className = 'modal-overlay';
        overlay.innerHTML = guideHtml;
        document.body.appendChild(overlay);
    }

    rewriteResume() {
        // Clear current parsed data and return to text input
        this.hideParsedReview();
        this.hideQualityWarnings();
        this.switchMethod('paste');
        
        // Pre-fill the textarea with the original text for editing
        const resumeTextarea = document.getElementById('resumeText');
        if (resumeTextarea && this.parsedData) {
            resumeTextarea.value = this.parsedData.original_text || '';
            resumeTextarea.focus();
        }
        
        UIUtils.showNotification('Please improve the resume using the quality guide', 'info');
    }

    continueAnyway() {
        // Just hide the warnings and continue with saving
        this.hideQualityWarnings();
        UIUtils.showNotification('Proceeding with candidate creation despite quality issues', 'warning');
    }

    async saveCandidate() {
        try {
            UIUtils.showNotification('Saving candidate to database...', 'info');
            
            let candidateData = {};
            
            if (this.parsedData) {
                // Robust field collection using data attributes
                const fieldsContainer = document.getElementById('parsedFields');
                
                // Get each field by its data-field attribute
                const nameInput = fieldsContainer.querySelector('[data-field="name"]');
                const emailInput = fieldsContainer.querySelector('[data-field="email"]');
                const locationInput = fieldsContainer.querySelector('[data-field="location"]');
                const experienceInput = fieldsContainer.querySelector('[data-field="experience_years"]');
                const educationInput = fieldsContainer.querySelector('[data-field="education"]');
                const profileTextarea = fieldsContainer.querySelector('[data-field="profile"]');
                
                // Validate required fields exist
                if (!nameInput || !emailInput) {
                    throw new Error('Required form fields are missing');
                }
                
                candidateData = {
                    // Existing fields
                    name: nameInput.value.trim(),
                    email: emailInput.value.trim(),
                    location: locationInput ? locationInput.value.trim() : this.parsedData.location || '',
                    experience_years: experienceInput ? parseInt(experienceInput.value) || 0 : this.parsedData.experience_years || 0,
                    education: educationInput ? educationInput.value.trim() : this.parsedData.education || '',
                    skills: this.parsedData.skills || [],
                    profile: profileTextarea ? profileTextarea.value.trim() : this.parsedData.profile || '',
                    cultural_attributes: this.parsedData.cultural_attributes || {},
                    
                    // FIXED: Get original resume text from parsed data
                    original_resume_text: this.parsedData.original_text || this.parsedData.original_resume_text || '',

                    // Enhanced data
                    growth_metrics: this.parsedData.growth_metrics || {},
                    career_metrics: this.parsedData.career_metrics || {},
                    quality_assessment: this.parsedData.quality_assessment || {},
                    extraction_method: this.parsedData.extraction_method || 'unknown'
                };
            } else if (this.currentMethod === 'form') {
                // Use quick form data
                const form = document.getElementById('quickCandidateForm');
                const skills = form.skills.value.split(',').map(skill => skill.trim()).filter(skill => skill);
                
                candidateData = {
                    name: form.name.value.trim(),
                    email: form.email.value.trim(),
                    location: form.location.value.trim(),
                    experience_years: parseInt(form.experience_years.value) || 0,
                    education: '',
                    skills: skills,
                    profile: form.profile.value.trim(),
                    cultural_attributes: {},
                    original_resume_text: '', // Manual entries don't have resume text
                    // Default enhanced data for manual entries
                    growth_metrics: this._getDefaultGrowthMetrics(),
                    career_metrics: this._getDefaultCareerMetrics(),
                    quality_assessment: {
                        quality_score: 0.5,
                        quality_level: 'medium',
                        quality_issues: ['Manually entered candidate'],
                        missing_required_fields: [],
                        missing_recommended_fields: [],
                        suggestions_for_improvement: []
                    },
                    extraction_method: 'manual'
                };
            } else {
                throw new Error('No candidate data to save - please parse or enter candidate information first');
            }
            
            // Validate required fields
            if (!candidateData.name) {
                throw new Error('Candidate name is required');
            }
            if (!candidateData.email) {
                throw new Error('Email is required');
            }
            
            const response = await api.post('/api/create-candidate', { candidate_data: candidateData });
            
            if (response.success) {
                const qualityLevel = candidateData.quality_assessment?.quality_level || 'unknown';
                UIUtils.showNotification(`Candidate "${candidateData.name}" created successfully! (Quality: ${qualityLevel})`, 'success');
                this.close();
                
                // Refresh candidates list
                if (window.candidatesModule) {
                    candidatesModule.displayCandidates(document.getElementById('candidatesContainer'));
                }
            } else {
                throw new Error(response.error);
            }
            
        } catch (error) {
            console.error('Save candidate error:', error);
            UIUtils.showNotification(`Failed to save candidate: ${error.message}`, 'error');
        }
    }

    _getDefaultGrowthMetrics() {
        return {
            growth_potential_score: 0.5,
            growth_dimensions: {
                vertical_growth: 0.5,
                scope_growth: 0.5,
                impact_growth: 0.5,
                adaptability: 0.5,
                leadership_velocity: 0.3
            },
            career_archetype: 'technical_specialist',
            career_stage: 'mid_career',
            executive_potential: 0.3,
            strategic_mobility: 0.5,
            analysis_rationale: 'Manually entered candidate',
            promotion_velocity: 0,
            max_role_level: 2
        };
    }

    _getDefaultCareerMetrics() {
        return {
            average_tenure_months: 24,
            career_progression_slope: 0.1,
            leadership_experience: false,
            number_of_companies: 1,
            role_variety_score: 0.5
        };
    }

    readFileContent(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = (e) => reject(e);
            reader.readAsText(file);
        });
    }

    open() {
        this.modal.classList.add('modal--active');
        // Reset form when opening
        this.hideParsedReview();
        this.hideQualityWarnings();
        document.getElementById('resumeText').value = '';
    }

    close() {
        this.modal.classList.remove('modal--active');
        this.hideParsedReview();
        this.hideQualityWarnings();
    }
}

// Global instance
window.candidateModal = new CandidateModal();