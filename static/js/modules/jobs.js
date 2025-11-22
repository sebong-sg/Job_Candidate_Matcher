// Jobs Management Module
class JobsModule {
    constructor() {
        this.initialized = false;
        this.currentJobs = [];
    }

    init() {
        if (this.initialized) return;
        console.log('💼 Jobs module initialized');
        this.setupJobDetailModal();
        this.initialized = true;
    }

    setupJobDetailModal() {
        document.getElementById('closeJobDetailModal').addEventListener('click', () => this.closeJobDetailModal());
        document.getElementById('closeDetailModal').addEventListener('click', () => this.closeJobDetailModal());
        document.querySelector('#jobDetailModal .modal__overlay').addEventListener('click', () => this.closeJobDetailModal());
        
        // Match candidates button
        document.getElementById('matchCandidatesBtn').addEventListener('click', () => {
            window.location.href = '/matching';
        });
    }

    async loadJobs() {
        try {
            const data = await api.get('/api/get-jobs');
            this.currentJobs = data.jobs || [];
            return this.currentJobs;
        } catch (error) {
            console.error('Error loading jobs:', error);
            if (window.UIUtils) {
                UIUtils.showNotification('Failed to load jobs', 'error');
            }
            return [];
        }
    }

    async displayJobs(container) {
        if (!container) return;
        
        // Show loading state
        container.innerHTML = `
            <div class="loading-state">
                <div class="loading-spinner"></div>
                <p>Loading jobs...</p>
            </div>
        `;

        try {
            const jobs = await this.loadJobs();
            this.renderJobs(container, jobs);
        } catch (error) {
            container.innerHTML = `
                <div class="error-state">
                    <svg class="icon" width="48" height="48" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                    <h3>Failed to load jobs</h3>
                    <p>Please try again later.</p>
                    <button onclick="jobsModule.displayJobs(document.getElementById('jobsContainer'))" 
                            class="btn btn--outline">Retry</button>
                </div>
            `;
        }
    }

