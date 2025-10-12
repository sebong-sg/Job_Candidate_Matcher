// Advanced Matching Module
class MatchingModule {
    constructor() {
        this.initialized = false;
        this.isRunning = false;
    }

    init() {
        if (this.initialized) return;
        console.log('🤖 Matching module initialized');
        this.initialized = true;
    }

    async runAdvancedMatching(algorithm = 'semantic', limit = 5) {
        // Prevent multiple simultaneous runs
        if (this.isRunning) {
            console.log('Matching already in progress...');
            return;
        }

        this.isRunning = true;
        const resultsContainer = document.getElementById('matchingResults');
        if (!resultsContainer) return;

        // Disable controls during matching
        this.setControlsLoading(true);

        // Show progress
        resultsContainer.innerHTML = this.getProgressHTML();

        try {
            UIUtils.showNotification(`Running ${algorithm} matching...`, 'info');
            
            const data = await api.post('/api/run-matching');
            
            if (data.error) {
                throw new Error(data.error);
            }

            this.displayMatchingResults(data, algorithm, limit);
            UIUtils.showNotification(`Found ${data.matches?.length || 0} job matches`, 'success');
            
        } catch (error) {
            console.error('Matching error:', error);
            resultsContainer.innerHTML = `
                <div class="error-state">
                    <div>❌</div>
                    <h3>Matching Failed</h3>
                    <p>${error.message}</p>
                    <button onclick="matchingModule.runAdvancedMatching()" 
                            class="btn btn--outline">Try Again</button>
                </div>
            `;
            UIUtils.showNotification('Failed to run matching', 'error');
        } finally {
            this.isRunning = false;
            this.setControlsLoading(false);
        }
    }

    setControlsLoading(isLoading) {
        const algorithmSelect = document.getElementById('matchAlgorithm');
        const limitSelect = document.getElementById('resultsLimit');
        const runButton = document.getElementById('runMatchingBtn');

        if (algorithmSelect && limitSelect && runButton) {
            if (isLoading) {
                algorithmSelect.parentElement.classList.add('loading');
                limitSelect.parentElement.classList.add('loading');
                runButton.disabled = true;
                runButton.innerHTML = '<span class="btn__icon">⏳</span> Running...';
            } else {
                algorithmSelect.parentElement.classList.remove('loading');
                limitSelect.parentElement.classList.remove('loading');
                runButton.disabled = false;
                runButton.innerHTML = '<span class="btn__icon">🤖</span> Run AI Matching';
            }
        }
    }

    getProgressHTML() {
        return `
            <div class="matching-progress">
                <div class="progress-steps">
                    <div class="progress-step">
                        <div class="step-icon active">1</div>
                        <div class="step-label">Loading Data</div>
                    </div>
                    <div class="progress-step">
                        <div class="step-icon">2</div>
                        <div class="step-label">Analyzing</div>
                    </div>
                    <div class="progress-step">
                        <div class="step-icon">3</div>
                        <div class="step-label">Matching</div>
                    </div>
                    <div class="progress-step">
                        <div class="step-icon">4</div>
                        <div class="step-label">Results</div>
                    </div>
                </div>
                <div class="loading-state">
                    <div class="loading-spinner"></div>
                    <p>Running AI matching engine...</p>
                </div>
            </div>
        `;
    }

    displayMatchingResults(data, algorithm, limit) {
        const resultsContainer = document.getElementById('matchingResults');
        if (!resultsContainer) return;

        if (!data.matches || data.matches.length === 0) {
            resultsContainer.innerHTML = `
                <div class="empty-state">
                    <svg class="icon" width="48" height="48" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                    <h3>No Matches Found</h3>
                    <p>Try adding more candidates or jobs to get matches.</p>
                </div>
            `;
            return;
        }

        // Apply limit to the number of matches displayed
        const limitedMatches = data.matches.slice(0, limit);

        const html = `
            <div class="match-results-grid">
                <div class="results-header">
                    <h3>Matching Results (${limitedMatches.length} of ${data.matches.length} jobs shown)</h3>
                    <div class="results-info">
                        <span>Algorithm: ${this.formatAlgorithmName(algorithm)}</span>
                        <span>•</span>
                        <span>Showing: Top ${limit} per job</span>
                    </div>
                </div>
                ${limitedMatches.map(match => this.renderJobMatch(match)).join('')}
            </div>
        `;

        resultsContainer.innerHTML = html;
    }

    formatAlgorithmName(algorithm) {
        const names = {
            'semantic': 'Semantic + Skills',
            'skills': 'Skills-Based',
            'hybrid': 'Hybrid'
        };
        return names[algorithm] || algorithm;
    }

    renderJobMatch(match) {
        return `
            <div class="job-match-section">
                <div class="job-match-header">
                    <div class="job-match-title">
                        <h3>${match.job_title}</h3>
                        <div class="company">at ${match.company}</div>
                    </div>
                    <div class="job-match-stats">
                        <div class="top-match-score">
                            <span class="score-value">${Math.round(match.top_score * 100)}%</span>
                            <div class="score-grade">${match.match_grade} Match</div>
                        </div>
                    </div>
                </div>
                <div class="candidate-matches">
                    <div class="candidate-match">
                        <div class="candidate-info">
                            <div class="candidate-name">${match.top_candidate}</div>
                            <div class="candidate-skills">
                                ${match.common_skills.map(skill => 
                                    `<span class="skill-tag">${skill}</span>`
                                ).join('')}
                            </div>
                        </div>
                        <div class="match-score">
                            <div class="score-value">${Math.round(match.top_score * 100)}%</div>
                            <div class="score-grade">Top Match</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
}

// Global instance
window.matchingModule = new MatchingModule();
