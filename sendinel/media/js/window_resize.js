var div_resize = function() {

    var heightContent = window.innerHeight - ($('#header').height() + $('#footer').height());
    var heightNotification = heightContent-(parseInt($('#notifications').css('padding-top'))*2);
    
    if($('#notifications').height()<heightContent){
        $('#notifications').height(heightNotification);
    }
    $('#content').height(heightContent);
    
    //Setting the width of the main menu
    var scrollbarOffset = 15;
    var widthContent = window.innerWidth / 2;   
    var notificationOffset = parseInt($('#notifications').css('padding-left'))+parseInt($('#notifications').css('padding-right'));
    var groupsOffset =  parseInt($('#groups').css('padding-left')) +parseInt($('#groups').css('padding-right'));
    var borderOffset = parseInt($('#notifications').css('borderRightWidth'));
    
    var widthNotification = widthContent - (scrollbarOffset + notificationOffset + borderOffset )
    var widthGroups = widthContent - (scrollbarOffset + groupsOffset +borderOffset )
    
    $('#notifications').width(widthNotification);
    $('#groups').width(widthContent-50);
};

$(window).resize(div_resize); 

$(document).ready(div_resize);
