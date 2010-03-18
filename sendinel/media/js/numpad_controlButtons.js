numpad.inputs.controlButtonsField = function(originalField) {
    this.originalField = originalField;
    this.selector = null;
    
    var fieldElement = this.originalField;
    fieldElement.fieldObject = this;
    this.fieldElement = fieldElement;    
    
    this.setupSelector = numpad.utils.setupSelector;
    this.setupSelector(".subselectable");
    var subselectables =  $(this.fieldElement).find(".subselectable")
    
    if(subselectables.length == 1) {
        this.selector.selected = 0;                
    } else {
        this.selector.selected = 1;        
    }
    
    subselectables.each(function(index,element) {
        element.url = $(element).siblings("[name]").first().val();
    });
 
    this.handleSubmit = function() {
        // this.originalField.selectedIndex = this.selector.selected;
        return;
    };
    
    this.handleDeselected = numpad.utils.handleDeselected;
    
    this.handleSelected = function() {
        var selected = this.selector.selected;
        this.selector.select(selected);
        $(this.selector.getSelected()).focus();
    };
    
};