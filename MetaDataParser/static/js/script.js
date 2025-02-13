document.getElementById("metadata-form").addEventListener("submit", async function(e) {
    e.preventDefault();
    const countryCode = document.getElementById("country_code").value;
    const paymentMethod = document.getElementById("payment_method").value;
    const ai_model = document.getElementById("ai_model").value;
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
            body: `country_code=${encodeURIComponent(countryCode)}&payment_method=${encodeURIComponent(paymentMethod)}&ai_model=${encodeURIComponent(ai_model)}`
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