var toNext = function(){
    var next = $("#next").val();
    window.location.replace(next);
};

var check_for_call = function() {
    var url = $("#ajax_url").val();
    var statusMessage = $("#auth_message");
    
    $.post(url,
        {
            number: $("#number").val()
        },
        function(json) {
   
            if(json && json.status) {
                
                switch(json.status) {                
                    case "waiting":                        
                        $("#auth_spinner_status").text(gettext("Waiting for your call"));
                       
                        window.setTimeout("check_for_call()", 1000);
                    break;
                    
                    case "received":                    
                        toNext();
                    break;
                    
                    case "failed":
                        statusMessage.addClass("error");
                        statusMessage.text(gettext("Sorry, the authentication of your telephone number failed. Please try again."));
                        statusMessage.show();
                        
                        $("#auth_spinner").hide();
                    break;
                }
            }
        },
        "json");        
};

$(document).ready(check_for_call);


