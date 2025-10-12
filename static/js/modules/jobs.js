// Jobs Management Module
class JobsModule {
    constructor() {
        this.initialized = false;
    }

    init() {
        if (this.initialized) return;
        console.log('💼 Jobs module initialized');
        this.initialized = true;
    }

    async loadJobs() {
        try {
            const data = await api.get('/api/get-jobs');
            return data.jobs || [];
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
                    <div>❌</div>
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
                    <div>💼</div>
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
                </div>
                <div class="jobs-grid">
                    ${jobs.map(job => this.renderJobCard(job)).join('')}
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    renderJobCard(job) {
        return `
            <div class="job-card">
                <div class="job-card__header">
                    <div>
                        <h4 class="job-card__title">${job.title}</h4>
                        <div class="job-card__company">${job.company}</div>
                    </div>
                </div>
                <div class="job-card__details">
                    <div class="job-card__location">📍 ${job.location}</div>
                    <div class="job-card__experience">⏳ ${job.experience_required || 0}+ years experience</div>
                </div>
                <div class="job-card__skills">
                    ${job.required_skills.slice(0, 5).map(skill => 
                        `<span class="skill-tag skill-tag--required">${skill}</span>`
                    ).join('')}
                    ${job.preferred_skills && job.preferred_skills.slice(0, 3).map(skill => 
                        `<span class="skill-tag">${skill}</span>`
                    ).join('')}
                    ${(job.required_skills.length > 5 || (job.preferred_skills && job.preferred_skills.length > 3)) ? 
                        `<span class="skill-tag">+${(job.required_skills.length - 5) + (job.preferred_skills ? job.preferred_skills.length - 3 : 0)}</span>` : ''}
                </div>
                <div class="job-card__description">
                    ${Formatters.truncateText(job.description, 150)}
                </div>
            </div>
        `;
    }
}

// Global instance
window.jobsModule = new JobsModule();