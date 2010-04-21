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
                
                window.setTimeout("Bluetooth.check_for_devices()", 3000);
            },
            error: function() {
                $("#loading").hide();
                var text = gettext("The Bluetooth device doesn't work correctly. Please inform the clerk.");
                var element = '<tr><td class="errorlist">' + text + '</td></tr>'
                
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
            success: function() {
                
                var statusText = $("#status");
                
                $("#auth_spinner").hide();
                var next = $("#next").val();
                statusText.addClass("success");
                statusText.text(gettext("Thank you! The appointment has been send to your mobile phone."));   
            
                var next = $("#next").val();
                var next_button = $("<div class='next-button'>" +
                            "<input type='submit' id='id_next' value='Next -&gt;' name='form_submit' class='subselectable' />" +
                            '<input type="hidden" value="' + next +'" name="next-button-link" /></div>');
                $("#control_buttons").append(next_button);
    
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