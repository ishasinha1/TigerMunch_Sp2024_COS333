// Handles the input submitted to the contact us form.

document.addEventListener("DOMContentLoaded", function () {
    const contactForm = document.getElementById("contactForm");
    const responseMessage = document.getElementById("responseMessage");

    contactForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;

        const formData = {
            name: name,
            email: email,
            message: message,
        };

        const apiEndpoint =  "/contact_us";
        
        // send the feedback to the back-end
        fetch(apiEndpoint, {
            method: "POST",
            headers: {
                'Content-Type':
                    'application/json;charset=utf-8'
            },
            body: JSON.stringify(formData)
        })
        // if response is successful, show a success message for a few seconds 
        .then(response => response.json())
        .then(data => {
            responseMessage.innerHTML = `<p>${data.message}</p>`;
            responseMessage.classList.add("success", "show"); 

            setTimeout(() => {
                contactForm.reset();
                responseMessage.innerHTML = "";
                responseMessage.classList.remove("success", "show");
            }, 2000);
        })
        // if the response is not successful, show a failed message for a few seconds
        .catch(error => {
            console.error("Error:", error);
            responseMessage.innerHTML = `<p>Error submitting the form. Please try again later.</p>`;
            responseMessage.classList.add("error", "show"); 

            setTimeout(() => {
                responseMessage.innerHTML = "";
                responseMessage.classList.remove("error", "show");
            }, 3000);
        });
    });
});