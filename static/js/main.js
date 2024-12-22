document.addEventListener('DOMContentLoaded', function() {
    const generateForm = document.getElementById('generateForm');
    const outputDiv = document.getElementById('output');
    const copyButton = document.getElementById('copyButton');
    const toast = document.getElementById('toast');
    const useGptToggle = document.getElementById('useGpt');
    const tuningParams = document.getElementById('tuningParams');

    // Load saved GPT toggle state
    const savedGptState = localStorage.getItem('useGpt');
    if (savedGptState !== null) {
        useGptToggle.checked = savedGptState === 'true';
        tuningParams.style.display = useGptToggle.checked ? 'block' : 'none';
    }

    // Show/hide tuning parameters based on GPT toggle
    useGptToggle.addEventListener('change', function() {
        tuningParams.style.display = this.checked ? 'block' : 'none';
        localStorage.setItem('useGpt', this.checked);
    });

    // Update slider labels when values change and save to localStorage
    const sliders = ['playfulness', 'humor', 'emotion', 'poetic', 'metaphorical', 'technical'];
    
    // Load saved tuning parameters
    sliders.forEach(param => {
        const savedValue = localStorage.getItem(`gptTuning_${param}`);
        if (savedValue !== null) {
            const slider = document.getElementById(param);
            slider.value = savedValue;
            const label = slider.previousElementSibling;
            label.textContent = label.textContent.replace(/\(\d+\)/, `(${savedValue})`);
        }
    });

    // Add event listeners for sliders
    sliders.forEach(param => {
        const slider = document.getElementById(param);
        const label = slider.previousElementSibling;
        slider.addEventListener('input', function() {
            const newValue = this.value;
            label.textContent = label.textContent.replace(/\(\d+\)/, `(${newValue})`);
            localStorage.setItem(`gptTuning_${param}`, newValue);
        });
    });

    generateForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const count = document.getElementById('count').value;
        const mode = document.getElementById('mode').value;
        const useGpt = document.getElementById('useGpt').checked;
        
        // Build URL with parameters
        let url = `/generate?count=${count}&mode=${mode}&use_gpt=${useGpt}`;
        
        // Add tuning parameters if GPT is enabled
        if (useGpt) {
            sliders.forEach(param => {
                url += `&${param}=${document.getElementById(param).value}`;
            });
        }
        
        try {
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.error) {
                if (data.fallback_available) {
                    // If fallback is available, show an option to retry without GPT
                    const retry = confirm(data.error + "\n\nWould you like to try again without GPT?");
                    if (retry) {
                        document.getElementById('useGpt').checked = false;
                        tuningParams.style.display = 'none';
                        generateForm.dispatchEvent(new Event('submit'));
                    }
                } else {
                    showToast(data.error);
                }
                return;
            }
            
            // Convert newlines to <br> tags and set as HTML
            outputDiv.innerHTML = data.text.replace(/\n/g, '<br><br>');
            copyButton.style.display = 'block';
        } catch (error) {
            showToast('Failed to generate text. Please try again.');
            console.error('Error:', error);
        }
    });

    copyButton.addEventListener('click', function() {
        const text = outputDiv.textContent;
        navigator.clipboard.writeText(text).then(
            function() {
                showToast('Copied to clipboard!');
            },
            function() {
                showToast('Failed to copy text');
            }
        );
    });

    function showToast(message) {
        toast.textContent = message;
        toast.style.display = 'block';
        setTimeout(() => {
            toast.style.display = 'none';
        }, 3000);
    }

    // Update max count based on mode
    document.getElementById('mode').addEventListener('change', function(e) {
        const countInput = document.getElementById('count');
        switch(e.target.value) {
            case 'paragraph':
                countInput.max = 5;
                break;
            case 'sentence':
                countInput.max = 10;
                break;
            case 'word':
                countInput.max = 50;
                break;
        }
        countInput.value = Math.min(countInput.value, countInput.max);
    });
});
