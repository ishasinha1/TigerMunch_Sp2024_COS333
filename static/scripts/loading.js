// Shows the loading overlay when the user submits the form.
document.addEventListener('DOMContentLoaded', function() {
    window.onpageshow = function(event) {
       if (event.persisted) {
        window.location.reload();
      }
    };
    document.getElementById('submitForm').addEventListener('submit', function() {
      document.getElementById('loadingOverlay').style.display = 'flex'; // Show the overlay
      document.querySelector('#content').style.filter = 'blur(5px)'; // Blur the background content
    });
});