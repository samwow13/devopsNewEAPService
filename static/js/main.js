// Panel visibility and expansion controls
document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    const panelToggleCheckbox = document.getElementById('panelToggle');
    const panels = document.querySelectorAll('.expansion-panel');
    
    // Initialize panel states
    panels.forEach(panel => {
        const header = panel.querySelector('.panel-header');
        const content = panel.querySelector('.panel-content');
        const arrow = header.querySelector('.panel-arrow');
        
        // Set initial state
        content.style.display = 'none';
        
        // Add click event to header
        header.addEventListener('click', () => {
            const isExpanded = content.style.display === 'block';
            
            // Toggle content visibility
            content.style.display = isExpanded ? 'none' : 'block';
            
            // Update arrow rotation
            arrow.style.transform = isExpanded ? 'rotate(0deg)' : 'rotate(90deg)';
        });
    });

    // Handle show/hide panels checkbox
    if (panelToggleCheckbox) {
        panelToggleCheckbox.addEventListener('change', function() {
            panels.forEach(panel => {
                panel.style.display = this.checked ? 'block' : 'none';
            });
        });
    }
});
