// Charts and Visualization Module
class ChartsModule {
    constructor() {
        this.initialized = false;
    }

    init() {
        if (this.initialized) return;
        console.log('📊 Charts module initialized');
        this.initialized = true;
    }

    createMatchDistributionChart(data, container) {
        if (!container) return;

        // Simple bar chart using CSS - in a real app you'd use Chart.js or similar
        const scores = data.matches || [];
        const scoreRanges = {
            'A+ (90-100%)': 0,
            'A (80-89%)': 0,
            'B+ (70-79%)': 0,
            'B (60-69%)': 0,
            'C (Below 60%)': 0
        };

        scores.forEach(match => {
            const score = match.top_score * 100;
            if (score >= 90) scoreRanges['A+ (90-100%)']++;
            else if (score >= 80) scoreRanges['A (80-89%)']++;
            else if (score >= 70) scoreRanges['B+ (70-79%)']++;
            else if (score >= 60) scoreRanges['B (60-69%)']++;
            else scoreRanges['C (Below 60%)']++;
        });

        const html = `
            <div class="chart-container">
                <h4>Match Score Distribution</h4>
                <div class="bar-chart">
                    ${Object.entries(scoreRanges).map(([range, count]) => `
                        <div class="bar-chart__item">
                            <div class="bar-chart__label">${range}</div>
                            <div class="bar-chart__bar-container">
                                <div class="bar-chart__bar" style="width: ${(count / Math.max(1, scores.length)) * 100}%">
                                    <span class="bar-chart__value">${count}</span>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    createSkillsChart(skillsData, container) {
        if (!container) return;

        const html = `
            <div class="chart-container">
                <h4>Top Required Skills</h4>
                <div class="skills-chart">
                    ${skillsData.slice(0, 8).map(skill => `
                        <div class="skills-chart__item">
                            <div class="skills-chart__skill">${Formatters.capitalizeWords(skill.name)}</div>
                            <div class="skills-chart__count">${skill.count}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        container.innerHTML = html;
    }
}

// Global instance
window.chartsModule = new ChartsModule();