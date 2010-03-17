$(document).ready(function() {
    $("#auth_step_2").hide();
    
    var submit_code = function() {
        if ( $("#sms_token").val() === SMS_TOKEN ){
            window.location = "thank_you.html";
        }
        else {
            $("#error").html("The Code you entered is invalid. Please try again.");
            $("#error").show();
            numpad.convert_forms();
        }
    };
    
    $("#form_submit").click( function() {
        $("#content1").html("");
        numpad.convert_forms();
        $("#auth_step_2").show();
        $("#sms_token").focus();
        
    });
    
    $("#sms_token").keydown(function(e) {
        if (e.keyCode === 13){
            submit_code();
        }
    });
    
    $("#code_submit").keydown(function(e) {
        if (e.keyCode === 13){
            submit_code();
        }
    });
    
    $("#code_submit").click( submit_code );   
    
});

