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
                            "<a href='/notifications/appointment/send?device_mac=" + device.mac + "' class='selectable'>" + 
                                device.name + 
                            "</a>"+
                        "</li>";
                        
                        $(deviceList).append($(deviceHTML));                        
                    });
                }
                
                window.setTimeout("Bluetooth.check_for_devices()", 3000);
            },
            error: function() {
                $("#loading").hide();
                var text = gettext("The Bluetooth device doesn't work correctly. Please inform the clerk.");
                var element = '<tr><td class="errorlist rounded-corners">' + text + '</td></tr>'
                
                var deviceTable = $("#bluetooth_devices");
                deviceTable.empty();
                deviceTable.append(element);
                $("#spinner").hide();
            }
        });
    },
    
    redirect_to_next: function() {
        Sendinel.Utils.goto_url($("#next").val());
    },
    
    send_file: function() {
        var url = $("#url").val();
        var nextButton = $(".button-right")
        nextButton.hide();
        $.ajax({
            url: url,
            type: "POST",
            data: {
                device_mac: $("#device_mac").val()
            },
            success: function() {
                
                var statusText = $("#status");
                
                $("#auth_spinner").hide();
                var next = $("#next").val();
                statusText.addClass("status success rounded-corners centered");
                statusText.text(gettext("Thank you! The appointment has been send to your mobile phone."));   
                
                nextButton.show();
                
    
                window.setTimeout("Bluetooth.redirect_to_next()", 10000);
            },
            error: function() {
                var stat = $("#spinner");
                
                stat[0].innerHTML = gettext("Failed to send appointment");
                stat.addClass("errorlist");
                
                window.setTimeout("Bluetooth.redirect_to_next()", 20000);
            }
        });
    }
};