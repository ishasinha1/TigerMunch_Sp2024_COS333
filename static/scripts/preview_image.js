// If the user clicks on preview image, the uploaded picture is displayed 
document.addEventListener("DOMContentLoaded", function () {
  var previewButton = document.getElementById("preview");
  var fileInput = document.getElementById("photo");
  var photoPreview = document.getElementById("photo-preview");

  previewButton.addEventListener("click", function (event) {
    event.preventDefault();
    
    // if an image has been uploaded
    if (fileInput.files && fileInput.files[0]) {
      var reader = new FileReader();
      reader.onload = function(e) {
        photoPreview.src = e.target.result;
        photoPreview.style.display = 'block';
        $('#imagePre').modal('show'); 
      };
      reader.readAsDataURL(fileInput.files[0]);
    } else {
      console.log('No preview selected');
    }

  });
});
