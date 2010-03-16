var numpad = {
    selector: null,
    selectedClass: "selected",
    
    handleKeydown: function(event) {
        switch(event.keyCode) {
            case 13: // Enter
                numpad.clickOnSelected(numpad.selector.getSelected());
                break;
            case 38: // Arrow up
                numpad.selector.selectPrevious();
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
    
    clickOnSelected: function(element) {
        var eTypeLow = (element.type || "").toLowerCase()
        if(element){
            if(element.tagName.toLowerCase() == "a") {
                window.location = element.href;
                return;
            } else if (eTypeLow == "submit" || eTypeLow == "button") {
                if(element.url) {
                    window.location = element.url;
                    return;                    
                }
                this.submit();
                element.form.submit();
                return;
            }            
                
            // recursively clicking all subselected children
            $(element).find(".numpad_subselected").each($.proxy(function(index,element) {
                return this.clickOnSelected(element);
            }, this));            
        }
        return;
    },
        
    convert_forms: function() {
        // if we already have selected elements, deselect them
        $("." + numpad.selectedClass).each(function(index, elem) {
            $(elem).removeClass(numpad.selectedClass)
        });
        
        $(".selectable_container [name]").each(function() {
            if($(this).hasClass("vDateField")) {
                new numpad.inputs.DateField(this);
            }
            else if($(this).hasClass("vTimeField")) {
                new numpad.inputs.TimeField(this);
            }
            else if(this.tagName.toLowerCase() == "select") {
                new numpad.inputs.SelectField(this);
            }
            else if($(this).hasClass("control-buttons")) {
                new numpad.inputs.controlButtonsField(this);
            }
        });
        
        $(".selectable_container").submit(numpad.submit);
            
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
    this.selectedClass = numpad.selectedClass;
    
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


