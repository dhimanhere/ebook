function getCSRFToken() {
  const name = 'csrftoken=';
  const decodedCookie = decodeURIComponent(document.cookie);
  const cookieArray = decodedCookie.split(';');
  for(let i = 0; i < cookieArray.length; i++) {
    let cookie = cookieArray[i].trim();
    if (cookie.indexOf(name) === 0) {
      return cookie.substring(name.length, cookie.length);
    }
  }
  return null;
}

// Reset upload status
function resetUploadStatus() {
  const uploadStatus = document.querySelector('.upload-status');
  const progressBar = document.querySelector('.progress-bar');
  const progressText = document.querySelector('.progress-text');
  const fileUploadStatus = document.querySelector('.file-upload-status');
  
  uploadStatus.style.display = 'none';
  progressBar.style.width = '0%';
  progressBar.style.backgroundColor = '#4CAF50';
  progressText.textContent = '0%';
  fileUploadStatus.textContent = 'Uploading eBook file...';
}

// Listen for file selection on the book input
document.querySelector('#id_book').addEventListener('change', function(e) {
  const file = e.target.files[0];
  if (file) {
        // You can add file validation here if needed
        const fileSize = (file.size / 1024 / 1024).toFixed(2); // Convert to MB
        document.querySelector('.file-upload-status').textContent = 
        `Selected: ${file.name} (${fileSize} MB)`;
      }
    });

// Main form submission handler
document.querySelector('.ebk-form').addEventListener('submit', function(e) {
  e.preventDefault();
  
  const form = e.target;
  const formData = new FormData(form);
  const uploadStatus = document.querySelector('.upload-status');
  const progressBar = document.querySelector('.progress-bar');
  const progressText = document.querySelector('.progress-text');
  const fileUploadStatus = document.querySelector('.file-upload-status');
  const submitButton = form.querySelector('button[type="submit"]');
  
    // Check if there's an ebook file to upload
  const bookFile = formData.get('book');
  const hasBookFile = bookFile && bookFile.name !== '';
  
  if (hasBookFile) {
    uploadStatus.style.display = 'block';
    fileUploadStatus.textContent = 'Uploading eBook file...';
  }
  
    // Disable submit button and update text
  submitButton.disabled = true;
  submitButton.textContent = 'Uploading...';
  
  const xhr = new XMLHttpRequest();
  
    // Upload progress handler - only show for book file
  xhr.upload.addEventListener('progress', function(event) {
    if (hasBookFile && event.lengthComputable) {
      const percentComplete = (event.loaded / event.total) * 100;
      progressBar.style.width = percentComplete + '%';
      progressText.textContent = Math.round(percentComplete) + '%';
    }
  });
  
    // Request completed handler
  xhr.addEventListener('load', function() {
    submitButton.disabled = false;
    
    if (xhr.status === 200) {
      const response = JSON.parse(xhr.responseText);
      
      if (response.success) {
                // Success handling
        if (hasBookFile) {
          progressBar.style.backgroundColor = '#4CAF50';
          fileUploadStatus.textContent = 'eBook Upload Complete!';
          fileUploadStatus.style.color = '#4CAF50';
        }
        submitButton.textContent = 'Published Successfully!';
        
                // Reset form and status after delay
        setTimeout(() => {
          form.reset();
          resetUploadStatus();
          submitButton.textContent = 'Publish eBook';
        }, 2000);
      } else {
                // Error handling
        if (hasBookFile) {
          progressBar.style.backgroundColor = '#f44336';
          fileUploadStatus.textContent = 'Upload Failed';
          fileUploadStatus.style.color = '#f44336';
        }
        submitButton.textContent = 'Publish eBook';
        
                // Display form errors
        if (response.errors) {
          Object.entries(response.errors).forEach(([field, errors]) => {
            const inputElement = form.querySelector(`#id_${field}`);
            if (inputElement) {
                            // Create or update error message
              let errorDiv = inputElement.nextElementSibling;
              if (!errorDiv || !errorDiv.classList.contains('error-message')) {
                errorDiv = document.createElement('div');
                errorDiv.classList.add('error-message');
                inputElement.parentNode.insertBefore(errorDiv, inputElement.nextSibling);
              }
              errorDiv.textContent = errors.join(', ');
            }
          });
        }
      }
    } else {
            // Server error handling
      if (hasBookFile) {
        progressBar.style.backgroundColor = '#f44336';
        fileUploadStatus.textContent = 'Server Error';
        fileUploadStatus.style.color = '#f44336';
      }
      submitButton.textContent = 'Publish eBook';
    }
  });
  
    // Network error handler
  xhr.addEventListener('error', function() {
    if (hasBookFile) {
      progressBar.style.backgroundColor = '#f44336';
      fileUploadStatus.textContent = 'Network Error';
      fileUploadStatus.style.color = '#f44336';
    }
    submitButton.disabled = false;
    submitButton.textContent = 'Publish eBook';
  });
  
    // Send the request
  xhr.open('POST', form.action || window.location.href);
  xhr.setRequestHeader('X-CSRFToken', getCSRFToken());
  xhr.send(formData);
});

// Clear error messages when user starts typing
document.querySelectorAll('.ebk-form input, .ebk-form textarea, .ebk-form select').forEach(input => {
  input.addEventListener('input', function() {
    const errorDiv = this.nextElementSibling;
    if (errorDiv && errorDiv.classList.contains('error-message')) {
      errorDiv.remove();
    }
  });
});
