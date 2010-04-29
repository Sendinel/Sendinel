$(document).ready(function() {
    var AVAILABLE_CHARS = 160;
    
    var textarea = $("#id_text");
    
    textarea.bind("keydown", function(e) {
        e.stopPropagation();
    
        var text_length = $(this).val().length;
    
        if(text_length > AVAILABLE_CHARS) {
            $(this).val($(this).val().substr(0, AVAILABLE_CHARS));
        }
    });
    
    textarea.bind("keyup", function(e) {
        e.stopPropagation();
        
        var text_length = $(this).val().length;
        
        $("#chars-left")[0].innerHTML = "Chars left: " + (AVAILABLE_CHARS - text_length);
    });
});