var check_for_call = function() {
    var url = "/call_handler";
    
    new Ajax.Request(url, {
        method: 'post',
        parameters: {
            number: $("phonenumber").value
        },
        onSuccess: function(response) {
            var json = (response.responseText || "").toJSON();   
            
            if(json && json.status) {
                switch(json.status) {
                    case "waiting":
                    break;
                    
                    case "received":
                        var statusText = $("auth_spinner");
                        statusText.innerHTML = "";
                        
                        window.clearInterval(checker);
                    break;
                    
                    case "failes":
                    break;
                }
            }             
        },
        onFailure: function() {
            
        }
    });
};

var checker = window.setInterval("check_for_call()", 5000);
