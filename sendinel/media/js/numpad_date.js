numpad.inputs.DateField = function(originalField) {
    this.originalField = originalField;
    this.selector = null;
    
    this.handleSelected = numpad.utils.handleSelected;
    this.handleDeselected = numpad.utils.handleDeselected;
    
    var htmlBlock =
    '<p class="selectable dates">' +
        '<input type="text" maxlength="4" name="" class="subselectable fourcharinput" />/' +
        '<input type="text" maxlength="2" name="" class="subselectable twocharinput" />/' +
        '<input type="text" maxlength="2" name="" class="subselectable twocharinput" />' +
    '</p>';
    
    this.createField = numpad.utils.createField;
    this.createField(htmlBlock);
        
    this.copyOriginalValues = function() {
        var originalValues = $(this.originalField).val().split("-");
        $(this.fieldElement).children("input:nth-child(1)").val(originalValues[0]);
        $(this.fieldElement).children("input:nth-child(2)").val(originalValues[1]);        
        $(this.fieldElement).children("input:nth-child(3)").val(originalValues[2]);                
    };
    this.copyOriginalValues();
    
    this.setupSelector = numpad.utils.setupSelector;
    this.setupSelector("input");
        
    this.handleKeydown = function(event) {
        var fieldObject = event.target.fieldElement.fieldObject;
        if($(event.target).attr("maxlength") && 
           $(event.target).val().length >= $(event.target).attr("maxlength") - 1) {
               // fieldObject.selector.selectNext();
               // $(fieldObject.selector.getSelected()).focus();
               return false;
        };
        return false;
    },        
        
    this.handleSubmit = function() {
        var fields = $(this.fieldElement).children("input");
        var date = $(fields[0]).val() + "-" + $(fields[1]).val()
                    + "-" + $(fields[2]).val();
        $(this.originalField).val(date);
    };
};