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
            this.handleSubmit = dt.handleSubmit;
            $(this).children(".subselectable")
                .focus(function(event) {
                    $(this).select();
                })
                .keydown(dt.handleKeydown);
        });
        $(".dates")[0].originalField = $("#id_date_0")[0];
        $(".dates")[0].fieldType = "date";
        $(".times")[0].originalField = $("#id_date_1")[0];
        $(".times")[0].fieldType = "time";
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
    
    handleSubmit: function() {
        console.log("datetime handlesubmit");
        console.log(this.originalField);
        
        var fields = $(this).children("input");
        if(this.fieldType == "date") {
            var date = $(fields[0]).val() + "-" + $(fields[1]).val()
                        + "-" + $(fields[2]).val();
            console.log(date);
            $(this.originalField).val(date);
        } else if(this.fieldType == "time") {
            var time = $(fields[0]).val() + ":" + $(fields[1]).val();
            console.log(time);
            $(this.originalField).val(time);
        }
    }
};

