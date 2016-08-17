/**
 * Created by topcoder on 8/16/16.
 */
$(document).ready(function(){
    $('.beef').hover(function() {
        $(this).css("cursor", "pointer");
        $(this).addClass('transition');
    }, function() {
         $(this).removeClass('transition')
    });
});