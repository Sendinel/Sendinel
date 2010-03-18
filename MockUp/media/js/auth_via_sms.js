var input_token = function() {
    $("#content1").html("");
    $("#auth_step_2").html("");
    numpad.convert_forms();
    $("#auth_step_3").show();
    $("#sms_token").focus();
    
};

$(document).ready(function() {
    $("#auth_step_2").hide();
    $("#auth_step_3").hide();
    
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
        $("#content1").hide();
        $("#auth_step_2").show();
        window.setTimeout("this.input_token()", 5000);
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