    renderJobs(container, jobs) {
        if (!jobs || jobs.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <svg class="icon" width="48" height="48" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
                        <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
                    </svg>
                    <h3>No Jobs Yet</h3>
                    <p>Get started by adding your first job using the "Add Job" button above.</p>
                </div>
            `;
            return;
        }

        const html = `
            <div class="jobs-list">
                <div class="list-header">
                    <h3>All Jobs (${jobs.length})</h3>
                    <div class="list-stats">
                        <span class="stat-item">High Quality: ${this.countJobsByQuality(jobs, 'high')}</span>
                        <span class="stat-item">Needs Improvement: ${this.countJobsByQuality(jobs, 'low') + this.countJobsByQuality(jobs, 'very_low')}</span>
                    </div>
                </div>
                <div class="jobs-grid">
                    ${jobs.map(job => this.renderJobCard(job)).join('')}
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    countJobsByQuality(jobs, qualityLevel) {
        return jobs.filter(job => {
            const quality = job.quality_assessment || {};
            return quality.quality_level === qualityLevel;
        }).length;
    }

    renderJobCard(job) {
        const quality = job.quality_assessment || {};
        const hasQualityData = quality.quality_level && quality.quality_level !== 'unknown';
        const hasEnhancedData = job.growth_requirements && job.growth_requirements.target_career_stage;
        const hasAIProfile = job.ai_job_profile && Object.keys(job.ai_job_profile).length > 0;
        
        return `
            <div class="job-card" data-job-id="${job.id}" onclick="jobsModule.showJobDetail(${job.id})">
                <div class="job-card__header">
                    <div>
                        <h4 class="job-card__title">${job.title || 'Untitled Job'}</h4>
                        <div class="job-card__company">${job.company || 'No company'}</div>
                    </div>
                    ${hasQualityData ? `
                        <span class="job-quality-badge job-quality-badge--${quality.quality_level}">
                            ${this.formatQualityLevel(quality.quality_level)}
                            ${quality.quality_score ? Math.round(quality.quality_score * 100) + '%' : ''}
                        </span>
                    ` : ''}
                </div>
                <div class="job-card__details">
                    <div class="job-card__location">
                        <svg class="icon" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                            <circle cx="12" cy="10" r="3"></circle>
                        </svg>
                        ${job.location || 'Location not specified'}
                    </div>
                    <div class="job-card__experience">
                        <svg class="icon" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"></circle>
                            <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>
                        ${job.experience_required || 0}+ years experience
                    </div>
                </div>
                ${hasEnhancedData ? `
                    <div class="job-card__enhanced">
                        <span class="enhanced-badge">${this.formatCareerStage(job.growth_requirements.target_career_stage)}</span>
                        <span class="enhanced-badge">${this.formatScopeLevel(job.growth_requirements.scope_level_required)}</span>
                        ${job.growth_requirements.role_archetype ? `
                            <span class="enhanced-badge">${this.formatArchetype(job.growth_requirements.role_archetype)}</span>
                        ` : ''}
                    </div>
                ` : ''}
                ${hasAIProfile ? `
                    <div class="job-card__ai-profile">
                        <span class="ai-badge">🤖 AI Enhanced</span>
                    </div>
                ` : ''}
                <div class="job-card__skills">
                    ${(job.required_skills || []).slice(0, 5).map(skill => 
                        `<span class="skill-tag skill-tag--required">${skill}</span>`
                    ).join('')}
                    ${job.preferred_skills && job.preferred_skills.slice(0, 3).map(skill => 
                        `<span class="skill-tag">${skill}</span>`
                    ).join('')}
                    ${((job.required_skills || []).length > 5 || (job.preferred_skills && job.preferred_skills.length > 3)) ? 
                        `<span class="skill-tag">+${((job.required_skills || []).length - 5) + (job.preferred_skills ? job.preferred_skills.length - 3 : 0)}</span>` : ''}
                </div>
                <div class="job-card__description">
                    ${Formatters.truncateText(job.description || 'No description available', 150)}
                </div>
                ${quality.quality_issues && quality.quality_issues.length > 0 ? `
                    <div class="job-card__quality-issues">
                        <small>⚠️ ${quality.quality_issues.length} quality issue${quality.quality_issues.length !== 1 ? 's' : ''}</small>
                    </div>
                ` : ''}
            </div>
        `;
    }

    showJobDetail(jobId) {
        const job = this.currentJobs.find(j => j.id === jobId);
        
        if (!job) {
            console.error('Job not found:', jobId);
            UIUtils.showNotification('Job details not found', 'error');
            return;
        }
        
        this.populateJobDetailModal(job);
        this.openJobDetailModal();
    }

    populateJobDetailModal(job) {
        console.log('🔍 Populating job detail modal with:', job);
        
        // Populate basic info
        document.getElementById('detailJobTitle').textContent = job.title || 'No title available';
        document.getElementById('detailCompany').textContent = job.company || 'No company specified';
        document.getElementById('detailLocation').textContent = job.location || 'Not specified';
        document.getElementById('detailExperience').textContent = `${job.experience_required || 0}+ years`;
        document.getElementById('detailJobType').textContent = job.job_type || 'Full-time';
        document.getElementById('detailSalary').textContent = job.salary_range || 'Not specified';
        // document.getElementById('detailDescription').textContent = job.description || 'No description available';
        document.getElementById('detailDescription').textContent = job.original_job_text || job.description || 'No description available';

        // Quality badge
        const quality = job.quality_assessment || {};
        const qualityBadge = document.getElementById('detailQualityBadge');
        if (quality.quality_level && quality.quality_level !== 'unknown') {
            qualityBadge.innerHTML = `${this.formatQualityLevel(quality.quality_level)} ${Math.round((quality.quality_score || 0.5) * 100)}%`;
            qualityBadge.className = `job-quality-badge job-quality-badge--${quality.quality_level}`;
            qualityBadge.style.display = 'inline-flex';
        } else {
            qualityBadge.style.display = 'none';
        }
        
        // Skills
        this.populateSkills('detailRequiredSkills', job.required_skills || []);
        this.populateSkills('detailPreferredSkills', job.preferred_skills || []);
        document.getElementById('preferredSkillsSection').style.display = 
            job.preferred_skills && job.preferred_skills.length > 0 ? 'block' : 'none';
        
        // NEW: AI Job Profile
        this.populateAIJobProfile(job);
        
        // Enhanced data
        this.populateEnhancedData(job);
        
        // Quality assessment
        this.populateQualityAssessment(job);
        
        // Job Requirements
        this.populateJobRequirements(job);
        
        console.log('✅ Job detail modal populated successfully');
    }

    populateAIJobProfile(job) {
        const aiProfileSection = document.getElementById('aiJobProfileSection');
        const aiProfileContent = document.getElementById('aiJobProfileContent');
        
        if (!aiProfileSection || !aiProfileContent) {
            console.error('AI Job Profile elements not found');
            return;
        }
        
        const aiProfile = job.ai_job_profile || {};
        
        if (aiProfile && Object.keys(aiProfile).length > 0) {
            const profileHtml = `
                <div class="ai-profile-section">
                    <div class="ai-profile-item">
                        <h5>Role Overview</h5>
                        <p>${aiProfile.role_overview || 'No role overview available.'}</p>
                    </div>
                    <div class="ai-profile-item">
                        <h5>Ideal Candidate Profile</h5>
                        <p>${aiProfile.ideal_candidate || 'No candidate profile available.'}</p>
                    </div>
                    <div class="ai-profile-item">
                        <h5>Key Success Factors</h5>
                        <p>${aiProfile.success_factors || 'No success factors identified.'}</p>
                    </div>
                    <div class="ai-profile-item">
                        <h5>Growth Potential</h5>
                        <p>${aiProfile.growth_potential || 'No growth potential analysis available.'}</p>
                    </div>
                    <div class="ai-profile-item">
                        <h5>Cultural Fit</h5>
                        <p>${aiProfile.cultural_fit || 'No cultural fit analysis available.'}</p>
                    </div>
                    <div class="ai-profile-item">
                        <h5>Recruiting Insights</h5>
                        <p>${aiProfile.recruiting_insights || 'No recruiting insights available.'}</p>
                    </div>
                </div>
            `;
            
            aiProfileContent.innerHTML = profileHtml;
            aiProfileSection.style.display = 'block';
        } else {
            aiProfileSection.style.display = 'none';
        }
    }

    populateSkills(containerId, skills) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error('Container not found:', containerId);
            return;
        }
        
        if (skills && skills.length > 0) {
            container.innerHTML = skills.map(skill => 
                `<span class="skill-tag">${skill}</span>`
            ).join('');
        } else {
            container.innerHTML = '<span class="text-muted">No skills specified</span>';
        }
    }

