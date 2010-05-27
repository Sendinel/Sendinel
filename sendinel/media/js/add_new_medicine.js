if(!Sendinel) { var Sendinel = {} }

Sendinel.medicines = {
    create: function() {
        var name = $("#dialog-form input[name=name]").val()
        $.post(medicines_create_url,
                { name: name },
                Sendinel.medicines.handle_create_result,
                "json");
    },
    handle_create_result: function(response) {
        if(response.errors) {
            $("#dialog-form .errorlist").text(response.errors.name.join(", "))
                                        .show();
            return;
        }
        var option = $("<option />")
            .text(response.name + " (0)")
            .val(response.id);
        $("#select-medicine").append(option)
                             .val(response.id);
        $("#dialog-form").dialog("close");
    },
    cleanup_dialog: function () {
        $("#dialog-form .errorlist").hide();
        $("#dialog-form input[name=name]").val("");
    }
}


$(document).ready(function(){
    var buttons = {};
    buttons[gettext('Add Medicine')] = Sendinel.medicines.create;
    buttons[gettext('Cancel')] = function() {
                                    $(this).dialog('close');
                               };

    $("#dialog-form").dialog({
        autoOpen: false,
        height: 300,
        width: 450,
        modal: true,
        buttons: buttons,
        close: Sendinel.medicines.cleanup_dialog
        });
        
    $("#medicines_create_button").click(function() {
            $("#dialog-form").dialog('open');
    });
    $("#dialog-form form").submit( function() {
        Sendinel.medicines.create();
        return false;
    })
});