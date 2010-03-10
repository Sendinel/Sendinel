numpad.inputs.datetime = {


    createField: function(htmlBlock, selectedClass) {
        var fieldElement = $(htmlBlock)[0];
        fieldElement.fieldObject = this;
        console.log(fieldElement);
        
        $(fieldElement).children("input")
            .focus(function(event) {
                $(this).select();
            })
            .keydown(numpad.inputs.datetime.handleKeydown);
        
        this.selector = new ElementSelector($(fieldElement).children("input"));
        this.selector.selectedClass = selectedClass;
        
        this.fieldElement = fieldElement;
        $(this.originalField).after(fieldElement).hide();
    },
    
    handleKeydown: function(event) {
        var fieldObject = $(event.target).parent()[0].fieldObject;
        switch(event.keyCode) {
            case 37: // Arrow left
                console.log("select the previous field");
                fieldObject.selector.selectPrevious();
                $(fieldObject.selector.getSelected()).focus();
                break;
            case 39: // Arrow right
                console.log("select the next field");
                fieldObject.selector.selectNext();
                $(fieldObject.selector.getSelected()).focus();
                break;
            default:
                return true;
        }
        return false;
    },


    // functions that get binded to datetime selectables
    handleDeselected: function() {
        console.log("deselected: ");
        console.log(this);
        
        $(this).children(".subselectable").removeClass("datetime_selected");
    },
    
    handleSelected: function() {
        console.log("selected: ");
        console.log(this);

        this.selector.select(0);
        console.log($(this.fieldElement).children(".subselectable"));
        $(this.fieldElement).children(".subselectable").first().focus();
    },
};

