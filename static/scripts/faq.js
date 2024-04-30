var buttonclick = document.getElementsByClassName("box");
var i;

// when a question is clicked, show the answer and activate the class to 
// display front-end changes
for (i = 0; i < buttonclick.length; i++) {
  buttonclick[i].addEventListener("click", function () {
    this.classList.toggle("active");
    this.parentElement.classList.toggle("active");

    var pannel = this.nextElementSibling;

    if (pannel.style.display === "block") {
      pannel.style.display = "none";
    } else {
      pannel.style.display = "block";
    }
  });
}
