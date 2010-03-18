var toNext = function(){
    var next = $("#next").val();
    window.location.replace(next);
};

var check_for_call = function() {
    var url = $("#ajax_url").val();
    $("#id_next").hide();
    $.post(url,
        {
            number: $("#number").val()
        },
        function(json) {
   
            if(json && json.status) {
                var statusText = $("#auth_status");
                
                switch(json.status) {                
                    case "waiting":                        
                        statusText.text(gettext("Waiting for your call"));
                        window.setTimeout("check_for_call()",1000);
                    break;
                    
                    case "received":
                    
                        $("#auth_spinner").hide();
                        var next = $("#next").val();
                        statusText.addClass("success");
                        statusText.text(gettext("Thank you! Your telephone number has been authenticated."));                        
                        var next_button = $("<div class='next-button'>" +
                            "<input type='submit' id='id_next' value='Next -&gt;' name='form_submit' class='subselectable' />" +
                            '<input type="hidden" value="' + next +'" name="next-button-link" /></div>');
                        $("#control_buttons").append(next_button);
                        numpad.convert_forms();
                        //window.setTimeout("toNext()", 10000);
                    break;
                    
                    case "failed":
                        statusText.addClass("errorlist");
                        statusText.text(gettext("Sorry, the authentication of your telephone number failed. Please try again."));
                        $("#auth_spinner").hide();
                                                
                    break;
                }
            }
        },
        "json");
        
};

$(document).ready(check_for_call);


