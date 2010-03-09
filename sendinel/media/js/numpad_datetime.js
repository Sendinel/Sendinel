numpad.inputs.datetime = {
    selector: null,

    convert: function() {
        var dt = numpad.inputs.datetime;
        dt.selector = new ElementSelector(".testform .selectable .subselectable");
        dt.selector.selectedClass = "datetime_selected";
        
        // TODO fix namespace problem^^
        $(".testform .selectable").each(function(index) {
            this.handleSelected = dt.handleSelected;
            this.handleDeselected = dt.handleDeselected;
            $(this).children(".subselectable")
                .focus(function(event) {
                    $(this).select();
                })
                .keydown(dt.handleKeydown);
        });
    },
    
    handleKeydown: function(event) {
        var dt = numpad.inputs.datetime;

        switch(event.keyCode) {
            case 37: // Arrow left
                console.log("select the previous field");
                dt.selector.selectPrevious();
                $(dt.selector.getSelected()).focus();
                break;
            case 39: // Arrow right
                console.log("select the next field");
                dt.selector.selectNext();
                $(dt.selector.getSelected()).focus();
                break;
            default:
                return true;
        }
        return false;
    },


    // functions that get binded to datetime selectables
    handleDeselected: function() {
        var dt = numpad.inputs.datetime;
        console.log("deselected: ");
        console.log(this);
        
        $(this).children(".subselectable").removeClass("datetime_selected");
    },
    
    handleSelected: function() {
        var dt = numpad.inputs.datetime;

        console.log("selected: ");
        console.log(this);
        dt.selector.selectables = $(this).children(".subselectable");

        dt.selector.select(0);
        $(this).children(".subselectable").first().focus();
    },
};
