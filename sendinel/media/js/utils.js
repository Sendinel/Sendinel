if(!Sendinel) { var Sendinel = {}; }

Sendinel.Utils = {
    confirmForm : function(form, title) {
        $("#confirmation").dialog({
            modal: true,
            resizable: false,
            draggable: false,
            title: title,
            buttons: {
                "Cancel" : function() {
                    $(this).dialog("close");
                },
                "OK" : function() {
                    form.submit();
                }
            }
        });
        
        if(!$("#confirmation").dialog("isOpen")) {
            $("#confirmation").dialog("open");
        }
    },
    
    goto_url : function(url) {
        if(url) {
            window.location.assign(url);
        }
    },
};