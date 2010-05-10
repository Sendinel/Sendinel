var div_resize = function() {

    var heightContent = window.innerHeight - ($('#header').height() + $('#footer').height());    
    $("#content").height(heightContent);
    
    if($("#contentform").length === 1) {
        // webkit browsers would not resize the element with hight: inherit
        // when it is getting resized via the script.
        // so we have to do it on our own...
        $("#contentform").height(heightContent);
    }
    
    var notificationWidth = window.innerWidth - ($('#sendinel-logo').width() + $('#hpi-logo').width());
    $('#header-notification').width(notificationWidth);
    
    if(Math.max($("#notifications").height(), $("#groups").height()) > heightContent) {
        var backgroundWidth = 12;
        $('#content').css("background-position", ($("#content").width() / 2) + backgroundWidth + "px 0px");
    } else {
        $('#content').css("background-position", "50% 0%");
    }
};

$(window).resize(div_resize); 
$(document).ready(div_resize);
