// Shows the file name once the user uploads a photo.
const btn = document.getElementById('photo');

const fileChosen = document.getElementById('file-chosen');

const photoPreview = document.getElementById('preview');

btn.addEventListener('change', function(){
   // do not show image preview for heic, just show the name of the uploaded image
   if (this.files[0].name === "image/heic" || this.files[0].name.toLowerCase().endsWith(".heic")) {
    fileChosen.textContent = this.files[0].name
   }
   // show the image preview and the name of the uploaded image
   else { 
    fileChosen.textContent = this.files[0].name
    preview.style.display = 'block'; 
   }
})
  