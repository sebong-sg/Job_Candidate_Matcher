// Main Application JavaScript
class App {
    constructor() {
        this.init();
    }

    init() {
        console.log('🚀 AI Job Matcher Pro - Professional UI Initialized');
        this.setupEventListeners();
        this.loadInitialData();
    }

    setupEventListeners() {
        // Menu toggle for responsive design
        const menuToggle = document.getElementById('menuToggle');
        if (menuToggle) {
            menuToggle.addEventListener('click', this.toggleSidebar.bind(this));
        }

        // Global error handler
        window.addEventListener('error', this.handleGlobalError.bind(this));
    }

    toggleSidebar() {
        const sidebar = document.querySelector('.sidebar');
        const mainContent = document.querySelector('.main-content');
        
        sidebar.classList.toggle('sidebar--collapsed');
        mainContent.classList.toggle('main-content--expanded');
        
        console.log('Sidebar toggled');
    }

    handleGlobalError(event) {
        console.error('Global error:', event.error);
        // You could show a user-friendly error message here
    }

    loadInitialData() {
        // Any global data that needs to be loaded on app start
        console.log('Loading initial application data...');
    }

    // Utility method for making API calls
    async apiCall(endpoint, options = {}) {
        try {
            const response = await fetch(endpoint, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API call failed:', error);
            throw error;
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.app = new App();
});

// Global utility functions
window.showLoading = function(element) {
    if (element) {
        element.innerHTML = `
            <div class="loading-state">
                <div class="loading-spinner"></div>
                <p>Loading...</p>
            </div>
        `;
    }
};

window.showError = function(element, message) {
    if (element) {
        element.innerHTML = `
            <div class="error-state">
                <div>❌</div>
                <p>${message}</p>
                <button onclick="location.reload()" class="btn btn--outline">Retry</button>
            </div>
        `;
    }
};