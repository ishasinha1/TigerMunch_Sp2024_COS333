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