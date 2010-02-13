var check_for_call = function() {
    var url = "/web/call_handler/";
    
    new Ajax.Request(url, {
        method: 'post',
        parameters: {
            number: $("phonenumber").value
        },
        onSuccess: function(response) {
            var json = (response.responseText || "").evalJSON();   
            if(json && json.status) {
                var statusText = $("auth_status");
                
                switch(json.status) {                
                    case "waiting":                        
                        statusText.innerHTML = "Waiting for your call";
                        window.setTimeout("check_for_call()",1000);
                    break;
                    
                    case "received":                        
                        statusText.innerHTML = "Thank you! Your telephone number has been authenticated.";
                        $("auth_spinner").hide();
                    break;
                    
                    case "failed":
                        statusText.innerHTML = "Sorry, the authentication of your telephone number failed. Please try again.";
                        $("auth_spinner").hide();
                                                
                    break;
                }
            }             
        },
        onFailure: function() {
            
        }
    });
};

window.setTimeout("check_for_call()", 1000);
