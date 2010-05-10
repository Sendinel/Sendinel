$(document).ready(function(){
    $("#id_phone_input").keydown(function(event){
        if(event.keyCode === 37){
            var phone_input = $("#id_phone_input");
            var string = phone_input.val();
            string = string.substr(0, (string.length - 1));
            phone_input.val(string);                    
            return false;
        }
    });
});