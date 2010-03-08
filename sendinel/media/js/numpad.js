var numpad = {

    selectables: new Array(),
    selected: 0,


    handleKeydown: function(event) {
        switch(event.keyCode) {
            case 38:
                numpad.selectPrevious();
                break;
            case 40:
                numpad.selectNext();
                break;
        }
    },
    
    selectNext: function() {
        return numpad.select(numpad.selected + 1);
    },
    
    selectPrevious: function() {
        return numpad.select(numpad.selected - 1);
    },
    
    select: function(number) {
        if(number < 0 || number >= numpad.selectables.length) {
            return false;
        }
        $(numpad.selectables[numpad.selected]).removeClass("selected");
        $(numpad.selectables[number]).addClass("selected");
        numpad.selected = number;
        return true;
    },
};

$(document).ready(function() {
    $(window).keydown(numpad.handleKeydown);
    numpad.selectables = $(".selectable");
    numpad.select(0);
});