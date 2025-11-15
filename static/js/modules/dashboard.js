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
                    <svg class="icon" width="48" height="48" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                    <h3>No Matches Found</h3>
                    <p>Try running the AI matching engine.</p>
                </div>
            `;
            return;
        }

        let html = `<div class="matches-list"><h3>Recent Matches (${data.matches.length})</h3>`;
        
        data.matches.forEach(match => {
            const breakdown = match.score_breakdown || {};
            html += `
                <div class="match-card">
                    <div class="match-card__header">
                        <h4>${match.job_title} at ${match.company}</h4>
                        <span class="match-score">${(match.top_score * 100).toFixed(1)}%</span>
                    </div>
                    <div class="match-card__body">
                        <p><strong>Top Candidate:</strong> ${match.top_candidate}</p>
                        <div class="score-breakdown">
                            <h5>Score Breakdown:</h5>
                            <div class="breakdown-item">
                                <span>Skills Match:
                                    <span class="info-icon-container">
                                        <span class="info-icon">
                                            <svg xmlns="http://www.w3.org/2000/svg" 
                                                 class="icon info-icon" width="20" height="20" 
                                                 fill="none" stroke="currentColor" stroke-width="2" 
                                                 viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
                                              <!-- Outer circle -->
                                              <path d="M12 2a10 10 0 1 0 0 20a10 10 0 0 0 0-20z"/>
                                              <!-- Stem of the "i" -->
                                              <path d="M11 12h2v4h-2z"/>
                                              <!-- Dot of the "i" -->
                                              <circle cx="12" cy="8" r="1"/>
                                            </svg>
                                        </span>
                                        <div class="tooltip">"Weighted keyword matching between job requirements and candidate skills. Higher weights for technical skills like Python (15%), JavaScript (12%), etc."</div>
                                    </span>                                
                                </span>
                                <span>${breakdown.skills || 0}%</span>
                            </div>
                            <div class="breakdown-item">
                                <span>Location:
                                    <span class="info-icon-container">
                                        <span class="info-icon">
                                            <svg xmlns="http://www.w3.org/2000/svg" 
                                                 class="icon info-icon" width="20" height="20" 
                                                 fill="none" stroke="currentColor" stroke-width="2" 
                                                 viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
                                              <!-- Outer circle -->
                                              <path d="M12 2a10 10 0 1 0 0 20a10 10 0 0 0 0-20z"/>
                                              <!-- Stem of the "i" -->
                                              <path d="M11 12h2v4h-2z"/>
                                              <!-- Dot of the "i" -->
                                              <circle cx="12" cy="8" r="1"/>
                                            </svg>
                                        </span>
                                        <div class="tooltip">"Global location compatibility considering geographic proximity, remote work, visa complexity, and timezone differences."</div>
                                    </span>                                                               
                                </span>
                                <span>${breakdown.location || 0}%</span>
                            </div>
                            <div class="breakdown-item">
                                <span>Experience:
                                    <span class="info-icon-container">
                                        <span class="info-icon">
                                            <svg xmlns="http://www.w3.org/2000/svg" 
                                                 class="icon info-icon" width="20" height="20" 
                                                 fill="none" stroke="currentColor" stroke-width="2" 
                                                 viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
                                              <!-- Outer circle -->
                                              <path d="M12 2a10 10 0 1 0 0 20a10 10 0 0 0 0-20z"/>
                                              <!-- Stem of the "i" -->
                                              <path d="M11 12h2v4h-2z"/>
                                              <!-- Dot of the "i" -->
                                              <circle cx="12" cy="8" r="1"/>
                                            </svg>
                                        </span>
                                        <div class="tooltip">"Experience level matching based on job title keywords (senior/junior/entry) and years of experience comparison."</div>
                                    </span>                                                                
                                </span>
                                <span>${breakdown.experience || 0}%</span>
                            </div>
                            <div class="breakdown-item">
                                <span>Profile Relevance:
                                    <span class="info-icon-container">
                                        <span class="info-icon">
                                            <svg xmlns="http://www.w3.org/2000/svg" 
                                                 class="icon info-icon" width="20" height="20" 
                                                 fill="none" stroke="currentColor" stroke-width="2" 
                                                 viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
                                              <!-- Outer circle -->
                                              <path d="M12 2a10 10 0 1 0 0 20a10 10 0 0 0 0-20z"/>
                                              <!-- Stem of the "i" -->
                                              <path d="M11 12h2v4h-2z"/>
                                              <!-- Dot of the "i" -->
                                              <circle cx="12" cy="8" r="1"/>
                                            </svg>
                                        </span>
                                        <div class="tooltip">"Semantic similarity using ChromaDB vector search. Analyzes contextual meaning beyond keywords using AI embeddings."</div>
                                    </span>                                
                                </span>
                                <span>${breakdown.semantic || 0}%</span>
                            </div> 
                            <div class="breakdown-item">
                                <span>Cultural Fit:
                                    <span class="info-icon-container">
                                        <span class="info-icon">
                                            <svg xmlns="http://www.w3.org/2000/svg" 
                                                 class="icon info-icon" width="20" height="20" 
                                                 fill="none" stroke="currentColor" stroke-width="2" 
                                                 viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
                                              <!-- Outer circle -->
                                              <path d="M12 2a10 10 0 1 0 0 20a10 10 0 0 0 0-20z"/>
                                              <!-- Stem of the "i" -->
                                              <path d="M11 12h2v4h-2z"/>
                                              <!-- Dot of the "i" -->
                                              <circle cx="12" cy="8" r="1"/>
                                            </svg>
                                        </span>
                                        <div class="tooltip">"Hybrid scoring: 70% keyword matching (teamwork, innovation, work environment, work pace, customer focus) + 30% semantic analysis of cultural context."</div>
                                    </span>                                
                                </span>
                                <span>${breakdown.cultural_fit || 0}%</span>
                            </div>
                            ${match.cultural_breakdown ? `
                            <div class="cultural-breakdown" style="margin-left: 10px; font-size: 0.8em; color: #666;">
                                <small>
                                    (${match.cultural_breakdown.keyword_score || 0}% Keywords + ${match.cultural_breakdown.semantic_score || 0}% Semantic)
                                </small>
                            </div>
                            ` : ''}
                            
                            <div class="breakdown-item">
                                <span>Growth Potential:</span>
                                <span>50%</span>
                            </div>
                        </div>
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
    // Redirect to candidates page instead of alert
    window.location.href = '/candidates';
}

function loadJobs() {
    alert('Jobs view coming soon');
}

// Global instance
const dashboardModule = new DashboardModule();

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => dashboardModule.init());