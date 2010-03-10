var numpad = {
    selector: null,

    getSelected: function() {
        return $(numpad.selectables[numpad.selected]);
    },

    handleKeydown: function(event) {
        switch(event.keyCode) {
            case 13: // Enter
                numpad.clickOnSelected();
                break;
            case 38: // Arrow up
                numpad.selector.selectPrevious();
                break;
            case 39: //Arrow right
                numpad.clickOnSelected();
                break;
            case 40: // Arrow down
                numpad.selector.selectNext();
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
    
    convert_forms: function() {
        numpad.inputs.datetime.convert();
        // numpad.conversions.convertDatetimes();
        numpad.inputs.convertSelects();
        
        numpad.selector = new ElementSelector($(".selectable"));
        numpad.selector.select(0); 
    },
    
    submit: function() {
        $(".selectable").each(function(index) {
            if(this.handleSubmit) {
                this.handleSubmit();
            }
        })
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

ElementSelector = function(selectables) {
    this.selectables = selectables;
    this.selected = 0;
    this.selectedClass = "selected";
    
    this.getSelected = function() {
        return this.selectables[this.selected];
    }
    
    this.selectNext = function() {
        this.select(this.selected + 1);
    }
    this.selectPrevious = function() {
        this.select(this.selected - 1);
    }
    this.select = function(number) {
        // select element selectables[number],
        //  call handleDeselect on the deselected element and
        //  run handleSelect on the selected element
        console.log(number);
        console.log(this);
        if(number < 0 || number >= this.selectables.length) {
            return false;
        }
        var oldItem = this.selectables[this.selected];
        if(oldItem.handleDeselected) {
           oldItem.handleDeselected();
        }
        $(oldItem).removeClass(this.selectedClass);
        
        this.selected = number;
        
        item = this.selectables[number]
        $(item).addClass(this.selectedClass)
        if(item.handleSelected) {
           item.handleSelected();
        }
    }
}


$(document).ready(function() {
    numpad.convert_forms();
    
    $(window).keydown(numpad.handleKeydown);
});


