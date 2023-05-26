$(document).ready(function() {
    $('.learn-more-link').click(function(e) {
        e.preventDefault(); // prevent the default action
        $('html, body').animate({
            scrollTop: $($(this).attr('href')).offset().top
        }, 'slow');
    });
});