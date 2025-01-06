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

// PowerShell Mode Management
function updatePSMode(mode) {
    const psModeElement = document.getElementById('psMode');
    if (psModeElement) {
        psModeElement.textContent = `PS Mode: ${mode}`;
        psModeElement.className = `badge ${mode === 'Remote' ? 'bg-primary' : 'bg-secondary'} me-3`;
    }
}

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
            
            // Update PS mode indicator
            updatePSMode(result.mode);
            
            outputContainer.style.display = 'block';
            outputElement.textContent = result.output;
            outputContainer.className = `mt-3 border p-3 ${result.status === 'success' ? 'border-success' : 'border-danger'}`;

            // Update process table if process data is available
            if (result.processData) {
                updateProcessTable(result.processData);
            }
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
            updateProcessTable(outputElement.textContent);
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

// Environment Selection Handler
document.addEventListener('DOMContentLoaded', function() {
    const environmentSelect = document.getElementById('environmentSelect');
    if (environmentSelect) {
        environmentSelect.addEventListener('change', async function() {
            const selectedEnvironment = this.value;
            
            // Clear existing interval if any
            if (processStatusInterval) {
                clearInterval(processStatusInterval);
                processStatusInterval = null;
            }
            
            try {
                const response = await fetch('/environment/select', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ environment: selectedEnvironment })
                });

                const result = await response.json();
                
                if (result.process_statuses) {
                    // Convert process statuses to the format expected by updateProcessTable
                    const processOutput = Object.entries(result.process_statuses)
                        .map(([process, status]) => `${process} is ${status.toLowerCase()}`)
                        .join('\n');
                    
                    updateProcessTable(processOutput);
                }
                
                // Start auto-refresh interval (for any environment)
                processStatusInterval = setInterval(refreshProcessStatus, 10000);
                
                // Update PS Mode
                updatePSMode(selectedEnvironment === 'Local' ? 'Local' : 'Remote');
                
            } catch (error) {
                console.error('Error selecting environment:', error);
                alert('Failed to select environment. Please try again.');
            }
        });
        
        // Trigger change event on initial load to set up initial state
        environmentSelect.dispatchEvent(new Event('change'));
    }
});

// Process Status Auto-Refresh
let processStatusInterval = null;

async function refreshProcessStatus() {
    const environmentSelect = document.getElementById('environmentSelect');
    if (!environmentSelect) return;
    
    try {
        // Get current process statuses from the server
        const response = await fetch('/environment/status', {
            method: 'GET'
        });

        const result = await response.json();
        if (result.process_statuses) {
            // Convert process statuses to the format expected by updateProcessTable
            const processOutput = Object.entries(result.process_statuses)
                .map(([process, status]) => `${process} is ${status.toLowerCase()}`)
                .join('\n');
            
            updateProcessTable(processOutput);
        }
    } catch (error) {
        console.error('Error refreshing process status:', error);
        // Don't show alert to avoid annoying the user
        // Just log to console and let it try again in 10 seconds
    }
}

// Function to dynamically update the process status table
function updateProcessTable(output) {
    const tableBody = document.getElementById('processStatusTableBody');
    if (!tableBody || !output) return;

    // Clear existing table rows
    tableBody.innerHTML = '';

    // Split the output into lines and process each line
    const lines = output.trim().split('\n');
    lines.forEach(line => {
        line = line.trim();
        if (!line) return;  // Skip empty lines
        
        // Try to match the pattern "processName is status"
        const match = line.match(/^(.+?)\s+is\s+(.+)$/);
        if (match) {
            const [, processName, status] = match;
            const isRunning = status.trim() === 'running';
            const row = document.createElement('tr');
            
            // Process name cell
            const processCell = document.createElement('td');
            processCell.textContent = processName.trim();
            
            // Status cell with dot indicator
            const statusCell = document.createElement('td');
            statusCell.classList.add('text-center');
            
            const statusDot = document.createElement('span');
            statusDot.classList.add('status-indicator');
            statusDot.classList.add(isRunning ? 'status-running' : 'status-stopped');
            
            const statusText = document.createElement('span');
            statusText.classList.add(isRunning ? 'text-success' : 'text-danger');
            statusText.textContent = status.trim();
            
            statusCell.appendChild(statusDot);
            statusCell.appendChild(statusText);
            
            // Actions cell
            const actionsCell = document.createElement('td');
            actionsCell.classList.add('text-center');
            
            const actionButton = document.createElement('button');
            actionButton.type = 'button';
            actionButton.classList.add('btn', 'process-action-btn');
            
            if (isRunning) {
                actionButton.classList.add('btn-danger');
                actionButton.textContent = 'Stop';
                actionButton.onclick = () => handleProcessAction(processName, 'stop');
            } else {
                actionButton.classList.add('btn-success');
                actionButton.textContent = 'Start';
                actionButton.onclick = () => handleProcessAction(processName, 'start');
            }
            
            actionsCell.appendChild(actionButton);
            
            // Add cells to row
            row.appendChild(processCell);
            row.appendChild(statusCell);
            row.appendChild(actionsCell);
            tableBody.appendChild(row);
        }
    });
}

// Function to handle process start/stop actions
async function handleProcessAction(processName, action) {
    const command = action === 'start' 
        ? `Start-Process ${processName}`
        : `Stop-Process -Name ${processName} -Force`;
        
    try {
        const response = await fetch('/ps/execute-command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ command })
        });

        const result = await response.json();
        
        // Refresh the process status after action
        const refreshCommand = `$processes = @('notepad', 'SnippingTool', 'calc', 'mspaint')\nforeach ($proc in $processes) {\n    if (Get-Process -Name $proc -ErrorAction SilentlyContinue) {\n        Write-Output "$proc is running"\n    } else {\n        Write-Output "$proc is not running"\n    }\n}`;
        
        const refreshResponse = await fetch('/ps/execute-command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ command: refreshCommand })
        });

        const refreshResult = await refreshResponse.json();
        updateProcessTable(refreshResult.output);
        
    } catch (error) {
        console.error(`Error ${action}ing process:`, error);
        alert(`Failed to ${action} process. Please try again.`);
    }
}
