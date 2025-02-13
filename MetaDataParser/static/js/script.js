const llmModelOptions = {
    groq: [
        { value: 'llama-3.1-8b-instant', label: 'Llama 3.1 8B Instant' },
        { value: 'llama-3.3-70b-versatile', label: 'Llama 3.3 70B Versatile' }
    ],
    groq_ingest: [
        { value: 'llama-3.1-8b-instant', label: 'Llama 3.1 8B Instant' },
        { value: 'llama-3.3-70b-versatile', label: 'Llama 3.3 70B Versatile' }
    ],
    gemini: [
        { value: 'gemini-1.5-pro-latest', label: 'Gemini 1.5 Pro' }
    ]
};

document.getElementById("ai_model").addEventListener("change", function() {
    const llmModelSelect = document.getElementById("llm_model");
    const selectedAiModel = this.value;
    
    // Clear existing options
    llmModelSelect.innerHTML = '';
    
    if (selectedAiModel) {
        llmModelSelect.disabled = false;
        
        // Add default option
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.disabled = true;
        defaultOption.selected = true;
        defaultOption.textContent = 'Select LLM Model';
        llmModelSelect.appendChild(defaultOption);
        
        // Add model-specific options
        const options = llmModelOptions[selectedAiModel] || [];
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option.value;
            optionElement.textContent = option.label;
            llmModelSelect.appendChild(optionElement);
        });
    } else {
        llmModelSelect.disabled = true;
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.disabled = true;
        defaultOption.selected = true;
        defaultOption.textContent = 'Select AI Model first';
        llmModelSelect.appendChild(defaultOption);
    }
});

document.getElementById("metadata-form").addEventListener("submit", async function(e) {
    e.preventDefault();
    const countryCode = document.getElementById("country_code").value;
    const paymentMethod = document.getElementById("payment_method").value;
    const ai_model = document.getElementById("ai_model").value;    
    const llm_model = document.getElementById("llm_model").value;
    const output = document.getElementById("output");
    const previewBtn = document.getElementById("previewBtn");
    const copyBtn = document.getElementById("copyBtn");
    
    output.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
    previewBtn.style.display = 'none';
    copyBtn.style.display = 'none';

    try {
        const response = await fetch("/generate-metadata", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `country_code=${encodeURIComponent(countryCode)}&payment_method=${encodeURIComponent(paymentMethod)}&ai_model=${encodeURIComponent(ai_model)}&llm_model=${encodeURIComponent(llm_model)}`
        });

        if (response.ok) {
            const data = await response.json();
            data.metadata = data.metadata || "{}";
            const formattedJson = JSON.stringify(JSON.parse(data.metadata, null, 2), null, 2);
            output.innerHTML = `<pre class="json-output"><code>${formattedJson}</code></pre>`;
            previewBtn.style.display = 'inline';
            copyBtn.style.display = 'inline';

            // Preview button functionality
            previewBtn.addEventListener("click", () => {
                document.getElementById("modalOutput").textContent = formattedJson;
                const previewModal = new bootstrap.Modal(document.getElementById("previewModal"));
                previewModal.show();
            });

            // Copy button functionality
            copyBtn.addEventListener("click", function() {
                navigator.clipboard.writeText(formattedJson).then(() => {
                    this.classList.remove('fa-copy');
                    this.classList.add('fa-check');
                    setTimeout(() => {
                        this.classList.remove('fa-check');
                        this.classList.add('fa-copy');
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy: ', err);
                });
            });
        } else {
            const error = await response.json();
            output.innerHTML = `<div class="alert alert-danger" role="alert"><i class="fas fa-exclamation-triangle me-2"></i>Error: ${error.error}</div>`;
        }
    } catch (error) {
        output.innerHTML = `<div class="alert alert-danger" role="alert"><i class="fas fa-exclamation-triangle me-2"></i>Network Error: ${error.message}</div>`;
    }
});