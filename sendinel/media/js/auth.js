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
                switch(json.status) {
                    case "waiting":
                        var statusText = $("auth_status");
                        statusText.innerHTML = "Waiting for your call";
                    break;
                    
                    case "received":
                        var statusText = $("auth_status");
                        statusText.innerHTML = "Thank you! Your telephone number has been authenticated.";
                        $("auth_spinner").hide();
                        window.clearInterval(checker);
                    break;
                    
                    case "failed":
                        var statusText = $("auth_status");
                        statusText.innerHTML = "Sorry, the authentication of your telephone number failed. Please try again.";
                        $("auth_spinner").hide();
                        window.clearInterval(checker);
                        
                    break;
                }
            }             
        },
        onFailure: function() {
            
        }
    });
};

var checker = window.setInterval("check_for_call()", 1000);
