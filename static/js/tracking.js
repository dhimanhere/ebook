document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.download-btn').forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            
            const ebookId = this.dataset.ebookId;
            
            console.log('Clicked download for ebook:', ebookId); // Debug log
            
            if (!ebookId) {
                console.error('Missing data attributes:', { ebookId, fileUrl });
                return;
            }
            
            const formData = new FormData();
            formData.append('ebook_id', ebookId);
            
            try {
                const response = await fetch('/track-download/', {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: formData
                });
                
                console.log('Response status:', response.status); // Debug log
                
                const contentType = response.headers.get('content-type');
                if (!contentType || !contentType.includes('application/json')) {
                    throw new TypeError("Response was not JSON");
                }
                
                const data = await response.json();
                console.log('Response data:', data); // Debug log
                
                if (response.ok && data.status === 'success') {
                    // Update download count display
                    const countDisplay = document.getElementById(`download-count-${ebookId}`);
                    if (countDisplay) {
                        countDisplay.textContent = `Downloads: ${data.count}`;
                    }
                } else {
                    throw new Error(data.message || 'Server error occurred');
                }
            } catch (error) {
                console.error('Error details:', error);
                alert(`Download error: ${error.message}`);
            }
        });
    });
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
