// Candidates Management Module
class CandidatesModule {
    constructor() {
        this.initialized = false;
        this.currentCandidates = [];
    }

    init() {
        if (this.initialized) return;
        console.log('👥 Candidates module initialized');
        this.setupCandidateDetailModal();
        this.initialized = true;
    }

    setupCandidateDetailModal() {
        document.getElementById('closeCandidateDetailModal').addEventListener('click', () => this.closeCandidateDetailModal());
        document.getElementById('closeDetailCandidateModal').addEventListener('click', () => this.closeCandidateDetailModal());
        document.querySelector('#candidateDetailModal .modal__overlay').addEventListener('click', () => this.closeCandidateDetailModal());
        
        // Find jobs button
        document.getElementById('findJobsForCandidateBtn').addEventListener('click', () => {
            window.location.href = '/matching';
        });
    }

    async loadCandidates() {
        try {
            const data = await api.get('/api/get-candidates');
            this.currentCandidates = data.candidates || [];
            return this.currentCandidates;
        } catch (error) {
            console.error('Error loading candidates:', error);
            if (window.UIUtils) {
                UIUtils.showNotification('Failed to load candidates', 'error');
            }
            return [];
        }
    }

    async displayCandidates(container) {
        if (!container) return;
        
        // Show loading state
        container.innerHTML = `
            <div class="loading-state">
                <div class="loading-spinner"></div>
                <p>Loading candidates...</p>
            </div>
        `;

        try {
            const candidates = await this.loadCandidates();
            this.renderCandidates(container, candidates);
        } catch (error) {
            container.innerHTML = `
                <div class="error-state">
                    <svg class="icon" width="48" height="48" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                    <h3>Failed to load candidates</h3>
                    <p>Please try again later.</p>
                    <button onclick="candidatesModule.displayCandidates(document.getElementById('candidatesContainer'))" 
                            class="btn btn--outline">Retry</button>
                </div>
            `;
        }
    }

