numpad.inputs.datetime = {


    // '<p class="selectable times">' + 
    //     '<input type="text" maxlength="2" name="" class="subselectable twocharinput" />:' + 
    //     '<input type="text" maxlength="2" name="" class="subselectable twocharinput" />'+
    // '</p>';
    
    handleKeydown: function(event) {
        console.log("datetime handlekeydown");
        console.log(event);
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
    
    // handleSubmit: function() {
    //     console.log("datetime handlesubmit");
    //     console.log(this.originalField);
    //     
    //     var fields = $(this).children("input");
    //     if(this.fieldType == "date") {
    //         var date = $(fields[0]).val() + "-" + $(fields[1]).val()
    //                     + "-" + $(fields[2]).val();
    //         console.log(date);
    //         $(this.originalField).val(date);
    //     } else if(this.fieldType == "time") {
    //         var time = $(fields[0]).val() + ":" + $(fields[1]).val();
    //         console.log(time);
    //         $(this.originalField).val(time);
    //     }
    // }
};

