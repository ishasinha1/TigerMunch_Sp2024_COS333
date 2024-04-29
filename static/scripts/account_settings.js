// displaying already entered values from the database to the modal when opened
$(document).ready(function(){
  $('#exampleModal').modal({backdrop: 'static'});
  $('#exampleModal').on('show.bs.modal', function () {
    $.ajax({
      url: "/select",
      method: "POST",
      success: function(data) {
        $('#cal_goal').val((data.calorie_goal >= 0 && data.calorie_goal <= 20000) ? data.calorie_goal : '');
        $('#fat_goal').val((data.fat_goal >= 0 && data.fat_goal <= 2000) ? data.fat_goal : '');
        $('#protein_goal').val((data.protein_goal >= 0 && data.protein_goal <= 2000) ? data.protein_goal : '');
        $('#carb_goal').val((data.carb_goal >= 0 && data.carb_goal <= 2000) ? data.carb_goal : '');
      }
    });
  });
});

// any change in the data is sent to database and the user gets redicted to the home page
// setting bounds on the input values
$('#insert_form').on("submit", function(event){
  event.preventDefault(); 

  let isValid = true; 
  if ($('#cal_goal').val() < 0) {
    alert("Calorie goal should be greater than 0");
    isValid = false;
  }
  if ($('#cal_goal').val() > 20000) {
    alert("Calorie goal should be less than 20,000");
    isValid = false;
  }
  if ($('#fat_goal').val() < 0) {
    alert("Fat goal should be greater than 0");
    isValid = false;
  }
  if ($('#fat_goal').val() > 2000) {
    alert("Fat goal should be less than 2,000");
    isValid = false;
  }
  if ($('#protein_goal').val() < 0) {
    alert("Protein goal should be greater than 0");
    isValid = false;
  }
  if ($('#protein_goal').val() > 2000) {
    alert("Protein goal should be less than 2,000");
    isValid = false;
  }
  if ($('#carb_goal').val() < 0) {
    alert("Carb goal should be greater than 0");
    isValid = false;
  }
  if ($('#carb_goal').val() > 2000) {
    alert("Carb goal should be less than 2,000");
    isValid = false;
  }

  if (isValid) {
    $.ajax({
      url: "/insert",
      method: "POST",
      data: $(this).serialize(),
      beforeSend: function() {
        $("#insert").val("Inserting");
      },
      success: function(data) {
        $("#exampleModal").modal('hide');
        if (data == 'success') {
          window.location.href = "/";
        } else {
          window.location.href = window.location.href; // Reload the page
        }
      }   
    });
  }
});