    renderCandidates(container, candidates) {
        if (!candidates || candidates.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <svg class="icon" width="48" height="48" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                        <circle cx="9" cy="7" r="4"></circle>
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                    </svg>
                    <h3>No Candidates Yet</h3>
                    <p>Get started by adding your first candidate using the "Add Candidate" button above.</p>
                </div>
            `;
            return;
        }

        const html = `
            <div class="candidates-list">
                <div class="list-header">
                    <h3>All Candidates (${candidates.length})</h3>
                </div>
                <div class="candidates-grid">
                    ${candidates.map(candidate => this.renderCandidateCard(candidate)).join('')}
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    renderCandidateCard(candidate) {
        const quality = candidate.quality_assessment || {};
        const hasQualityData = quality.quality_level && quality.quality_level !== 'unknown';
        const hasEnhancedData = candidate.growth_metrics && candidate.growth_metrics.career_stage;
        
        return `
            <div class="candidate-card" data-candidate-id="${candidate.id}" onclick="candidatesModule.showCandidateDetail(${candidate.id})">
                <div class="candidate-card__header">
                    <div>
                        <h4 class="candidate-card__name">${candidate.name || 'Unnamed Candidate'}</h4>
                        <div class="candidate-card__email">${candidate.email || 'No email'}</div>
                    </div>
                    ${hasQualityData ? `
                        <span class="candidate-quality-badge candidate-quality-badge--${quality.quality_level}">
                            ${this.formatQualityLevel(quality.quality_level)}
                            ${quality.quality_score ? Math.round(quality.quality_score * 100) + '%' : ''}
                        </span>
                    ` : ''}
                </div>
                <div class="candidate-card__details">
                    <div class="candidate-card__location">
                        <svg class="icon" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                            <circle cx="12" cy="10" r="3"></circle>
                        </svg>
                        ${candidate.location || 'Location not specified'}
                    </div>
                    <div class="candidate-card__experience">
                        <svg class="icon" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"></circle>
                            <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>
                        ${candidate.experience_years || 0}+ years experience
                    </div>
                </div>
                ${hasEnhancedData ? `
                    <div class="candidate-card__enhanced">
                        <span class="enhanced-badge">${this.formatCareerStage(candidate.growth_metrics.career_stage)}</span>
                        <span class="enhanced-badge">${this.formatArchetype(candidate.growth_metrics.career_archetype)}</span>
                        ${candidate.growth_metrics.growth_potential_score ? `
                            <span class="enhanced-badge">Growth: ${Math.round(candidate.growth_metrics.growth_potential_score)}%</span>
                        ` : ''}
                    </div>
                ` : ''}
                <div class="candidate-card__skills">
                    ${(candidate.skills || []).slice(0, 5).map(skill => 
                        `<span class="skill-tag">${skill}</span>`
                    ).join('')}
                    ${(candidate.skills || []).length > 5 ? 
                        `<span class="skill-tag">+${(candidate.skills || []).length - 5}</span>` : ''}
                </div>
                <div class="candidate-card__profile">
                    ${this.truncateText(candidate.profile || 'No profile available', 120)}
                </div>
                ${quality.quality_issues && quality.quality_issues.length > 0 ? `
                    <div class="candidate-card__quality-issues">
                        <small>⚠️ ${quality.quality_issues.length} quality issue${quality.quality_issues.length !== 1 ? 's' : ''}</small>
                    </div>
                ` : ''}
            </div>
        `;
    }

    showCandidateDetail(candidateId) {
        const candidate = this.currentCandidates.find(c => c.id === candidateId);
        
        if (!candidate) {
            console.error('Candidate not found:', candidateId);
            UIUtils.showNotification('Candidate details not found', 'error');
            return;
        }
        
        this.populateCandidateDetailModal(candidate);
        this.openCandidateDetailModal();
    }

    populateCandidateDetailModal(candidate) {
        console.log('🔍 Populating candidate detail modal with:', candidate);
        
        // Populate basic info
        document.getElementById('detailCandidateName').textContent = candidate.name || 'No name available';
        document.getElementById('detailEmail').textContent = candidate.email || 'No email specified';
        document.getElementById('detailLocation').textContent = candidate.location || 'Not specified';
        document.getElementById('detailExperience').textContent = `${candidate.experience_years || 0}+ years experience`;
        document.getElementById('detailEducation').textContent = candidate.education || 'Not specified';
        document.getElementById('detailProfile').textContent = candidate.profile || 'No profile available';
        
        // Quality badge
        const quality = candidate.quality_assessment || {};
        const qualityBadge = document.getElementById('detailQualityBadge');
        if (quality.quality_level && quality.quality_level !== 'unknown') {
            qualityBadge.innerHTML = `${this.formatQualityLevel(quality.quality_level)} ${Math.round((quality.quality_score || 0.5) * 100)}%`;
            qualityBadge.className = `candidate-quality-badge candidate-quality-badge--${quality.quality_level}`;
            qualityBadge.style.display = 'inline-flex';
        } else {
            qualityBadge.style.display = 'none';
        }
        
        // Skills
        this.populateSkills('detailSkills', candidate.skills || []);
        
        // Enhanced data
        this.populateEnhancedData(candidate);
        
        // Quality assessment
        this.populateQualityAssessment(candidate);
        
        // Candidate Profile
        this.populateCandidateProfile(candidate);
        
        // Complete CV Details Section
        const cvDetailsSection = document.getElementById('cvDetailsSection');
        if (cvDetailsSection && candidate.original_resume_text) {
            cvDetailsSection.style.display = 'block';
            document.getElementById('cvDetailsContent').textContent = candidate.original_resume_text;
        } else {
            if (cvDetailsSection) cvDetailsSection.style.display = 'none';
        }
        
        console.log('✅ Candidate detail modal populated successfully');
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

    populateEnhancedData(candidate) {
        const enhancedSection = document.getElementById('detailEnhancedData');
        const enhancedGrid = document.getElementById('enhancedDataGrid');
        
        if (!enhancedSection || !enhancedGrid) {
            console.error('Enhanced data elements not found');
            return;
        }
        
        const growthMetrics = candidate.growth_metrics || {};
        
        if (growthMetrics.career_stage) {
            enhancedGrid.innerHTML = `
                <div class="enhanced-data-item">
                    <span class="enhanced-data-label">Career Stage:</span>
                    <span class="enhanced-data-value">${this.formatCareerStage(growthMetrics.career_stage)}</span>
                </div>
                <div class="enhanced-data-item">
                    <span class="enhanced-data-label">Role Archetype:</span>
                    <span class="enhanced-data-value">${this.formatArchetype(growthMetrics.career_archetype)}</span>
                </div>
                ${growthMetrics.growth_potential_score ? `
                <div class="enhanced-data-item">
                    <span class="enhanced-data-label">Growth Potential:</span>
                    <span class="enhanced-data-value">${Math.round(growthMetrics.growth_potential_score)}%</span>
                </div>
                ` : ''}
                ${growthMetrics.executive_potential ? `
                <div class="enhanced-data-item">
                    <span class="enhanced-data-label">Executive Potential:</span>
                    <span class="enhanced-data-value">${Math.round(growthMetrics.executive_potential * 100)}%</span>
                </div>
                ` : ''}
            `;
            enhancedSection.style.display = 'block';
        } else {
            enhancedSection.style.display = 'none';
        }
    }

    populateQualityAssessment(candidate) {
        const qualitySection = document.getElementById('detailQuality');
        const qualityContent = document.getElementById('qualityDetailContent');
        
        if (!qualitySection || !qualityContent) {
            console.error('Quality assessment elements not found');
            return;
        }
        
        const quality = candidate.quality_assessment || {};
        
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

    populateCandidateProfile(candidate) {
        const profileSection = document.getElementById('candidateRequirementsSection');
        const profileGrid = document.getElementById('candidateRequirementsGrid');
        
        if (!profileSection || !profileGrid) {
            console.error('Candidate profile elements not found');
            return;
        }
        
        const profile = this.extractCandidateProfile(candidate);
        profileGrid.innerHTML = this.renderCandidateProfile(profile);
        profileSection.style.display = 'block';
    }

    extractCandidateProfile(candidate) {
        const growth = candidate.growth_metrics || {};
        const cultural = candidate.cultural_attributes || {};
        
        return {
            skills: {
                core: candidate.skills || [],
                proficiency: candidate.skill_proficiency || {}
            },
            location: candidate.location || 'Not specified',
            experience: candidate.experience_years || 0,
            education: candidate.education || 'Not specified',
            cultural: {
                teamwork: this.extractCulturalScore(cultural.teamwork),
                innovation: this.extractCulturalScore(cultural.innovation),
                workEnvironment: this.extractCulturalScore(cultural.work_environment),
                workPace: this.extractCulturalScore(cultural.work_pace)
            },
            growth: {
                careerStage: growth.career_stage || 'mid_career',
                roleArchetype: growth.career_archetype || 'technical_specialist',
                growthPotential: growth.growth_potential_score || 0,
                executivePotential: growth.executive_potential || 0
            }
        };
    }

    renderCandidateProfile(profile) {
        return `
            <div class="requirements-category">
                <h5>Skills & Experience</h5>
                <div class="requirement-item">
                    <span class="requirement-label">Core Skills:</span>
                    <span class="requirement-value">
                        ${profile.skills.core.length > 0 ? 
                            profile.skills.core.slice(0, 8).map(skill => 
                                `<span class="skill-tag skill-tag--small">${skill}</span>`
                            ).join('') : 
                            '<span class="text-muted">None specified</span>'
                        }
                        ${profile.skills.core.length > 8 ? 
                            `<span class="skill-tag skill-tag--small">+${profile.skills.core.length - 8}</span>` : 
                            ''
                        }
                    </span>
                </div>
                <div class="requirement-item">
                    <span class="requirement-label">Experience:</span>
                    <span class="requirement-value">${profile.experience}+ years</span>
                </div>
                <div class="requirement-item">
                    <span class="requirement-label">Education:</span>
                    <span class="requirement-value">${profile.education}</span>
                </div>
            </div>
            
            <div class="requirements-category">
                <h5>Location & Preferences</h5>
                <div class="requirement-item">
                    <span class="requirement-label">Location:</span>
                    <span class="requirement-value">${profile.location}</span>
                </div>
                <div class="requirement-item">
                    <span class="requirement-label">Team Collaboration:</span>
                    <span class="requirement-value">${this.formatCulturalValue(profile.cultural.teamwork)}</span>
                </div>
                <div class="requirement-item">
                    <span class="requirement-label">Work Pace:</span>
                    <span class="requirement-value">${this.formatCulturalValue(profile.cultural.workPace)}</span>
                </div>
            </div>
            
            <div class="requirements-category">
                <h5>Career Growth</h5>
                <div class="requirement-item">
                    <span class="requirement-label">Career Stage:</span>
                    <span class="requirement-value">${this.formatCareerStage(profile.growth.careerStage)}</span>
                </div>
                <div class="requirement-item">
                    <span class="requirement-label">Role Archetype:</span>
                    <span class="requirement-value">${this.formatArchetype(profile.growth.roleArchetype)}</span>
                </div>
                <div class="requirement-item">
                    <span class="requirement-label">Growth Potential:</span>
                    <span class="requirement-value">${Math.round(profile.growth.growthPotential * 100)}%</span>
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

    openCandidateDetailModal() {
        document.getElementById('candidateDetailModal').classList.add('modal--active');
    }

    closeCandidateDetailModal() {
        document.getElementById('candidateDetailModal').classList.remove('modal--active');
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

    formatArchetype(archetype) {
        const archetypes = {
            'high_growth_ic': 'High Growth IC',
            'strategic_executive': 'Strategic Exec',
            'technical_specialist': 'Tech Specialist',
            'portfolio_leader': 'Portfolio Leader'
        };
        return archetypes[archetype] || archetype;
    }

    truncateText(text, length) {
        if (!text) return 'No profile available';
        return text.length > length ? text.substring(0, length) + '...' : text;
    }
}

// Global instance
window.candidatesModule = new CandidatesModule();