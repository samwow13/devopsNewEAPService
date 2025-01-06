// Panel visibility and expansion controls
document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    const panelToggleCheckbox = document.getElementById('panelToggle');
    const accordionItems = document.querySelectorAll('.accordion-item');
    const testConnectionBtn = document.getElementById('testConnection');
    
    // Handle show/hide panels checkbox
    if (panelToggleCheckbox) {
        panelToggleCheckbox.addEventListener('change', function() {
            accordionItems.forEach(item => {
                item.style.display = this.checked ? 'block' : 'none';
            });
        });
    }

    // Handle test connection button
    if (testConnectionBtn) {
        testConnectionBtn.addEventListener('click', async function() {
            const computerName = document.getElementById('computerName').value.trim();
            
            if (!computerName) {
                alert('Please enter a computer name');
                return;
            }

            // Disable button and show loading state
            testConnectionBtn.disabled = true;
            testConnectionBtn.innerHTML = 'Testing...';

            try {
                const response = await fetch('/ps/test-connection', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ computer_name: computerName })
                });

                const result = await response.json();
                
                // Get output container and its elements
                const outputContainer = document.getElementById('psOutputContainer');
                const commandElement = document.getElementById('psCommand');
                const outputElement = document.getElementById('psOutput');

                // Update command and output
                commandElement.textContent = `# Executed PowerShell Command:\n${result.command}`;
                outputElement.textContent = result.raw_output;

                // Show the output container
                outputContainer.style.display = 'block';

                // Add status indicator class
                outputContainer.className = `mt-3 border-${result.status === 'success' ? 'success' : 'danger'}`;

            } catch (error) {
                console.error('Error testing connection:', error);
                
                // Show error in output container
                const outputContainer = document.getElementById('psOutputContainer');
                const commandElement = document.getElementById('psCommand');
                const outputElement = document.getElementById('psOutput');

                commandElement.textContent = '# Error occurred while testing connection';
                outputElement.textContent = error.toString();
                outputContainer.style.display = 'block';
                outputContainer.className = 'mt-3 border-danger';
            } finally {
                // Re-enable button and restore text
                testConnectionBtn.disabled = false;
                testConnectionBtn.innerHTML = 'Test Connection';
            }
        });
    }
});

// PowerShell Command Execution
document.addEventListener('DOMContentLoaded', function() {
    const executeCommandBtn = document.getElementById('executeCommand');
    const clearOutputBtn = document.getElementById('clearOutput');
    const commandInput = document.getElementById('psCommandInput');
    const outputContainer = document.getElementById('psCommandOutput');
    const outputElement = document.getElementById('commandOutput');

    if (executeCommandBtn && commandInput) {
        // Execute command when button is clicked
        executeCommandBtn.addEventListener('click', executeCommand);
        
        // Execute command when Enter is pressed in input
        commandInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                executeCommand();
            }
        });
    }

    if (clearOutputBtn) {
        clearOutputBtn.addEventListener('click', function() {
            outputElement.textContent = '';
            outputContainer.style.display = 'none';
        });
    }

    async function executeCommand() {
        const command = commandInput.value.trim();
        
        if (!command) {
            alert('Please enter a PowerShell command');
            return;
        }

        // Disable button and show loading state
        executeCommandBtn.disabled = true;
        executeCommandBtn.innerHTML = 'Executing...';

        try {
            const response = await fetch('/ps/execute-command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: command })
            });

            const result = await response.json();
            
            // Show the output container
            outputContainer.style.display = 'block';
            
            // Update output
            outputElement.textContent = result.output;

        } catch (error) {
            console.error('Error executing command:', error);
            outputContainer.style.display = 'block';
            outputElement.textContent = `Error executing command: ${error.toString()}`;
        } finally {
            // Re-enable button and restore text
            executeCommandBtn.disabled = false;
            executeCommandBtn.innerHTML = 'Execute';
        }
    }
});
