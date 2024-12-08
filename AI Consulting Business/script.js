document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("contact-form");

    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Prevent the form from refreshing the page

        // Collect form data
        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const message = document.getElementById("message").value;

        // Send data to Google Sheets using the Web App URL
        fetch("https://script.google.com/macros/s/AKfycbwPtDEPpd1nbRsNTmPdCAmVsWdDPgS1RS0a0TC09vzx5Msq0SWq69bPguCACo__3SPAkg/exec", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name: name, email: email, message: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                alert("Thank you! Your message has been sent.");
                form.reset(); // Clear the form
            } else {
                alert("There was an issue submitting your message. Please try again.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("There was an error with your submission.");
        });
    });
});

const faqItems = Array.from(document.querySelectorAll('.cs-faq-item'));
        for (const item of faqItems) {
            const onClick = () => {
            item.classList.toggle('active')
        }
        item.addEventListener('click', onClick)
        }
                                