document.addEventListener('DOMContentLoaded', function() {
    const ollamaForm = document.getElementById('ollama-form');
    const responseElement = document.getElementById('ollama-response');
    const loadingSpinner = document.getElementById('loading-spinner');
    const errorDisplay = document.getElementById('error-display');
    const statusMessages = document.getElementById('status-messages');
    const copyButton = document.getElementById('copy-button');
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Copy to clipboard functionality
    copyButton.addEventListener('click', async function() {
        try {
            const text = responseElement.textContent;
            await navigator.clipboard.writeText(text);
            
            // Visual feedback
            const tooltip = bootstrap.Tooltip.getInstance(copyButton);
            copyButton.setAttribute('data-bs-original-title', 'Copied!');
            tooltip.show();
            
            // Reset tooltip after 2 seconds
            setTimeout(() => {
                copyButton.setAttribute('data-bs-original-title', 'Copy to clipboard');
                tooltip.hide();
            }, 2000);
            
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
    });

    function updateStatus(message, type = 'info') {
        // const statusDiv = document.createElement('div');
        // statusDiv.className = `alert alert-${type} mb-2`;
        // statusDiv.textContent = message;
        // statusMessages.prepend(statusDiv);
        // setTimeout(() => statusDiv.remove(), 5000);
    }

    ollamaForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Reset display states
        errorDisplay.classList.add('d-none');
        loadingSpinner.classList.remove('d-none');
        responseElement.textContent = 'Processing request...';
        
        // Get form data
        const formData = {
            model_name: document.getElementById('model_name').value,
            prompt: document.getElementById('prompt').value,
            context: document.getElementById('context').value || '',
            embedding_model : document.getElementById('embedding_model').value
        };

        try {
            updateStatus('Sending request to Ollama service...');
            const response = await fetch('/api/ollama', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                responseElement.textContent = 'An error occurred while processing the request.';
                throw new Error(`Server responded with status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }

            // Format and display the response
            responseElement.innerHTML = `<code>${data.response.replace(/\n/g, '<br>')}</code>`;
            updateStatus('Response generated successfully', 'success');

        } catch (error) {
            console.error('Error:', error);
            errorDisplay.textContent = `Error: ${error.message}`;
            errorDisplay.classList.remove('d-none');
            updateStatus(error.message, 'danger');
        } finally {
            loadingSpinner.classList.add('d-none');
        }
    });
});
