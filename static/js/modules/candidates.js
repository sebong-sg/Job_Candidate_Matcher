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
            const data = await api.get('/get-candidates');
            return data.candidates || [];
        } catch (error) {
            console.error('Error loading candidates:', error);
            UIUtils.showNotification('Failed to load candidates', 'error');
            return [];
        }
    }

    async displayCandidates(container) {
        if (!container) return;

        UIUtils.showNotification('Loading candidates...', 'info');
        
        try {
            const candidates = await this.loadCandidates();
            this.renderCandidates(container, candidates);
            UIUtils.showNotification(`Loaded ${candidates.length} candidates`, 'success');
        } catch (error) {
            UIUtils.showNotification('Failed to load candidates', 'error');
        }
    }

    renderCandidates(container, candidates) {
        if (!candidates || candidates.length === 0) {
            container.innerHTML = '<div class="empty-state">No candidates found</div>';
            return;
        }

        const html = `
            <div class="candidates-list">
                <div class="list-header">
                    <h3>Candidates (${candidates.length})</h3>
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
                    <span class="candidate-card__experience">${Formatters.formatExperience(candidate.experience_years)}</span>
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
                    ${Formatters.truncateText(candidate.profile, 120)}
                </div>
            </div>
        `;
    }
}

// Global instance
window.candidatesModule = new CandidatesModule();