    populateEnhancedData(job) {
        const enhancedSection = document.getElementById('detailEnhancedData');
        const enhancedGrid = document.getElementById('enhancedDataGrid');
        
        if (!enhancedSection || !enhancedGrid) {
            console.error('Enhanced data elements not found');
            return;
        }
        
        const growthReqs = job.growth_requirements || {};
        
        if (growthReqs.target_career_stage) {
            enhancedGrid.innerHTML = `
                <div class="enhanced-data-item">
                    <span class="enhanced-data-label">Career Stage:</span>
                    <span class="enhanced-data-value">${this.formatCareerStage(growthReqs.target_career_stage)}</span>
                </div>
                <div class="enhanced-data-item">
                    <span class="enhanced-data-label">Role Type:</span>
                    <span class="enhanced-data-value">${this.formatArchetype(growthReqs.role_archetype)}</span>
                </div>
                <div class="enhanced-data-item">
                    <span class="enhanced-data-label">Scope Level:</span>
                    <span class="enhanced-data-value">${this.formatScopeLevel(growthReqs.scope_level_required)}</span>
                </div>
                ${growthReqs.leadership_scope ? `
                <div class="enhanced-data-item">
                    <span class="enhanced-data-label">Leadership Scope:</span>
                    <span class="enhanced-data-value">
                        <span class="leadership-badge leadership-badge--${growthReqs.leadership_scope}">
                            ${this.formatLeadershipScope(growthReqs.leadership_scope)}
                        </span>
                    </span>    
                </div>
                ` : ''}
            `;
            enhancedSection.style.display = 'block';
        } else {
            enhancedSection.style.display = 'none';
        }
    }

