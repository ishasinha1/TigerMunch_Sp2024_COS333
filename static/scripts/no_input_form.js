document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('submitBtn').addEventListener('click', function(event) {
      var fileInput = document.getElementById('photo').value;
      var textInput = document.getElementById('description').value;
      console.log('File Input:', fileInput); // Debugging output
      console.log('Text Input:', textInput); // Debugging output
      if (!fileInput && !textInput.trim()) {
        event.preventDefault();
        $('#noInput').modal('show');
      } else {
        document.getElementById('submitForm').submit();
      }
    });
  });