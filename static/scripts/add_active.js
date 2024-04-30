// Highlights the current page in the header.
var curr_path = window.location.pathname;
curr_path = curr_path.substring(1);
elem = document.getElementById(curr_path);
elem.classList.add('active');