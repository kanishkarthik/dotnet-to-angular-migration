const llmModelOptions = {
    groq: [
        { value: 'llama-3.1-8b-instant', label: 'Llama 3.1 8B Instant' },
        { value: 'llama-3.3-70b-versatile', label: 'Llama 3.3 70B Versatile' },
        { value: 'deepseek-r1-distill-llama-70b', label: 'DeepSeek R1 Distill Llama 70B' },
        { value: 'llama3-70b-8192', label : 'Llama 70b 8192' },
    ],
    groq_ingest: [
        { value: 'llama-3.1-8b-instant', label: 'Llama 3.1 8B Instant' },
        { value: 'llama-3.3-70b-versatile', label: 'Llama 3.3 70B Versatile' },
        { value: 'deepseek-r1-distill-llama-70b', label: 'DeepSeek R1 Distill Llama 70B' },
        { value: 'llama3-70b-8192', label : 'Llama 70b 8192' },

    ],
    gemini: [
        { value: 'gemini-1.5-pro-latest', label: 'Gemini 1.5 Pro' },
        { value:'gemini-2.0-flash', label: 'Gemini 2.0 Flash'},
        { value:'gemini-2.0-flash-lite-preview-02-05', label: 'Gemini 2.0 Flash-Lite Preview'}

    ],
    gemini_ingest: [
        { value: 'gemini-1.5-pro-latest', label: 'Gemini 1.5 Pro' }
    ],

};
let vsCodeEditor = null;

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
    const customPrompt = document.getElementById("custom_prompt").value;
    const reindex = document.getElementById("reindex")?.checked || false;
    const output = document.getElementById("output");
    const vsCodeEditorContainer = document.getElementById("vscodeeditor-container");
    const previewBtn = document.getElementById("previewBtn");
    const copyBtn = document.getElementById("copyBtn");
    const saveBtn = document.getElementById("saveBtn");
    
    output.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
    output.style.display = 'inline';
    previewBtn.style.display = 'none';
    copyBtn.style.display = 'none';
    saveBtn.style.display = 'none';
    vsCodeEditorContainer.style.display = 'none';
    try {
        const formData = new URLSearchParams({
            country_code: countryCode,
            payment_method: paymentMethod,
            ai_model: ai_model,
            llm_model: llm_model,
            custom_prompt: customPrompt,
            save_metadata: document.getElementById("save_metadata").checked
        });

        // Only include reindex parameter if Groq Ingest is selected
        if (ai_model === 'groq_ingest') {
            formData.append('re_index', reindex);
        }

        const response = await fetch("/generate-metadata", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            data.metadata = data.metadata || "{}";
            const formattedJson = JSON.stringify(JSON.parse(data.metadata, null, 2), null, 2);
            output.innerHTML = `<pre class="json-output"><code>${formattedJson}</code></pre>`;
            output.style.display = 'none';
            vsCodeEditorContainer.style.display = 'block';
            updateVsCodeViewer(formattedJson);
            previewBtn.style.display = 'inline';
            copyBtn.style.display = 'inline';
            if(formData.get('save_metadata') == 'false') {
                saveBtn.style.display = 'inline';
            }

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

// Add event listener for AI model change to handle reindex visibility
document.getElementById('ai_model').addEventListener('change', function() {
    const reindexContainer = document.getElementById('reindexContainer');
    if (this.value === 'groq_ingest') {
        reindexContainer.classList.remove('d-none');
    } else {
        reindexContainer.classList.add('d-none');
        document.getElementById('reindex').checked = false;
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const aiModelSelect = document.getElementById('ai_model');
    const reindexContainer = document.getElementById('reindexContainer');

    aiModelSelect.addEventListener('change', function() {
        reindexContainer.style.display = this.value === 'groq_ingest' ? 'block' : 'none';
        if (this.value !== 'groq_ingest') {
            document.getElementById('reindex').checked = false;
        }
    });
});

// Add event listener for save button
document.getElementById('saveBtn').addEventListener('click', async function() {
    const output = document.getElementById('output').textContent;
    if (!output || output === 'Please fill out the form and click "Generate Metadata" to see the results here.') {
        alert('No metadata to save!', 'warning');
        return;
    }

    try {
        const countryCode = document.getElementById("country_code").value;
        const paymentMethod = document.getElementById("payment_method").value;
        const response = await fetch('/save-metadata', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                key: countryCode+"_"+paymentMethod,
                metadata: output
            })
        });

        if (response.ok) {
            alert('Metadata saved successfully!', 'success');
        } else {
            throw new Error('Failed to save metadata');
        }
    } catch (error) {
        alert('Error saving metadata: ' + error.message, 'error');
    }
});


require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' }});
require(["vs/editor/editor.main"], function () {
    vsCodeEditor = monaco.editor.create(document.getElementById('vsCodeEditor'), {
        value: "// Please fill out the form and click 'Generate Metadata' to see the results here.",
        language: "json",
        theme: "vs-dark",
        readOnly: false
    }); 
    updateEditorHeight(); // Set initial height 
});

function updateVsCodeViewer(formattedJson) {
    vsCodeEditor.setValue(formattedJson);
    updateEditorHeight(); // Adjust height after setting new content
}
function updateEditorHeight() {
    if (!vsCodeEditor) return;
    const lineCount = vsCodeEditor.getModel().getLineCount();
    const newHeight = Math.min(50 + lineCount * 20, window.innerHeight * 0.8); // Adjust height dynamically

    document.getElementById('vsCodeEditor').style.height = newHeight + "px"; // Update container height
    vsCodeEditor.layout(); // Refresh layout
}
 // Adjust height when content changes
window.addEventListener("resize", updateEditorHeight);

