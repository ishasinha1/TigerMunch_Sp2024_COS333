const btn = document.getElementById('photo');

const fileChosen = document.getElementById('file-chosen');

const photoPreview = document.getElementById('photo-preview');
  
  btn.addEventListener('change', function() {
    if (this.files && this.files[0]) {
      fileChosen.textContent = this.files[0].name;
      const reader = new FileReader();
      reader.onload = function(e) {
        photoPreview.src = e.target.result;
        fileChosen.style.display = 'none'
        photoPreview.style.display = 'block'; 
      };
      reader.readAsDataURL(this.files[0]); 
    } else {
      fileChosen.textContent = 'No file chosen';
      photoPreview.style.display = 'none'; 
    }
  });
  