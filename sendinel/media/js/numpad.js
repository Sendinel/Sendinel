var numpad = {

    selectables: new Array(),
    selected: 0,

    getSelected: function() {
        return $(numpad.selectables[numpad.selected]);
    },

    handleKeydown: function(event) {
        switch(event.keyCode) {
            case 13: // Enter
                numpad.clickOnSelected();
                break;
            case 38: // Arrow up
                numpad.selectPrevious();
                break;
            case 39: //Arrow right
                numpad.clickOnSelected();
                break;
            case 40: // Arrow down
                numpad.selectNext();
                break;
        }
    },
    
    clickOnSelected: function() {
        console.log(numpad.getSelected());    
        var el = numpad.getSelected()[0];
        if(el.tagName.toLowerCase() == "a") {
            window.location = el.href;
        } else {
            numpad.getSelected().trigger('click');
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
        numpad.getSelected().removeClass("selected");
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