class DashboardModule {
    constructor() {
        this.initialized = false;
    }

    init() {
        if (this.initialized) return;
        
        this.loadStats();
        this.loadMatches();
        this.initialized = true;
    }

    async loadStats() {
        try {
            const response = await fetch('/api/stats');
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            
            const data = await response.json();
            this.updateMetrics(data);
        } catch (error) {
            this.showError('Failed to load dashboard data');
        }
    }

    async loadMatches() {
        const container = document.getElementById('matches-results');
        if (container) {
            container.innerHTML = '<div class="loading-state"><div class="loading-spinner"></div><p>Loading matches...</p></div>';
        }

        try {
            const response = await fetch('/api/run-matching', { 
                method: 'POST'
            });
            
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            
            const data = await response.json();
            this.displayMatches(data);
        } catch (error) {
            this.showError('Failed to load matches');
        }
    }

    updateMetrics(data) {
        document.getElementById('jobs-count').textContent = data.total_jobs || 0;
        document.getElementById('candidates-count').textContent = data.total_candidates || 0;
        document.getElementById('matches-count').textContent = data.total_matches || 0;
        document.getElementById('success-rate').textContent = (data.success_rate || 0) + '%';
    }

    displayMatches(data) {
        const container = document.getElementById('matches-results');
        if (!container) return;

        if (data.error) {
            container.innerHTML = `<div class="error-state">Error: ${data.error}</div>`;
            return;
        }

        if (!data.matches || data.matches.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div>🔍</div>
                    <h3>No Matches Found</h3>
                    <p>Try running the AI matching engine.</p>
                </div>
            `;
            return;
        }

        let html = `<div class="matches-list"><h3>Recent Matches (${data.matches.length})</h3>`;
        
        data.matches.forEach(match => {
            html += `
                <div class="match-card">
                    <div class="match-card__header">
                        <h4>${match.job_title} at ${match.company}</h4>
                        <span class="match-score">${(match.top_score * 100).toFixed(1)}%</span>
                    </div>
                    <div class="match-card__body">
                        <p><strong>Top Candidate:</strong> ${match.top_candidate}</p>
                        <p><strong>Common Skills:</strong> ${match.common_skills ? match.common_skills.join(', ') : 'None'}</p>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        container.innerHTML = html;
    }

    showError(message) {
        const matchesContainer = document.getElementById('matches-results');
        if (matchesContainer) {
            matchesContainer.innerHTML = `
                <div class="error-state">
                    <div>❌</div>
                    <p>${message}</p>
                </div>
            `;
        }
    }
}

// Global functions
async function runMatching() {
    const resultsElement = document.getElementById('matches-results');
    if (resultsElement) {
        resultsElement.innerHTML = '<div class="loading-state"><div class="loading-spinner"></div><p>Running AI matching...</p></div>';
    }

    try {
        const response = await fetch('/api/run-matching', { method: 'POST' });
        const data = await response.json();
        
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            dashboardModule.displayMatches(data);
            dashboardModule.loadStats();
        }
    } catch (error) {
        alert('Failed to run matching');
    }
}

function loadCandidates() {
    alert('Candidates view coming soon');
}

function loadJobs() {
    alert('Jobs view coming soon');
}

// Global instance
const dashboardModule = new DashboardModule();

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => dashboardModule.init());