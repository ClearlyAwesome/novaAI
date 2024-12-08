// unseenScript.js

// Global variable to track submission
var submitted = false;

// Function called when the hidden iframe loads after form submission
function formCallback() {
    if(submitted) {
        // Display the modal
        var modal = document.getElementById('success-modal');
        modal.style.display = 'block';

        // Reset the form after displaying the modal
        document.getElementById('custom-anonymous-form').reset();

        // Clear the selected date/time display (if you have it displayed)
        // var displayElement = document.getElementById('selected-datetime');
        // displayElement.textContent = '';

        submitted = false;
    }
}

// Custom Form Validation
function validateForm() {
    var dateInput = document.getElementById('send-date');
    var timeInput = document.getElementById('send-time');
    var timestampInput = document.getElementById('send-datetime-timestamp');

    if (dateInput.value === '' || timeInput.value === '') {
        alert('Please select a date and time.');
        return false; // Prevent form submission
    }

    var selectedTimestamp = parseInt(timestampInput.value, 10);
    var now = new Date();
    var diffMs = selectedTimestamp - now.getTime();
    var diffMins = diffMs / 60000;
    if (diffMins < 3) {
        alert('The selected date and time must be at least 3 minutes from now.');
        return false; // Prevent form submission
    }

    return true; // Allow form submission
}

// Date/Time Picker Script and Modal functionality
document.addEventListener('DOMContentLoaded', function() {
    // Modal functionality
    var modal = document.getElementById('success-modal');
    var closeModal = document.getElementById('close-modal');

    // When the user clicks on <span> (x), close the modal
    closeModal.onclick = function() {
        modal.style.display = 'none';
    }

    // When the user clicks anywhere outside of the modal content, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }

    // Date/Time Picker Script
    var datetimeInput = document.getElementById('send-datetime');
    var datetimeButton = document.getElementById('datetime-button');
    var displayElement = document.getElementById('selected-datetime');
    var dateInput = document.getElementById('send-date');
    var timeInput = document.getElementById('send-time');
    var timestampInput = document.getElementById('send-datetime-timestamp');

    // Initialize Flatpickr on the hidden input
    var fp = flatpickr(datetimeInput, {
        enableTime: true,
        dateFormat: "m/d/Y at h:i K",
        onClose: function(selectedDates, dateStr, instance) {
            if (selectedDates.length > 0) {
                var selectedDate = selectedDates[0];

                // Get current date/time
                var now = new Date();
                var diffMs = selectedDate - now;
                var diffMins = diffMs / 60000;

                if (diffMins < 3) {
                    alert('Please select a date and time at least 3 minutes into the future.');
                    // Clear the inputs
                    dateInput.value = '';
                    timeInput.value = '';
                    timestampInput.value = '';
                    // Reopen the calendar
                    fp.clear();
                    fp.open();
                    return;
                }

                // Format date and time separately
                var dateOptions = { month: '2-digit', day: '2-digit', year: 'numeric' };
                var timeOptions = { hour: 'numeric', minute: 'numeric', hour12: true };
                var formattedDate = selectedDate.toLocaleDateString('en-US', dateOptions);
                var formattedTime = selectedDate.toLocaleTimeString('en-US', timeOptions);

                // Update hidden inputs
                dateInput.value = formattedDate;
                timeInput.value = formattedTime;
                timestampInput.value = selectedDate.getTime();

                // Display selected date and time (if desired)
                // displayElement.textContent = formattedDate + ' at ' + formattedTime;
            } else {
                // Clear values if no date is selected
                dateInput.value = '';
                timeInput.value = '';
                timestampInput.value = '';
            }
        }
    });

    // Open Flatpickr on button click
    datetimeButton.addEventListener('click', function() {
        fp.open();
    });

    // Form submission handling
    document.getElementById("custom-anonymous-form").addEventListener("submit", function (e) {
        e.preventDefault();

        // Validate the form
        if (!validateForm()) {
            return;
        }

        submitted = true;

        // Collect form data
        const frequency = document.querySelector('input[name="entry.917662412"]:checked').value;
        const recipient = document.getElementById("recipient").value;
        const message = document.getElementById("message").value;
        const senderPhone = document.getElementById("senderPhone").value;
        const email = document.getElementById("email").value;
        const terms = document.getElementById("terms").checked ? "Confirm" : "";

        // Date and Time
        const sendDate = document.getElementById("send-date").value;
        const sendTime = document.getElementById("send-time").value;

        // Create a hidden form to submit to Google Forms
        const googleForm = document.createElement("form");
        googleForm.action =
            "https://docs.google.com/forms/d/e/1FAIpQLSceVjG-bWjYNDjjAvIrSinNRyXdSS4pataVWGW4lT-a8RD7wA/formResponse";
        googleForm.method = "POST";
        googleForm.target = "hidden_iframe";

        // Append hidden inputs with the data
        googleForm.innerHTML = `
            <input type="hidden" name="entry.917662412" value="${frequency}">
            <input type="hidden" name="entry.123456789" value="${sendDate}">
            <input type="hidden" name="entry.987654321" value="${sendTime}">
            <input type="hidden" name="entry.545226767" value="${recipient}">
            <input type="hidden" name="entry.777167988" value="${message}">
            <input type="hidden" name="entry.1890605530" value="${senderPhone}">
            <input type="hidden" name="entry.381221661" value="${email}">
            <input type="hidden" name="entry.912502050" value="${terms}">
        `;

        document.body.appendChild(googleForm);
        googleForm.submit();

        // Remove the temporary form after submission
        document.body.removeChild(googleForm);

        // The formCallback function will handle displaying the modal and resetting the form
        formCallback();
    });
});
// unseenScript.js

document.getElementById("custom-anonymous-form").addEventListener("submit", function (e) {
    e.preventDefault();

    // Collect form data
    const recipient = document.getElementById("recipient").value;
    const message = document.getElementById("message").value;
    const carrier = document.querySelector('input[name="carrier"]:checked').value;

    // Validate carrier
    const carrierGateways = {
        verizon: "vtext.com",
        att: "txt.att.net",
        tmobile: "tmomail.net",
        sprint: "messaging.sprintpcs.com",
    };

    if (!carrierGateways[carrier]) {
        alert("Unsupported carrier.");
        return;
    }

    // Build the recipient's email-to-SMS address
    const smsEmail = `${recipient}@${carrierGateways[carrier]}`;

    // Send the email using SMTP2GO via SMTP.js
    Email.send({
        Host: "mail.smtp2go.com",
        Port: 587,
        Username: "tiktokemail@oegmail.com", // Replace with your SMTP2GO username
        Password: "api-398E997806664D90804C25A5DDD7683E", // Replace with your SMTP2GO API key
        To: smsEmail, // Recipient's email-to-SMS gateway
        From: "tiktokemail@oegmail.com", // Masked sender address
        Subject: "", // Subject is optional for SMS
        Body: message, // The SMS content
    })
        .then((response) => {
            alert("Message sent successfully!");
        })
        .catch((error) => {
            alert("Failed to send message: " + error);
        });
});
