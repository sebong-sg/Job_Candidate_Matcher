// 🎯 JOB MODAL MANAGEMENT
// Handles job creation with multiple input methods:
// - JD File Upload
// - Text Paste & Parse  
// - Quick Form Entry

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
        console.log('✅ Job modal initialized');
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
                UIUtils.showNotification('Job description parsed successfully!', 'success');
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

    renderParsedFields() {
        if (!this.parsedData) return '';
        
        const confidence = this.parsedData.confidence_scores || {};
        
        return `
            <div class="form-grid">
                <div class="form-group">
                    <label>Job Title</label>
                    <input type="text" value="${this.parsedData.title || ''}" class="form-input">
                    <span class="confidence-indicator confidence-high">${Math.round(confidence.title * 100)}%</span>
                </div>
                <div class="form-group">
                    <label>Company</label>
                    <input type="text" value="${this.parsedData.company || ''}" class="form-input">
                    <span class="confidence-indicator confidence-medium">${Math.round(confidence.company * 100)}%</span>
                </div>
                <div class="form-group">
                    <label>Location</label>
                    <input type="text" value="${this.parsedData.location || ''}" class="form-input">
                </div>
                <div class="form-group">
                    <label>Experience Required (years)</label>
                    <input type="number" value="${this.parsedData.experience_required || 0}" class="form-input" min="0" max="50">
                    <span class="confidence-indicator confidence-medium">${Math.round(confidence.experience * 100)}%</span>
                </div>
                <div class="form-group">
                    <label>Employment Type</label>
                    <select class="form-select">
                        <option value="Full-time" ${this.parsedData.employment_type === 'Full-time' ? 'selected' : ''}>Full-time</option>
                        <option value="Part-time" ${this.parsedData.employment_type === 'Part-time' ? 'selected' : ''}>Part-time</option>
                        <option value="Contract" ${this.parsedData.employment_type === 'Contract' ? 'selected' : ''}>Contract</option>
                        <option value="Remote" ${this.parsedData.employment_type === 'Remote' ? 'selected' : ''}>Remote</option>
                    </select>
                </div>
                <div class="form-group full-width">
                    <label>Required Skills</label>
                    <div class="skills-display">
                        ${(this.parsedData.required_skills || []).map(skill => 
                            `<span class="skill-tag">${skill}</span>`
                        ).join('')}
                        ${(!this.parsedData.required_skills || this.parsedData.required_skills.length === 0) ? 
                            '<span class="text-muted">No skills extracted</span>' : ''}
                    </div>
                    <span class="confidence-indicator confidence-high">${Math.round(confidence.skills * 100)}%</span>
                </div>
                <div class="form-group full-width">
                    <label>Job Description</label>
                    <textarea class="form-textarea" rows="4">${this.parsedData.description || ''}</textarea>
                </div>
            </div>
        `;
    }

    hideParsedReview() {
        document.getElementById('parsedReview').style.display = 'none';
        document.getElementById('saveJob').style.display = 'none';
        this.parsedData = null;
    }

    async saveJob() {
        try {
            UIUtils.showNotification('Saving job to database...', 'info');
            
            let jobData = {};
            
            if (this.parsedData) {
                // Use parsed and edited data
                const fields = document.querySelectorAll('#parsedFields input, #parsedFields select, #parsedFields textarea');
                jobData = {
                    title: fields[0].value,
                    company: fields[1].value,
                    location: fields[2].value,
                    experience_required: parseInt(fields[3].value) || 0,
                    job_type: fields[4].value,
                    required_skills: this.parsedData.required_skills || [],
                    description: fields[6].value
                };
            } else if (this.currentMethod === 'form') {
                // Use quick form data
                const form = document.getElementById('quickJobForm');
                jobData = {
                    title: form.title.value,
                    company: form.company.value,
                    location: form.location.value,
                    description: form.description.value,
                    required_skills: [],
                    experience_required: 0,
                    job_type: form.job_type.value
                };
            } else {
                throw new Error('No job data to save');
            }
            
            // Validate required fields
            if (!jobData.title.trim() || !jobData.company.trim()) {
                throw new Error('Job title and company are required');
            }
            
            const response = await api.post('/api/create-job', { job_data: jobData });
            
            if (response.success) {
                UIUtils.showNotification(`Job "${jobData.title}" created successfully!`, 'success');
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
        document.getElementById('jdText').value = '';
    }

    close() {
        this.modal.classList.remove('modal--active');
        this.hideParsedReview();
    }
}

// Global instance
window.jobModal = new JobModal();
