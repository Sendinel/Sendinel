numpad.utils = {


    createField: function(htmlBlock) {
        var fieldElement = $(htmlBlock)[0];
        fieldElement.fieldObject = this;
        this.fieldElement = fieldElement;
        $(this.originalField).after(fieldElement).hide();
    },
    
    setupSelector: function(selectables_selector) {
        $(this.fieldElement).children(selectables_selector)
            .focus(function(event) {
                $(this).select();
            })
            .keydown(numpad.utils.handleKeydown);
        var selectables = $(this.fieldElement).children(selectables_selector);
        this.selector = new ElementSelector(selectables);
        this.selector.selectedClass = "numpad_subselected";
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


    // functions that get binded to selectables
    handleDeselected: function() {
        console.log("deselected: ");
        console.log(this);

        var selectedClass = this.selector.selectedClass;
        this.selector.selectables.removeClass(selectedClass);
    },
    
    handleSelected: function() {
        console.log("selected: ");
        console.log(this);

        this.selector.select(0);
        this.selector.selectables.first().focus();
    },
};

