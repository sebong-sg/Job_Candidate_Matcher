// UI Utility Functions
class UIUtils {
    static showNotification(message, type = 'info', duration = 5000) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification--${type}`;
        notification.innerHTML = `
            <div class="notification__content">
                <span class="notification__icon">${this.getNotificationIcon(type)}</span>
                <span class="notification__message">${message}</span>
                <button class="notification__close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;

        // Add styles if not already added
        if (!document.querySelector('#notification-styles')) {
            const styles = document.createElement('style');
            styles.id = 'notification-styles';
            styles.textContent = `
                .notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                    border-left: 4px solid #3b82f6;
                    z-index: 1000;
                    max-width: 400px;
                    animation: slideIn 0.3s ease;
                }
                .notification--success { border-left-color: #10b981; }
                .notification--error { border-left-color: #ef4444; }
                .notification--warning { border-left-color: #f59e0b; }
                .notification__content {
                    padding: 12px 16px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }
                .notification__close {
                    background: none;
                    border: none;
                    font-size: 18px;
                    cursor: pointer;
                    margin-left: auto;
                }
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
            `;
            document.head.appendChild(styles);
        }

        document.body.appendChild(notification);

        // Auto remove after duration
        if (duration > 0) {
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, duration);
        }

        return notification;
    }

    static getNotificationIcon(type) {
        const icons = {
            info: 'ℹ️',
            success: '✅',
            error: '❌',
            warning: '⚠️'
        };
        return icons[type] || icons.info;
    }

    static toggleLoading(element, isLoading) {
        if (isLoading) {
            element.setAttribute('data-original-text', element.textContent);
            element.innerHTML = '<div class="loading-spinner small"></div> Loading...';
            element.disabled = true;
        } else {
            const originalText = element.getAttribute('data-original-text');
            if (originalText) {
                element.textContent = originalText;
            }
            element.disabled = false;
        }
    }

    static formatNumber(number) {
        return new Intl.NumberFormat().format(number);
    }

    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Make available globally
window.UIUtils = UIUtils;