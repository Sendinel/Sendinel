$(document).ready(function() {
    $("#auth_step_2_1").hide();
    $("#auth_step_2_2").hide();
    $("#auth_step_2_3").hide();
        
    $(document).keydown(function(e) {
        switch(e.keyCode) {
            case KEY_AUTHENTICATED:
                $("#content1").hide();
                $("#auth_step_2_2").hide();
                $("#auth_step_2_3").hide();
                $("#auth_step_2_1").show();
                break;
             
            case KEY_ERROR:
                $("#content1").hide();
                $("#auth_step_2_1").hide();
                $("#auth_step_2_3").hide();                
                $("#auth_step_2_2").show();
                break;
            
            case KEY_ALTERNATIVE:
                $("#content1").hide();
                $("#auth_step_2_1").hide();
                $("#auth_step_2_2").hide();
                $("#auth_step_2_3").show();
                break;
        }
    });
});

