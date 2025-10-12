// Formatters Utility Module
class Formatters {
    static formatExperience(years) {
        if (!years && years !== 0) return 'No exp';
        return `${years} ${years === 1 ? 'year' : 'years'}`;
    }

    static truncateText(text, length) {
        if (!text) return 'No profile available';
        return text.length > length ? text.substring(0, length) + '...' : text;
    }

    static formatPercentage(decimal) {
        return `${Math.round(decimal * 100)}%`;
    }

    static capitalizeWords(str) {
        return str.replace(/\b\w/g, l => l.toUpperCase());
    }
}

// Global instance
window.Formatters = Formatters;
