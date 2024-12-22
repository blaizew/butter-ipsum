document.addEventListener('DOMContentLoaded', function() {
    const generateForm = document.getElementById('generateForm');
    const outputDiv = document.getElementById('output');
    const copyButton = document.getElementById('copyButton');
    const toast = document.getElementById('toast');

    generateForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const count = document.getElementById('count').value;
        const mode = document.getElementById('mode').value;
        
        try {
            const response = await fetch(`/generate?count=${count}&mode=${mode}`);
            const data = await response.json();
            
            if (data.error) {
                showToast(data.error);
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
