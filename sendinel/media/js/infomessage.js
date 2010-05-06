var AVAILABLE_CHARS = 160;

$(document).ready(function() {    
    
    var textarea = $("#id_text");
    
    $("#chars-left")[0].innerHTML = AVAILABLE_CHARS;
    
    textarea.bind("keydown", function(e) {
        e.stopPropagation();
        
        var offset = (e.keyCode !== 46 && e.keyCode !== 8) ? 1 : 0;
        
        // text_length have to be incremented because current key would be added to length
        var text_length = $(this).val().length + offset;
    
    
        if(text_length > AVAILABLE_CHARS) {
            $(this).val($(this).val().substr(0, AVAILABLE_CHARS));
        }
    });
    
    textarea.bind("keyup", function(e) {
        e.stopPropagation();
        
        var text_length = $(this).val().length;
        
        if(text_length > AVAILABLE_CHARS) {
            $(this).val($(this).val().substr(0, AVAILABLE_CHARS));
            text_length = AVAILABLE_CHARS;
        }
        
        $("#chars-left")[0].innerHTML = AVAILABLE_CHARS - text_length;
    });
});