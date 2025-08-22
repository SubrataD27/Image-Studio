// Custom JavaScript for AI Image Studio - Designed by Subrata

document.addEventListener('DOMContentLoaded', function() {
    // Initialize app
    initializeApp();
});

function initializeApp() {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.getElementById('uploadForm');
    const submitBtn = document.getElementById('submitBtn');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const operationType = document.getElementById('operationType');
    const submitText = document.getElementById('submitText');
    const controlsPanel = document.getElementById('controlsPanel');

    // Feature configurations
    const featureConfig = {
        'remove_bg': {
            title: 'Remove Background',
            icon: 'fa-magic',
            color: '#6366f1'
        },
        'compress': {
            title: 'Compress Image',
            icon: 'fa-compress-alt',
            color: '#f59e0b'
        },
        'resize': {
            title: 'Resize Image',
            icon: 'fa-expand-arrows-alt',
            color: '#3b82f6'
        },
        'change_bg': {
            title: 'Change Background',
            icon: 'fa-palette',
            color: '#10b981'
        },
        'enhance': {
            title: 'Enhance Image',
            icon: 'fa-adjust',
            color: '#ef4444'
        },
        'blur': {
            title: 'Apply Blur Effect',
            icon: 'fa-eye-slash',
            color: '#6b7280'
        }
    };

    // Feature selection
    document.querySelectorAll('.feature-card').forEach(card => {
        card.addEventListener('click', function() {
            // Remove active class from all cards
            document.querySelectorAll('.feature-card').forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked card
            this.classList.add('active');
            
            const feature = this.dataset.feature;
            const config = featureConfig[feature];
            
            // Update form
            operationType.value = feature;
            submitText.textContent = config.title;
            
            // Update button icon
            const btnIcon = submitBtn.querySelector('i');
            btnIcon.className = `fas ${config.icon} me-2`;
            
            // Show/hide controls
            showControls(feature);
            
            // Add visual feedback
            addClickEffect(this);
        });
    });

    // Controls visibility
    function showControls(feature) {
        const allControls = document.querySelectorAll('.control-section');
        allControls.forEach(control => control.style.display = 'none');
        
        if (feature !== 'remove_bg') {
            controlsPanel.style.display = 'block';
            const targetControl = document.getElementById(feature + 'Controls');
            if (targetControl) {
                targetControl.style.display = 'block';
            }
        } else {
            controlsPanel.style.display = 'none';
        }
    }

    // Click effect animation
    function addClickEffect(element) {
        element.style.transform = 'scale(0.95)';
        setTimeout(() => {
            element.style.transform = '';
        }, 150);
    }

    // Slider value updates
    const sliders = ['quality', 'brightness', 'contrast', 'saturation', 'sharpness', 'blur'];
    sliders.forEach(sliderName => {
        const slider = document.getElementById(sliderName + 'Slider');
        const valueDisplay = document.getElementById(sliderName + 'Value');
        
        if (slider && valueDisplay) {
            slider.addEventListener('input', function() {
                valueDisplay.textContent = this.value;
                addSliderGlow(this);
            });
        }
    });

    // Slider glow effect
    function addSliderGlow(slider) {
        slider.style.boxShadow = '0 0 15px rgba(99, 102, 241, 0.5)';
        setTimeout(() => {
            slider.style.boxShadow = '';
        }, 300);
    }

    // Drag and drop functionality
    if (uploadZone) {
        uploadZone.addEventListener('dragover', handleDragOver);
        uploadZone.addEventListener('dragleave', handleDragLeave);
        uploadZone.addEventListener('drop', handleDrop);
        uploadZone.addEventListener('click', () => fileInput.click());
    }

    function handleDragOver(e) {
        e.preventDefault();
        uploadZone.classList.add('drag-over');
        uploadZone.style.borderColor = '#10b981';
        uploadZone.style.background = 'rgba(16, 185, 129, 0.1)';
    }

    function handleDragLeave(e) {
        e.preventDefault();
        uploadZone.classList.remove('drag-over');
        uploadZone.style.borderColor = '';
        uploadZone.style.background = '';
    }

    function handleDrop(e) {
        e.preventDefault();
        handleDragLeave(e);
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            updateFileDisplay(files[0].name);
        }
    }

    // File input change
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                updateFileDisplay(e.target.files[0].name);
            }
        });
    }

    // Update file display
    function updateFileDisplay(fileName) {
        const uploadTitle = uploadZone.querySelector('.upload-title');
        const uploadIcon = uploadZone.querySelector('.upload-icon');
        
        uploadIcon.className = 'fas fa-check-circle upload-icon';
        uploadIcon.style.color = '#10b981';
        uploadTitle.innerHTML = `<i class="fas fa-check-circle me-2"></i>Selected: ${fileName}`;
        
        uploadZone.style.borderColor = '#10b981';
        uploadZone.style.background = 'rgba(16, 185, 129, 0.1)';
        
        // Add success animation
        uploadZone.style.transform = 'scale(1.02)';
        setTimeout(() => {
            uploadZone.style.transform = '';
        }, 300);
    }

    // Form submission
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            if (!fileInput.files.length) {
                e.preventDefault();
                showNotification('Please select a file first!', 'error');
                return;
            }
            
            showLoading();
        });
    }

    // Show loading state
    function showLoading() {
        submitBtn.style.display = 'none';
        loadingSpinner.style.display = 'block';
        
        // Animate loading text
        const loadingText = loadingSpinner.querySelector('p');
        if (loadingText) {
            animateLoadingText(loadingText);
        }
    }

    // Animate loading text
    function animateLoadingText(element) {
        const texts = [
            'AI is analyzing your image...',
            'Processing with advanced algorithms...',
            'Almost done, creating magic...',
            'Finalizing your masterpiece...'
        ];
        
        let index = 0;
        const interval = setInterval(() => {
            element.textContent = texts[index];
            index = (index + 1) % texts.length;
        }, 2000);
        
        // Store interval to clear it later if needed
        window.loadingInterval = interval;
    }

    // Notification system
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
            ${message}
        `;
        
        // Add notification styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'error' ? '#ef4444' : '#3b82f6'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    // Add custom animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    // Initialize tooltips for better UX
    initializeTooltips();
}

// Tooltip system
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            showTooltip(this, this.dataset.tooltip);
        });
        
        element.addEventListener('mouseleave', function() {
            hideTooltip();
        });
    });
}

function showTooltip(element, text) {
    const tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip';
    tooltip.textContent = text;
    tooltip.style.cssText = `
        position: absolute;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        z-index: 1001;
        pointer-events: none;
        white-space: nowrap;
    `;
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.left = `${rect.left + rect.width / 2 - tooltip.offsetWidth / 2}px`;
    tooltip.style.top = `${rect.top - tooltip.offsetHeight - 10}px`;
    
    // Store reference for cleanup
    window.currentTooltip = tooltip;
}

function hideTooltip() {
    if (window.currentTooltip) {
        document.body.removeChild(window.currentTooltip);
        window.currentTooltip = null;
    }
}

// Smooth scrolling for better UX
function smoothScrollTo(element) {
    element.scrollIntoView({
        behavior: 'smooth',
        block: 'center'
    });
}

// Show notification function
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
            <span>${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    // Add styles if not already added
    if (!document.getElementById('notification-styles')) {
        const styles = document.createElement('style');
        styles.id = 'notification-styles';
        styles.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                z-index: 10000;
                animation: slideIn 0.3s ease-out;
                max-width: 400px;
                border-left: 4px solid;
            }
            .notification-success { border-left-color: #10b981; }
            .notification-error { border-left-color: #ef4444; }
            .notification-info { border-left-color: #3b82f6; }
            .notification-content {
                padding: 15px 20px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .notification-close {
                background: none;
                border: none;
                margin-left: auto;
                color: #6b7280;
                cursor: pointer;
            }
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(styles);
    }
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Add some Easter eggs for fun
let clickCount = 0;
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('logo-icon')) {
        clickCount++;
        if (clickCount === 5) {
            showNotification('🎉 You found the Easter egg! Made with extra love by Subrata!', 'info');
            clickCount = 0;
        }
    }
});
