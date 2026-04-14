// Admin Script Principal
document.addEventListener('DOMContentLoaded', function() {
    // Toggle sidebar sur mobile
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
        });
    }
    
    // Fermer les alertes
    const closeAlerts = document.querySelectorAll('.close-alert');
    closeAlerts.forEach(function(closeBtn) {
        closeBtn.addEventListener('click', function() {
            this.parentElement.remove();
        });
    });
    
    // Auto-fermeture des alertes après 5 secondes
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            alert.style.transition = 'opacity 0.5s ease-out';
            alert.style.opacity = '0';
            setTimeout(function() {
                if (alert.parentElement) {
                    alert.remove();
                }
            }, 500);
        });
    }, 5000);
    
    // Gestion des tooltips
    const tooltipElements = document.querySelectorAll('[title]');
    tooltipElements.forEach(function(element) {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('title');
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.position = 'absolute';
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 10) + 'px';
            tooltip.style.left = (rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)) + 'px';
            tooltip.style.backgroundColor = '#333';
            tooltip.style.color = 'white';
            tooltip.style.padding = '5px 10px';
            tooltip.style.borderRadius = '4px';
            tooltip.style.fontSize = '12px';
            tooltip.style.zIndex = '1000';
            tooltip.style.whiteSpace = 'nowrap';
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltip = document.querySelector('.tooltip');
            if (tooltip) {
                tooltip.remove();
            }
        });
    });
}); 
// Confirmation de suppression
const deleteLinks = document.querySelectorAll('a[href*="delete"]');
