// Checks whether neither a photo nor description has been entered.
// If so it shows a warning window, otherwise it clicks the submit button 
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('submitBtn').addEventListener('click', function(event) {
      var fileInput = document.getElementById('photo').value;
      var textInput = document.getElementById('description').value;
      if (!fileInput && !textInput.trim()) {
        event.preventDefault();
        $('#noInput').modal('show');
      } else {
        document.getElementById('submitForm').submit();
      }
    });
});