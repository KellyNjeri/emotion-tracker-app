document.addEventListener('DOMContentLoaded', function() {
    // Form validation enhancements
    enhanceForms();
    
    // Mobile menu handling
    initMobileMenu();
    
    // Health tip interactions
    initHealthTips();
    
    // Entry management
    initEntryManagement();
});

function enhanceForms() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

function initMobileMenu() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', () => {
            navbarCollapse.classList.toggle('show');
        });
        
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navbarCollapse.classList.remove('show');
            });
        });
    }
}

function initHealthTips() {
    const healthTipElement = document.querySelector('.health-tip');
    if (healthTipElement) {
        healthTipElement.addEventListener('click', function() {
            this.classList.toggle('expanded');
        });
    }
}

function initEntryManagement() {
    const deleteButtons = document.querySelectorAll('.delete-entry');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this entry?')) {
                e.preventDefault();
            }
        });
    });
}

async function fetchUserEntries() {
    try {
        const response = await fetch('/api/entries');
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to fetch entries');
    } catch (error) {
        console.error('Error fetching entries:', error);
        return [];
    }
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.querySelector('.container').prepend(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}