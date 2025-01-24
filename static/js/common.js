var toggleButton = document.getElementById('toggleButton');
if (toggleButton) {
    toggleButton.addEventListener('click', function() {
        var form = document.getElementById('formContainer');
        if (form.style.display === 'none') {
            form.style.display = 'block';
        } else {
            form.style.display = 'none';
        }
    });
}


$('#datePicker').change(function() {
    var selectedDate = $(this).val();
    var height = parseFloat($('#height').val()); // Assuming the form has an input with id 'height'
    var weight = parseFloat($('#weight').val()); // Assuming the form has an input with id 'weight'
    var targetBmi = parseFloat($('#target_bmi').val()) || 26.9; // Default to 26.9 if not set

    $.ajax({
        url: '/calculatetarget',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            date: selectedDate,
            height: height,
            weight: weight,
            target_bmi: targetBmi
        }),
        success: function(response) {
            // Update the result div with the HTML from the response
            if (response.html) {
                $("#result").html(response.html);
                $("#minimaldate").empty();
            }

            if (response.htmlminimaldate) {
                $("#minimaldate").html(response.htmlminimaldate);
                $("#result").empty();
            }

            else if (response.error) {
                // Handle error case
                $("#result").html(`<div class='error'>${response.error}</div>`);
                $("#minimaldate").empty();
            }
        }
    });
});