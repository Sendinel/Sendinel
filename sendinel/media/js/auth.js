var check_for_call = function() {
    var url = "../check_call_received/";
    $.post(url,
        {
            number: $("#number").val()
        },
        function(json) {
   
            if(json && json.status) {
                var statusText = $("#auth_status");
                
                switch(json.status) {                
                    case "waiting":                        
                        statusText.text("Waiting for your call");
                        window.setTimeout("check_for_call()",1000);
                    break;
                    
                    case "received":                        
                        statusText.text("Thank you! Your telephone number has been authenticated.");
                        $("#next").show();
                        $("#auth_spinner").hide();
                    break;
                    
                    case "failed":
                        statusText.text("Sorry, the authentication of your telephone number failed. Please try again.");
                        $("#next").hide();
                        $("#auth_spinner").hide();
                                                
                    break;
                }
            }
        },
        "json");
};
$(#next).hide();
$(document).ready(check_for_call);



