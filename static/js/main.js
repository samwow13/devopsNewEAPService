// Panel visibility and expansion controls
document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    const panelToggleCheckbox = document.getElementById('panelToggle');
    const accordionItems = document.querySelectorAll('.accordion-item');
    
    // Handle show/hide panels checkbox
    if (panelToggleCheckbox) {
        panelToggleCheckbox.addEventListener('change', function() {
            accordionItems.forEach(item => {
                item.style.display = this.checked ? 'block' : 'none';
            });
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
    const autoFillButton = document.getElementById('autoFillButton');

    async function executeCommand() {
        if (!commandInput.value.trim()) {
            alert('Please enter a command');
            return;
        }

        executeCommandBtn.disabled = true;
        executeCommandBtn.textContent = 'Executing...';

        try {
            const response = await fetch('/ps/execute-command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: commandInput.value })
            });

            const result = await response.json();
            
            outputContainer.style.display = 'block';
            outputElement.textContent = result.output;
            outputContainer.className = `mt-3 border p-3 ${result.status === 'success' ? 'border-success' : 'border-danger'}`;

        } catch (error) {
            console.error('Error executing command:', error);
            outputContainer.style.display = 'block';
            outputElement.textContent = 'Error executing command: ' + error.toString();
            outputContainer.className = 'mt-3 border border-danger p-3';
        } finally {
            executeCommandBtn.disabled = false;
            executeCommandBtn.textContent = 'Execute';
        }
    }

    if (executeCommandBtn && commandInput) {
        // Execute command when button is clicked
        executeCommandBtn.addEventListener('click', async function() {
            await executeCommand();
        });

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

    if (autoFillButton && commandInput) {
        autoFillButton.addEventListener('click', function() {
            const psScript = `$processes = @('notepad', 'SnippingTool', 'calc', 'mspaint')\nforeach ($proc in $processes) {\n    if (Get-Process -Name $proc -ErrorAction SilentlyContinue) {\n        Write-Output "$proc is running"\n    } else {\n        Write-Output "$proc is not running"\n    }\n}`;
            commandInput.value = psScript;
        });
    }
});
