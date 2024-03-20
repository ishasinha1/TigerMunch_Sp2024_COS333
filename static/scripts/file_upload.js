const btn = document.getElementById('photo');

const fileChosen = document.getElementById('file-chosen');

btn.addEventListener('change', function(){
    fileChosen.textContent = this.files[0].name
  })