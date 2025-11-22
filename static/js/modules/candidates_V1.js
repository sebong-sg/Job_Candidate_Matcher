// Candidates Management Module
class CandidatesModule {
    constructor() {
        this.initialized = false;
    }

    init() {
        if (this.initialized) return;
        console.log('👥 Candidates module initialized');
        this.initialized = true;
    }

    async loadCandidates() {
        try {
            const data = await api.get('/api/get-candidates');  // Add /api/ prefix
            return data.candidates || [];
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
        return `
            <div class="candidate-card">
                <div class="candidate-card__header">
                    <h4 class="candidate-card__name">${candidate.name}</h4>
                    <span class="candidate-card__experience">${this.formatExperience(candidate.experience_years)}</span>
                </div>
                <div class="candidate-card__details">
                    <div class="candidate-card__email">
                        <svg class="icon" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                            <polyline points="22,6 12,13 2,6"></polyline>
                        </svg>
                        ${candidate.email}
                    </div>
                    <div class="candidate-card__location">
                        <svg class="icon" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                            <circle cx="12" cy="10" r="3"></circle>
                        </svg>
                        ${candidate.location}
                    </div>
                </div>
                <div class="candidate-card__skills">
                    ${candidate.skills.slice(0, 4).map(skill => 
                        `<span class="skill-tag">${skill}</span>`
                    ).join('')}
                    ${candidate.skills.length > 4 ? `<span class="skill-tag">+${candidate.skills.length - 4}</span>` : ''}
                </div>
                <div class="candidate-card__profile">
                    ${this.truncateText(candidate.profile, 120)}
                </div>
            </div>
        `;
    }

    formatExperience(years) {
        if (!years) return 'No exp';
        return `${years} ${years === 1 ? 'year' : 'years'}`;
    }

    truncateText(text, length) {
        if (!text) return 'No profile available';
        return text.length > length ? text.substring(0, length) + '...' : text;
    }
}

// Global instance
window.candidatesModule = new CandidatesModule();
