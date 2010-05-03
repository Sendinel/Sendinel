$(document).ready(function() {
    var AVAILABLE_CHARS = 160;
    
    var textarea = $("#id_text");
    
    textarea.bind("keydown", function(e) {
        e.stopPropagation();
        
        // text_length have to be incremented because current key would be added to length
        var text_length = $(this).val().length + 1;
    
    
        if(text_length > AVAILABLE_CHARS) {
            $(this).val($(this).val().substr(0, AVAILABLE_CHARS - 1));
        }
    });
    
    textarea.bind("keyup", function(e) {
        e.stopPropagation();
        
        var text_length = $(this).val().length;
        
        $("#chars-left")[0].innerHTML = "Chars left: " + (AVAILABLE_CHARS - text_length);
    });
});