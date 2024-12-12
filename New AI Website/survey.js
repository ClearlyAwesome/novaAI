document.getElementById('survey-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    
    // Gather form data
    const formData = new FormData(event.target);

    // Send data to the server
    fetch('/save-survey', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            // Show the modal on successful submission
            document.getElementById('completion-modal').style.display = 'block';
        } else {
            alert('There was an error submitting your survey. Please try again.');
        }
    })
    .catch(() => {
        alert('There was an error submitting your survey. Please check your connection and try again.');
    });
});
