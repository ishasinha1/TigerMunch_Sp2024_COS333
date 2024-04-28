// if a user has not set any goals, this script navigates the user 
// to the account setting modal after clicking on the frontend arrow
$(document).ready(function(){
    $("#showFeaturesBtn").click(function(){
        // Programmatically toggle the navbar dropdown
        var dropdownMenu = new bootstrap.Dropdown(document.getElementById('navbarDropdownMenuLink'));
        dropdownMenu.toggle();

        // Show the modal
        var exampleModal = new bootstrap.Modal(document.getElementById('exampleModal'), {
            keyboard: false,
            backdrop: 'static'
        });
        exampleModal.show();
    });
});