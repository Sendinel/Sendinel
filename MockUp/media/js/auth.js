$(document).ready(function() {
    $("#auth_step_2").hide();
    
    $("#form_submit").click(function() {
        $("#content1").hide();
        $("#auth_step_2").show();
        
        $(document).keydown(function(e) {
            switch(e.keyCode) {
                case KEY_AUTHENTICATED:
                    window.location = "thank_you.html";
                    break;
                 
                case KEY_ERROR:
                    window.location = "you_fail.html";
                    break;
            }
        });
    });
});

