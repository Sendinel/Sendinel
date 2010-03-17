var check_for_call = function() {
    var url = $("#ajax_url").val();
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
                        statusText.text(gettext("Thank you! Your telephone number has been authenticated."));
                        var next = $("#next").val();
                        window.location.replace(next);
                    break;
                    
                    case "failed":
                        statusText.text(gettext("Sorry, the authentication of your telephone number failed. Please try again."));
                        $("#auth_spinner").hide();
                                                
                    break;
                }
            }
        },
        "json");
   
        
};

$(document).ready(check_for_call);


