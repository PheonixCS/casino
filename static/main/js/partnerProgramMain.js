$(document).ready(function(){
    $('.colPartnProgramSubmit-text').click(function() {
        showRegistrationForm();
    });
    $('.close').click(function() {
        closeForm();
    });

});
function showRegistrationForm() {
    $('#overlay').addClass('showOverlay');
    $('#registrationForm').addClass('show');
}
function closeForm() {
    $('#overlay').removeClass('showOverlay');
    $('.form').removeClass('show');
}