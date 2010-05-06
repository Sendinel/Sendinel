var div_resize = function() {

    var heightContent = window.innerHeight - ($('#header').height() + $('#footer').height());    
    $("#content").height(heightContent);
    
    if($("#notifications").height() > heightContent) {
        var backgroundWidth = 10;
        $('#content').css("background-position", ($("#content").width() / 2) + backgroundWidth + "px 0px");
    } else {
        $('#content').css("background-position", "50% 0%");
    }
};

$(window).resize(div_resize); 
$(document).ready(div_resize);
