var Bluetooth = {

    check_for_devices: function() {
        var url = "../get_devices/";
        $.ajax({
            url: url,
            type: "POST",
            success: function(json) {
       
                if(json && json.devices) {
                    var deviceTable = $("#bluetooth_devices")[0];
                    
                    deviceTable.innerHTML = "";
                    
                    $(json.devices).each(function(index, device) {                
                        var html = ""
                        
                        var tr = document.createElement("tr");
                        var id_td = document.createElement("td");
                        var name_td = document.createElement("td");
                        
                        var hidden_name = document.createElement("input");
                        var type = document.createAttribute("type");
                        type.nodeValue = "hidden";
                        var value = document.createAttribute("value");
                        value.nodeValue = device.mac;
                        var name = document.createAttribute("name");
                        name.nodeValue = "device_mac";
                        hidden_name.setAttributeNode(type);
                        hidden_name.setAttributeNode(value);
                        hidden_name.setAttributeNode(name);
                        
                        var name_link = document.createElement("a");
                        
                        var onClick_link = document.createAttribute("href");
                        onClick_link.nodeValue = "javascript:document.form"+index+".submit()";
                        name_link.setAttributeNode(onClick_link);
                        name_link.innerHTML = device.name;
                        
                        var name_form = document.createElement("form");
                        var action = document.createAttribute("action");
                        action.nodeValue = $("#next").attr("value");                   
                        var method = document.createAttribute("method");
                        method.nodeValue = "GET";
                        
                        var form_name = document.createAttribute("name");
                        form_name.nodeValue = "form"+index;
                        name_form.setAttributeNode(action);
                        name_form.setAttributeNode(method);
                        name_form.setAttributeNode(form_name);
                        name_form.appendChild(hidden_name);
                        name_form.appendChild(name_link);
                        var csrf = $("#csrf input").clone(); 
                        csrf.appendTo(name_form);
                        
                        id_td.innerHTML = index+1;
                        name_td.appendChild(name_form);
                        
                        tr.appendChild(id_td);
                        tr.appendChild(name_td);
                        
                        deviceTable.appendChild(tr);
                        
                    });
                }
                window.setTimeout("Bluetooth.check_for_devices()", 3000);
            },
            error: function() {
                $("#loading").hide();
            
                var deviceTable = $("#bluetooth_devices")[0];
                    
                deviceTable.innerHTML = "";
            
                var tr = document.createElement("tr");
                var td = document.createElement("td");
                
                td.innerHTML = "The Bluetooth device doesn't work correctly. ";
                td.innerHTML += "Please inform the clerk.";

                tr.appendChild(td);
                deviceTable.appendChild(tr);
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
            success: Bluetooth.redirect_to_next(),
            error: function() {
                $("#spinner")[0].innerHTML = "Failed to send appointment";
                window.setTimeout("Bluetooth.redirect_to_next()", 20000);
            }
        });
    }
};