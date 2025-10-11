// Data Formatting Utilities
class Formatters {
    static formatPercentage(value, decimals = 1) {
        if (value === null || value === undefined) return '0%';
        return `${(value * 100).toFixed(decimals)}%`;
    }

    static formatScore(score) {
        if (score >= 0.9) return 'A+';
        if (score >= 0.8) return 'A';
        if (score >= 0.7) return 'B+';
        if (score >= 0.6) return 'B';
        if (score >= 0.5) return 'C+';
        return 'C';
    }

    static formatExperience(years) {
        if (years === 1) return '1 year';
        if (years > 1) return `${years} years`;
        return 'Less than 1 year';
    }

    static formatDate(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }

    static formatSkills(skills, max = 5) {
        if (!skills || !Array.isArray(skills)) return [];
        return skills.slice(0, max);
    }

    static truncateText(text, maxLength = 100) {
        if (!text) return '';
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }

    static capitalizeWords(str) {
        if (!str) return '';
        return str.replace(/\b\w/g, char => char.toUpperCase());
    }
}

// Make available globally
window.Formatters = Formatters;