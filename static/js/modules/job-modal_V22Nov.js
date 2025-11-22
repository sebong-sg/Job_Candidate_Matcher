// 🎯 JOB MODAL MANAGEMENT - Enhanced with Quality Assessment
// Handles job creation with quality flags and improvement suggestions

class JobModal {
    constructor() {
        this.modal = document.getElementById('addJobModal');
        this.currentMethod = 'upload';
        this.parsedData = null;
        this.initialized = false;
    }

    init() {
        if (this.initialized) return;
        
        this.setupEventListeners();
        this.initialized = true;
        console.log('✅ Job modal initialized with quality assessment');
    }

    setupEventListeners() {
        // Method tab switching
        document.querySelectorAll('.input-method-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchMethod(e.target.dataset.method);
            });
        });

        // Modal controls
        document.getElementById('closeJobModal').addEventListener('click', () => this.close());
        document.getElementById('cancelJob').addEventListener('click', () => this.close());
        document.getElementById('saveJob').addEventListener('click', () => this.saveJob());

        // Parse actions
        document.getElementById('parseJdText').addEventListener('click', () => this.parseText());
        
        // File upload setup
        this.setupFileUpload();
        
        // NEW: Quality improvement actions
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
        const uploadZone = document.getElementById('jdUploadZone');
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
            this.parseJobDescription(content);
        } catch (error) {
            UIUtils.showNotification('Failed to read file', 'error');
        }
    }

    async parseText() {
        const text = document.getElementById('jdText').value;
        if (!text.trim()) {
            UIUtils.showNotification('Please enter job description text', 'error');
            return;
        }
        this.parseJobDescription(text);
    }

    async parseJobDescription(text) {
        try {
            UIUtils.showNotification('Parsing job description with AI...', 'info');
            
            const response = await api.post('/api/parse-job-description', { job_text: text });
            
            if (response.success) {
                this.parsedData = response.job_data;
                this.showParsedReview();
                
                // NEW: Show quality assessment
                this.showQualityAssessment();
                
                UIUtils.showNotification('Job description parsed successfully! Please verify.', 'success');
            } else {
                throw new Error(response.error);
            }
        } catch (error) {
            console.error('Parsing error:', error);
            UIUtils.showNotification('Failed to parse job description', 'error');
        }
    }

    showParsedReview() {
        document.getElementById('parsedReview').style.display = 'block';
        document.getElementById('saveJob').style.display = 'block';
        
        // Populate parsed fields for editing
        const fieldsContainer = document.getElementById('parsedFields');
        fieldsContainer.innerHTML = this.renderParsedFields();
    }

    showQualityAssessment() {
        // NEW: Always show quality indicator
        this.renderQualityIndicator();
        
        // Show warnings for low quality JDs
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
                    <h4>Job Description Needs Improvement</h4>
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
                            <span class="metric-label">Missing Fields:</span>
                            <span class="metric-value">
                                ${quality.missing_required_fields.length + quality.missing_recommended_fields.length}
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
                    <button onclick="jobModal.showQualityGuide()" class="btn btn--outline">
                        📋 View Quality Guide
                    </button>
                    <button onclick="jobModal.rewriteJD()" class="btn btn--primary">
                        ✏️ Rewrite Job Description
                    </button>
                    <button onclick="jobModal.continueAnyway()" class="btn btn--secondary">
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
        
        const confidence = this.parsedData.confidence_scores || {};
        const quality = this.parsedData.quality_assessment || {};
        
        return `
            <div class="form-grid">
                <div class="form-group">
                    <label>Job Title</label>
                    <input type="text" value="${this.parsedData.title || ''}" class="form-input" data-field="title">
                    <span class="confidence-indicator ${this.getConfidenceClass(confidence.title)}">
                        ${Math.round(confidence.title * 100)}%
                    </span>
                </div>
                <div class="form-group">
                    <label>Company</label>
                    <input type="text" value="${this.parsedData.company || ''}" class="form-input" data-field="company">
                    <span class="confidence-indicator ${this.getConfidenceClass(confidence.company)}">
                        ${Math.round(confidence.company * 100)}%
                    </span>
                </div>
                <div class="form-group">
                    <label>Location</label>
                    <input type="text" value="${this.parsedData.location || ''}" class="form-input" data-field="location">
                    <span class="confidence-indicator ${this.getConfidenceClass(confidence.location)}">
                        ${Math.round(confidence.location * 100)}%
                    </span>
                </div>
                <div class="form-group">
                    <label>Experience Required (years)</label>
                    <input type="number" value="${this.parsedData.experience_required || 0}" class="form-input" min="0" max="50" data-field="experience">
                    <span class="confidence-indicator ${this.getConfidenceClass(confidence.experience)}">
                        ${Math.round(confidence.experience * 100)}%
                    </span>
                </div>
                <div class="form-group">
                    <label>Employment Type</label>
                    <select class="form-select" data-field="employment_type">
                        <option value="Full-time" ${this.parsedData.employment_type === 'Full-time' ? 'selected' : ''}>Full-time</option>
                        <option value="Part-time" ${this.parsedData.employment_type === 'Part-time' ? 'selected' : ''}>Part-time</option>
                        <option value="Contract" ${this.parsedData.employment_type === 'Contract' ? 'selected' : ''}>Contract</option>
                        <option value="Remote" ${this.parsedData.employment_type === 'Remote' ? 'selected' : ''}>Remote</option>
                        <option value="Hybrid" ${this.parsedData.employment_type === 'Hybrid' ? 'selected' : ''}>Hybrid</option>
                    </select>
                    <span class="confidence-indicator ${this.getConfidenceClass(confidence.employment_type)}">
                        ${Math.round(confidence.employment_type * 100)}%
                    </span>
                </div>
                
                <!-- NEW: Enhanced Data Display -->
                ${this.parsedData.growth_requirements ? `
                <div class="form-group full-width">
                    <label>Career Stage & Growth</label>
                    <div class="enhanced-data-display">
                        <div class="enhanced-data-item">
                            <span class="enhanced-label">Target Career Stage:</span>
                            <span class="enhanced-value">${this.formatCareerStage(this.parsedData.growth_requirements.target_career_stage)}</span>
                        </div>
                        <div class="enhanced-data-item">
                            <span class="enhanced-label">Role Archetype:</span>
                            <span class="enhanced-value">${this.formatArchetype(this.parsedData.growth_requirements.role_archetype)}</span>
                        </div>
                        <div class="enhanced-data-item">
                            <span class="enhanced-label">Scope Level:</span>
                            <span class="enhanced-value">${this.formatScopeLevel(this.parsedData.growth_requirements.scope_level_required)}</span>
                        </div>
                    </div>
                    <span class="confidence-indicator ${this.getConfidenceClass(confidence.enhanced_data)}">
                        Enhanced Data: ${Math.round(confidence.enhanced_data * 100)}%
                    </span>
                </div>
                ` : ''}
                
                <div class="form-group full-width">
                    <label>Required Skills</label>
                    <div class="skills-display">
                        ${(this.parsedData.required_skills || []).map(skill => 
                            `<span class="skill-tag">${skill}</span>`
                        ).join('')}
                        ${(!this.parsedData.required_skills || this.parsedData.required_skills.length === 0) ? 
                            '<span class="text-muted">No skills extracted</span>' : ''}
                    </div>
                    <span class="confidence-indicator ${this.getConfidenceClass(confidence.skills)}">
                        ${Math.round(confidence.skills * 100)}%
                    </span>
                </div>

                <div class="form-group full-width">
                    <label>Job Profile</label>
                    <textarea class="form-textarea" rows="4" data-field="summary">${this.parsedData.summary || ''}</textarea>
                </div>

                <div class="form-group full-width">
                    <label>Job Description</label>
                    <textarea class="form-textarea" rows="4" data-field="description">${this.parsedData.description || ''}</textarea>
                </div>
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
            'portfolio_leader': 'Portfolio Leader'
        };
        return archetypes[archetype] || archetype;
    }

    formatScopeLevel(level) {
        const levels = {
            1: 'Individual Contributor',
            2: 'Team Lead',
            3: 'Department Head', 
            4: 'Organization Lead'
        };
        return levels[level] || `Level ${level}`;
    }

    hideParsedReview() {
        document.getElementById('parsedReview').style.display = 'none';
        document.getElementById('saveJob').style.display = 'none';
        this.parsedData = null;
    }

    hideQualityWarnings() {
        document.getElementById('qualityWarnings').style.display = 'none';
        document.getElementById('qualityIndicator').style.display = 'none';
    }

    // NEW: Quality Improvement Actions
    showQualityGuide() {
        const guideHtml = `
            <div class="quality-guide">
                <div class="guide-header">
                    <h3>📋 Job Description Quality Guide</h3>
                    <button onclick="this.parentElement.parentElement.remove()" class="btn-close">×</button>
                </div>
                <div class="guide-content">
                    <div class="guide-section">
                        <h4>✅ Excellent Job Description Includes:</h4>
                        <ul>
                            <li>Clear, specific job title and company name</li>
                            <li>500+ characters detailed description</li>
                            <li>5-7 specific responsibilities as bullet points</li>
                            <li>5-7 required skills (both technical and soft skills)</li>
                            <li>Specific years of experience required</li>
                            <li>Education and certification requirements</li>
                            <li>Clear location/remote work specifications</li>
                            <li>Career growth and development opportunities</li>
                        </ul>
                    </div>
                    
                    <div class="guide-section">
                        <h4>❌ Poor Job Description Signs:</h4>
                        <ul>
                            <li>Less than 200 characters total</li>
                            <li>Vague language ("etc.", "and more", "similar experience")</li>
                            <li>No specific skills listed</li>
                            <li>Missing experience requirements</li>
                            <li>No clear sections (Responsibilities, Requirements)</li>
                            <li>Generic company description</li>
                        </ul>
                    </div>
                    
                    <div class="guide-section">
                        <h4>🎯 Best Practices:</h4>
                        <ul>
                            <li>Use specific numbers (e.g., "3+ years of Python experience")</li>
                            <li>Separate required skills from preferred skills</li>
                            <li>Include both technical and soft skills</li>
                            <li>Mention team structure and reporting lines</li>
                            <li>Describe company culture and work environment</li>
                            <li>Include specific projects or technologies used</li>
                        </ul>
                    </div>
                </div>
                <div class="guide-actions">
                    <button onclick="jobModal.rewriteJD()" class="btn btn--primary">
                        ✏️ Rewrite Using This Guide
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

    rewriteJD() {
        // Clear current parsed data and return to text input
        this.hideParsedReview();
        this.hideQualityWarnings();
        this.switchMethod('text');
        
        // Pre-fill the textarea with the original text for editing
        const jdTextarea = document.getElementById('jdText');
        if (jdTextarea && this.parsedData) {
            jdTextarea.value = this.parsedData.description;
            jdTextarea.focus();
        }
        
        UIUtils.showNotification('Please rewrite the job description using the quality guide', 'info');
    }

    continueAnyway() {
        // Just hide the warnings and continue with saving
        this.hideQualityWarnings();
        UIUtils.showNotification('Proceeding with job creation despite quality issues', 'warning');
    }

    async saveJob() {
        try {
            UIUtils.showNotification('Saving job to database...', 'info');
            
            let jobData = {};
            
            if (this.parsedData) {
                // Robust field collection using data attributes
                const fieldsContainer = document.getElementById('parsedFields');
                
                // Get each field by its data-field attribute
                const titleInput = fieldsContainer.querySelector('[data-field="title"]');
                const companyInput = fieldsContainer.querySelector('[data-field="company"]');
                const locationInput = fieldsContainer.querySelector('[data-field="location"]');
                const experienceInput = fieldsContainer.querySelector('[data-field="experience"]');
                const employmentSelect = fieldsContainer.querySelector('[data-field="employment_type"]');
                const descriptionTextarea = fieldsContainer.querySelector('[data-field="description"]');
                
                // Validate required fields exist
                if (!titleInput || !companyInput) {
                    throw new Error('Required form fields are missing');
                }
                
                jobData = {
                    // Existing fields
                    title: titleInput.value.trim(),
                    company: companyInput.value.trim(),
                    location: locationInput ? locationInput.value.trim() : this.parsedData.location || '',
                    experience_required: experienceInput ? parseInt(experienceInput.value) || 0 : this.parsedData.experience_required || 0,
                    job_type: employmentSelect ? employmentSelect.value : this.parsedData.employment_type || 'Full-time',
                    required_skills: this.parsedData.required_skills || [],
                    description: descriptionTextarea ? descriptionTextarea.value.trim() : this.parsedData.description || '',
                    cultural_attributes: this.parsedData.cultural_attributes || {},
                    // NEW: Enhanced data
                    growth_requirements: this.parsedData.growth_requirements || {},
                    skill_requirements: this.parsedData.skill_requirements || {},
                    career_progression: this.parsedData.career_progression || {},
                    quality_assessment: this.parsedData.quality_assessment || {},
                    confidence_scores: this.parsedData.confidence_scores || {}
                };
            } else if (this.currentMethod === 'form') {
                // Use quick form data
                const form = document.getElementById('quickJobForm');
                jobData = {
                    title: form.title.value.trim(),
                    company: form.company.value.trim(),
                    location: form.location.value.trim(),
                    description: form.description.value.trim(),
                    required_skills: [],
                    experience_required: parseInt(form.experience_required.value) || 0,
                    job_type: form.job_type.value,
                    cultural_attributes: {},
                    // NEW: Default enhanced data for manual entries
                    growth_requirements: this._getDefaultGrowthRequirements(),
                    skill_requirements: this._getDefaultSkillRequirements(),
                    career_progression: this._getDefaultCareerProgression(),
                    quality_assessment: {
                        quality_score: 0.5,
                        quality_level: 'medium',
                        quality_issues: ['Manually entered job description'],
                        missing_required_fields: [],
                        missing_recommended_fields: [],
                        suggestions_for_improvement: []
                    }
                };
            } else {
                throw new Error('No job data to save - please parse or enter job information first');
            }
            
            // Validate required fields
            if (!jobData.title) {
                throw new Error('Job title is required');
            }
            if (!jobData.company) {
                throw new Error('Company name is required');
            }
            
            const response = await api.post('/api/create-job', { job_data: jobData });
            
            if (response.success) {
                const qualityLevel = jobData.quality_assessment?.quality_level || 'unknown';
                UIUtils.showNotification(`Job "${jobData.title}" created successfully! (Quality: ${qualityLevel})`, 'success');
                this.close();
                
                // Refresh jobs list
                if (window.jobsModule) {
                    jobsModule.displayJobs(document.getElementById('jobsContainer'));
                }
            } else {
                throw new Error(response.error);
            }
            
        } catch (error) {
            console.error('Save job error:', error);
            UIUtils.showNotification(`Failed to save job: ${error.message}`, 'error');
        }
    }

    _getDefaultGrowthRequirements() {
        return {
            target_career_stage: 'mid_career',
            role_archetype: 'technical_specialist',
            scope_level_required: 1,
            executive_potential_required: 0.3,
            learning_expectations: 0.5,
            confidence: 0.3,
            has_clear_requirements: false
        };
    }

    _getDefaultSkillRequirements() {
        return {
            core_skills: [],
            secondary_skills: [],
            required_proficiency: {},
            skill_priority_weights: {},
            confidence: 0.3
        };
    }

    _getDefaultCareerProgression() {
        return {
            promotion_expectations: 'standard',
            strategic_mobility_preferred: 0.5,
            impact_scale_required: 0.5,
            confidence: 0.3
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
        document.getElementById('jdText').value = '';
    }

    close() {
        this.modal.classList.remove('modal--active');
        this.hideParsedReview();
        this.hideQualityWarnings();
    }
}

// Global instance
window.jobModal = new JobModal();