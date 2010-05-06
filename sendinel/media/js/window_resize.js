var div_resize = function() {

    var heightContent = window.innerHeight - ($('#header').height() + $('#footer').height());    
    $("#content").height(heightContent);
    
    if($("#notifications").height() > heightContent) {
        var backgroundWidth = 10;
        $('#main-menu').css("background-position", ($("#main-menu").width() / 2) + backgroundWidth + "px 0px");
    } else {
        $('#main-menu').css("background-position", "50% 0%");
    }
};

$(window).resize(div_resize); 
$(document).ready(div_resize);
