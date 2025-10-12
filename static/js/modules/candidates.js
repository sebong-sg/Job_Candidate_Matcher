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
                    <div>❌</div>
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
                    <div>👥</div>
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
                    <div class="candidate-card__email">📧 ${candidate.email}</div>
                    <div class="candidate-card__location">📍 ${candidate.location}</div>
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
