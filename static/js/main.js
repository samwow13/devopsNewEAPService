// Panel visibility and expansion controls
document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    const togglePanelsCheckbox = document.getElementById('togglePanels');
    const panels = document.querySelectorAll('.expansion-panel');
    
    // Initialize panel states
    panels.forEach(panel => {
        const header = panel.querySelector('.panel-header');
        const content = panel.querySelector('.panel-content');
        const icon = header.querySelector('.expand-icon');
        
        // Set initial state
        content.style.display = 'none';
        
        // Add click event to header
        header.addEventListener('click', () => {
            const isExpanded = content.style.display === 'block';
            
            // Toggle content visibility
            content.style.display = isExpanded ? 'none' : 'block';
            
            // Update icon rotation
            icon.style.transform = isExpanded ? 'rotate(-90deg)' : 'rotate(0deg)';
        });
    });

    // Handle show/hide panels checkbox
    togglePanelsCheckbox.addEventListener('change', function() {
        panels.forEach(panel => {
            panel.style.display = this.checked ? 'block' : 'none';
        });
    });
});
