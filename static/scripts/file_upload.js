const btn = document.getElementById('photo');

const fileChosen = document.getElementById('file-chosen');

const photoPreview = document.getElementById('preview');

btn.addEventListener('change', function(){
    fileChosen.textContent = this.files[0].name
    preview.style.display = 'block'; 
  })
  