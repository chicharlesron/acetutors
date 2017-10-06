$(document).ready(function() {
    $('#tutorial_date').datepicker({format: 'yyyy-mm-dd',});
    $('#tutorial_start').timepicker({'timeFormat': 'g:i a', 'scrollDefault': 'now'});
    $('#tutorial_end').timepicker({'timeFormat': 'g:i a', 'scrollDefault': 'now'});
});