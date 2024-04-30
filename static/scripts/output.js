// After displaying the results from the entered info for adding a meal. 
// The following ensures that the user cannot enter negative/extremely
// large values for security reasons.

$('#save_form').on("submit", function(event){
    event.preventDefault(); 

    let isValid = true; 
    if ($('#cal').val() < 0 ) {
        alert("Calories should be a nonnegative integer");
        isValid = false;
    }
    if ($('#cal').val() > 20000 ) {
        alert("Calories should be less than 20,000");
        isValid = false;
    }
    if ($('#fat').val() < 0) {
        alert("Fat should be a nonnegative integer");
        isValid = false;
    }
    if ($('#fat').val() > 2000) {
        alert("Fat should be less than 2,000");
        isValid = false;
    }
    if ($('#protein').val() < 0) {
        alert("Protein should be a nonnegative integer");
        isValid = false;
    }
    if ($('#protein').val() > 2000) {
        alert("Protein should be less than 2,000");
        isValid = false;
    }
    if ($('#carbs').val() < 0) {
        alert("Carbs should be a nonnegative integer");
        isValid = false;
    }
    if ($('#carbs').val() > 2000) {
        alert("Carbs should be less than 2,000");
        isValid = false;
    }

    // If all entries are valid, they are sent to the backend.
    if (isValid) {
    $.ajax({
        url: "/save_results",
        method: "POST",
        data: $(this).serialize(),
        success: function(data) {
            console.log(data); 
            if (data.status === 'success') {
                window.location.href = "/home";
            } else {
                alert('Failed to save results.');
            }
        },
        error: function() {
            alert('An error occurred during the request.');
        }});
    }
});