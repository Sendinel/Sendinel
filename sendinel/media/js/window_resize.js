var div_resize = function() {
    // content1 - (#rightbar + body.margin)
        
    $("#content1").width($(window).width() - 
        ($("#rightbar").outerWidth() + 
         ((parseInt($("body").css("margin-left"), 10) * 4) + 
          (parseInt($("#content1").css("padding-left"), 10))
         )
      )
     );
};

$(window).resize(div_resize)
         .ready(div_resize); 