var check_for_devices = function() {
    var url = "../get_devices/";
    $.ajax({
        url: url,
        type: "POST",
        success: function(json) {
   
            if(json && json.devices) {
                var deviceTable = $("#bluetooth_devices")[0];
                
                deviceTable.innerHTML = "";
                
                $(json.devices).each(function(index, device) {                
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
                    action.nodeValue = "";
                    var method = document.createAttribute("method");
                    method.nodeValue = "POST";
                    var form_name = document.createAttribute("name");
                    form_name.nodeValue = "form"+index;
                    name_form.setAttributeNode(action);
                    name_form.setAttributeNode(method);
                    name_form.setAttributeNode(form_name);
                    name_form.appendChild(hidden_name);
                    name_form.appendChild(name_link);                    
                    
                    id_td.innerHTML = index+1;
                    name_td.appendChild(name_form);
                    
                    tr.appendChild(id_td);
                    tr.appendChild(name_td);
                    
                    deviceTable.appendChild(tr);
                    
                });
            }
            window.setTimeout("check_for_devices()", 3000);
        }
    });
};

$(document).ready(check_for_devices);