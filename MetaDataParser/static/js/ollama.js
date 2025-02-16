document.addEventListener('DOMContentLoaded', function() {
    const ollamaForm = document.getElementById('ollama-form');
    const responseElement = document.getElementById('ollama-response');

    ollamaForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading state
        responseElement.textContent = 'Loading...';
        
        // Get form data
        const formData = {
            model_name: document.getElementById('model_name').value,
            prompt: document.getElementById('prompt').value,
            context: document.getElementById('context').value || ''
        };

        try {
            const response = await fetch('/api/ollama', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Format and display the response
            responseElement.innerHTML = `<code>${data.response.replace(/\n/g, '<br>')}</code>`;

        } catch (error) {
            console.error('Error:', error);
            responseElement.innerHTML = `<span class="text-danger">Error: ${error.message}</span>`;
        }
    });
});
