var numpad = {
    selector: null,

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
        var el = numpad.selector.getSelected();
        if(el.tagName.toLowerCase() == "a") {
            window.location = el.href;
        } else if (el.type && el.type.toLowerCase() == "submit") {
            this.submit();
            el.form.submit();
        } else {
            $(numpad.selector.getSelected()).trigger('click');
        }
    },
    
    convert_forms: function() {
        $(".selectable_form [name]").each(function() {
            if($(this).hasClass("vDateField")) {
                new numpad.inputs.DateField(this);
            }
            else if($(this).hasClass("vTimeField")) {
                new numpad.inputs.TimeField(this);
            }
            else if(this.tagName.toLowerCase() == "select") {
                new numpad.inputs.SelectField(this);
            }
        });
        
        $(".selectable_form").submit(numpad.submit);
            
        numpad.selector = new ElementSelector($(".selectable"));
        numpad.selector.select(0); 
    },
    
    submit: function() {
        $(".selectable").each(function(index) {
            if(this.fieldObject && this.fieldObject.handleSubmit) {
                this.fieldObject.handleSubmit();
            }
        })
    },
    
    inputs: {}
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
        if(number < 0 || number >= this.selectables.length) {
            return false;
        }
        var oldItem = this.selectables[this.selected];
        if(oldItem.fieldObject && oldItem.fieldObject.handleDeselected) {
           oldItem.fieldObject.handleDeselected();
        }
        $(oldItem).removeClass(this.selectedClass);
        
        this.selected = number;
        
        item = this.selectables[number]
        $(item).addClass(this.selectedClass)
        if(item.fieldObject && item.fieldObject.handleSelected) {
           item.fieldObject.handleSelected();
        } else {
            item.focus();
        }
    }
}

$(document).ready(function() {
    numpad.convert_forms();
    $(window).keydown(numpad.handleKeydown);
});


