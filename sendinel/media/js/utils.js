if(!Sendinel) { var Sendinel = {}; }

Sendinel.Utils = {
    confirmForm : function(form, title) {
        $("#confirmation").dialog({
            modal: true,
            resizable: false,
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
    }
};