    formatLeadershipScope(scope) {
       const scopes = {
            'individual_contributor': 'Individual Contributor',
            'team_lead': 'Team Lead', 
            'manager': 'Manager',
            'executive': 'Executive'
        };
        return scopes[scope] || scope;
    }

    populateQualityAssessment(job) {
        const qualitySection = document.getElementById('detailQuality');
        const qualityContent = document.getElementById('qualityDetailContent');
        
        if (!qualitySection || !qualityContent) {
            console.error('Quality assessment elements not found');
            return;
        }
        
        const quality = job.quality_assessment || {};
        
        if (quality.quality_level) {
            qualityContent.innerHTML = `
                <div class="quality-indicator quality-indicator--${quality.quality_level}">
                    <div class="quality-indicator__header">
                        <span class="quality-indicator__label">Overall Quality Score</span>
                        <span class="quality-indicator__score">${Math.round((quality.quality_score || 0.5) * 100)}%</span>
                    </div>
                    <div class="quality-indicator__level">
                        <span class="quality-badge quality-badge--${quality.quality_level}">
                            ${this.formatQualityLevel(quality.quality_level)}
                        </span>
                    </div>
                </div>
                ${quality.quality_issues && quality.quality_issues.length > 0 ? `
                <div class="quality-warning quality-warning--${quality.quality_level}">
                    <div class="warning-header">
                        <h4>Quality Issues</h4>
                    </div>
                    <div class="warning-content">
                        <ul>
                            ${quality.quality_issues.map(issue => `<li>${issue}</li>`).join('')}
                        </ul>
                    </div>
                </div>
                ` : ''}
            `;
            qualitySection.style.display = 'block';
        } else {
            qualitySection.style.display = 'none';
        }
    }

    populateJobRequirements(job) {
        const requirementsSection = document.getElementById('jobRequirementsSection');
        const requirementsGrid = document.getElementById('jobRequirementsGrid');
        
        if (!requirementsSection || !requirementsGrid) {
            console.error('Job requirements elements not found');
            return;
        }
        
        const requirements = this.extractJobRequirements(job);
        requirementsGrid.innerHTML = this.renderJobRequirements(requirements);
        requirementsSection.style.display = 'block';
    }

    extractJobRequirements(job) {
        const cultural = job.cultural_attributes || {};
        const growth = job.growth_requirements || {};
        const skillReqs = job.skill_requirements || {};
        
        return {
            skills: {
                core: skillReqs.core_skills || job.required_skills || [],
                secondary: skillReqs.secondary_skills || job.preferred_skills || [],
                proficiency: skillReqs.required_proficiency || {}
            },
            location: job.location || 'Not specified',
            experience: job.experience_required || 0,
            employmentType: job.job_type || 'Full-time',
            cultural: {
                teamwork: this.extractCulturalScore(cultural.teamwork),
                innovation: this.extractCulturalScore(cultural.innovation),
                workEnvironment: this.extractCulturalScore(cultural.work_environment),
                workPace: this.extractCulturalScore(cultural.work_pace),
                customerFocus: this.extractCulturalScore(cultural.customer_focus)
            },
            growth: {
                careerStage: growth.target_career_stage || 'mid_career',
                roleArchetype: growth.role_archetype || 'technical_specialist',
                scopeLevel: growth.scope_level_required || 1,
                executivePotential: growth.executive_potential_required || 0.3
            }
        };
    }

