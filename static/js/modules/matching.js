// Matching Engine Module
class MatchingModule {
    constructor() {
        this.initialized = false;
    }

    init() {
        if (this.initialized) return;
        console.log('🤖 Matching module initialized');
        this.initialized = true;
    }

    async runMatching() {
        UIUtils.showNotification('Running AI matching...', 'info');
        
        try {
            const data = await api.post('/run-matching');
            
            if (data.error) {
                throw new Error(data.error);
            }

            UIUtils.showNotification(`Found ${data.matches?.length || 0} matches`, 'success');
            return data;
        } catch (error) {
            console.error('Matching error:', error);
            UIUtils.showNotification('Failed to run matching', 'error');
            throw error;
        }
    }

    displayMatches(matches, container) {
        if (!container) return;

        if (!matches || matches.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div>🔍</div>
                    <h3>No Matches Found</h3>
                    <p>Try running the AI matching engine or add more candidates/jobs.</p>
                </div>
            `;
            return;
        }

        const html = `
            <div class="matches-list">
                <div class="list-header">
                    <h3>Top Matches (${matches.length})</h3>
                </div>
                ${matches.map(match => this.renderMatchCard(match)).join('')}
            </div>
        `;

        container.innerHTML = html;
    }

    renderMatchCard(match) {
        const breakdown = match.score_breakdown || {};
        return `
            <div class="match-card">
                <div class="match-card__header">
                    <div class="match-card__title">
                        <h4>${match.job_title}</h4>
                        <span class="match-card__company">at ${match.company}</span>
                    </div>
                    <div class="match-card__score">
                        <span class="score-badge score-badge--${match.match_grade}">
                            ${Formatters.formatPercentage(match.top_score)}
                        </span>
                        <span class="match-grade">${match.match_grade}</span>
                    </div>
                </div>
                <div class="match-card__details">
                    <div class="match-card__candidate">
                        <strong>Top Candidate:</strong> ${match.top_candidate}
                    </div>
                    <div class="match-card__breakdown">
                        <div class="breakdown-item">
                            <span>Skills:</span>
                            <span>${match.score_breakdown || 0}%</span>
                        </div>
                        <div class="breakdown-item">
                            <span>Experience:</span>
                            <span>${breakdown.experience || 0}%</span>
                        </div>
                        <div class="breakdown-item">
                            <span>Location:</span>
                            <span>${breakdown.location || 0}%</span>
                        </div>
                    </div>
                    <div class="match-card__skills">
                        <strong>Common Skills:</strong>
                        ${match.common_skills && match.common_skills.length > 0 
                            ? match.common_skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')
                            : '<span class="text-muted">No common skills</span>'
                        }
                    </div>
                </div>
            </div>
        `;
    }
}

// Global instance
window.matchingModule = new MatchingModule();