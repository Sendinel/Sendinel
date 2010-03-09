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
            default:
                return true;
        }
        // stop event propagation
        return false;
    },
    
    clickOnSelected: function() {
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
        var oldItem = numpad.getSelected();
        if(oldItem[0].handleDeselected) {
           oldItem[0].handleDeselected();
        }
        oldItem.removeClass("selected");
        
        numpad.selected = number;
        
        var item = numpad.getSelected();
        item.addClass("selected")
        
        if(item[0].handleSelected) {
           item[0].handleSelected();
        } else {
            item.focus();
        }
        return true;
    },
    
    
    convert_forms: function() {
        numpad.inputs.datetime.convert();
        // numpad.conversions.convertDatetimes();
        numpad.inputs.convertSelects();


        
    },
    
    inputs: {
        convertDatetimes: function() {
            $(".selectable_form .datetime").each(function(index) {
               $(this).addClass("selectable")
            });
        },
        convertSelects: function() {
            $("select").each(function(index) {
                $(this).addClass("selectable");
            });
        },
    }
};


$(document).ready(function() {
    numpad.convert_forms();
    
    $(window).keydown(numpad.handleKeydown);
    numpad.selectables = $(".selectable");
    numpad.select(0);
});