    renderJobRequirements(requirements) {
        return `
            <div class="requirements-category">
                <h5>Skills & Experience</h5>
                <div class="requirement-item">
                    <span class="requirement-label">Core Skills:</span>
                    <span class="requirement-value">
                        ${requirements.skills.core.length > 0 ? 
                            requirements.skills.core.slice(0, 8).map(skill => 
                                `<span class="skill-tag skill-tag--small">${skill}</span>`
                            ).join('') : 
                            '<span class="text-muted">None specified</span>'
                        }
                        ${requirements.skills.core.length > 8 ? 
                            `<span class="skill-tag skill-tag--small">+${requirements.skills.core.length - 8}</span>` : 
                            ''
                        }
                    </span>
                </div>
                <div class="requirement-item">
                    <span class="requirement-label">Experience Required:</span>
                    <span class="requirement-value">${requirements.experience}+ years</span>
                </div>
                <div class="requirement-item">
                    <span class="requirement-label">Employment Type:</span>
                    <span class="requirement-value">${requirements.employmentType}</span>
                </div>
            </div>
            
            <div class="requirements-category">
                <h5>Location & Environment</h5>
                <div class="requirement-item">
                    <span class="requirement-label">Location:</span>
                    <span class="requirement-value">${requirements.location}</span>
                </div>
                <div class="requirement-item">
                    <span class="requirement-label">Team Collaboration:</span>
                    <span class="requirement-value">${this.formatCulturalValue(requirements.cultural.teamwork)}</span>
                </div>
                <div class="requirement-item">
                    <span class="requirement-label">Work Pace:</span>
                    <span class="requirement-value">${this.formatCulturalValue(requirements.cultural.workPace)}</span>
                </div>
            </div>
            
            <div class="requirements-category">
                <h5>Career Growth</h5>
                <div class="requirement-item">
                    <span class="requirement-label">Career Stage:</span>
                    <span class="requirement-value">${this.formatCareerStage(requirements.growth.careerStage)}</span>
                </div>
                <div class="requirement-item">
                    <span class="requirement-label">Role Type:</span>
                    <span class="requirement-value">${this.formatArchetype(requirements.growth.roleArchetype)}</span>
                </div>
                <div class="requirement-item">
                    <span class="requirement-label">Scope Level:</span>
                    <span class="requirement-value">${this.formatScopeLevel(requirements.growth.scopeLevel)}</span>
                </div>
            </div>
        `;
    }

    extractCulturalScore(scoreData) {
        if (typeof scoreData === 'number') {
            return scoreData;
        } else if (Array.isArray(scoreData) && scoreData.length > 0) {
            return scoreData[0];
        } else if (typeof scoreData === 'object' && scoreData !== null) {
            return scoreData.score || 0.5;
        }
        return 0.5;
    }

    formatCulturalValue(score) {
        if (score >= 0.8) return 'Very High';
        if (score >= 0.6) return 'High';
        if (score >= 0.4) return 'Medium';
        return 'Low';
    }

    openJobDetailModal() {
        document.getElementById('jobDetailModal').classList.add('modal--active');
    }

    closeJobDetailModal() {
        document.getElementById('jobDetailModal').classList.remove('modal--active');
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
            'early_career': 'Early Career',
            'mid_career': 'Mid Career', 
            'executive': 'Executive'
        };
        return stages[stage] || stage;
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

    formatArchetype(archetype) {
        const archetypes = {
            'high_growth_ic': 'High Growth IC',
            'strategic_executive': 'Strategic Exec',
            'technical_specialist': 'Tech Specialist',
            'portfolio_leader': 'Portfolio Leader'
        };
        return archetypes[archetype] || archetype;
    }
}

// Global instance
window.jobsModule = new JobsModule();