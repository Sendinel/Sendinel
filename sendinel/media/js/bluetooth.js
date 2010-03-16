var Bluetooth = {

    check_for_devices: function() {
        var url = "../get_devices/";
        $.ajax({
            url: url,
            type: "POST",
            success: function(json) {
       
                if(json && json.devices) {
                    var deviceList = $("#bluetooth_devices")[0];
                    
                    deviceList.innerHTML = "";
                    
                    $(json.devices).each(function(index, device) {                
                        var deviceHTML = 
                        "<li>"+
                            "<a href='../appointment/send?device_mac=" + device.mac + "' class='selectable'>" + 
                                device.name + 
                            "</a>"+
                        "</li>";
                        
                        $(deviceList).append($(deviceHTML));                        
                    });
                }
                numpad.convert_forms();
                
                window.setTimeout("Bluetooth.check_for_devices()", 3000);
            },
            error: function() {
                $("#loading").hide();
                var text = gettext("The Bluetooth device doesn't work correctly. Please inform the clerk.");
                var element = '<tr><td>' + text + '</td></tr>'
                
                var deviceTable = $("#bluetooth_devices");
                deviceTable.empty();
                deviceTable.append(element);
                $("#spinner").hide();
            }
        });
    },
    
    redirect_to_next: function() {
        window.location = $("#next").val();
    },
    
    send_file: function() {
        var url = $("#url").val();
        
        $.ajax({
            url: url,
            type: "POST",
            data: {
                device_mac: $("#device_mac").val()
            },
            success: Bluetooth.redirect_to_next,
            error: function() {
                $("#spinner")[0].innerHTML = gettext("Failed to send appointment");
                window.setTimeout("Bluetooth.redirect_to_next()", 20000);
            }
        });
    }
};