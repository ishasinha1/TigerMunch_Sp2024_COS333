const btn = document.getElementById('photo');

const fileChosen = document.getElementById('file-chosen');

const photoPreview = document.getElementById('preview');

btn.addEventListener('change', function(){
  console.log('path image', this.files[0].name)
  if (this.files[0].name === "image/heic" || this.files[0].name.toLowerCase().endsWith(".heic")) {
    fileChosen.textContent = this.files[0].name
    console.log('Heic image upload')
 }
 else { 
    fileChosen.textContent = this.files[0].name
    preview.style.display = 'block'; 
 }
  })
  