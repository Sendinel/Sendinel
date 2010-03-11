numpad.inputs.controlButtonsField = function(originalField) {
    this.originalField = originalField;
    this.selector = null;
        
    // var htmlBlock = '<div class="selectable select-div"></div>';
    // 
    // this.createField = numpad.utils.createField;
    // this.createField(htmlBlock);
    
    var fieldElement = this.originalField;
    fieldElement.fieldObject = this;
    this.fieldElement = fieldElement;    
    
    // this.copyOriginalValues = function() {
    //     var fieldElement = this.fieldElement;
    //     $(this.originalField).children("option").each(function(index) {
    //         var a = $('<a href="#""></a>');
    //         a.html($(this).html());
    //         a[0].originalValue = $(this).val();
    //         $(a).click(function() {
    //             fieldElement.fieldObject.selector.select(index);
    //             return false;
    //         });
    //         $(fieldElement).append(a);    
    //     });
    // };
    // this.copyOriginalValues();
    
    this.setupSelector = numpad.utils.setupSelector;
    this.setupSelector(".subselectable");
    this.selector.select(1);
    
    $(this.fieldElement).find(".subselectable").each(function(index,element) {
        element.url = $(element).siblings("[name]").first().val();
    });
 
    this.handleSubmit = function() {
        // this.originalField.selectedIndex = this.selector.selected;
        return;
    };
    
    // this.handleDeselected is not needed because selection stays on unfocus
    
    this.handleSelected = function() {
        var selected = this.selector.selected;
        this.selector.select(selected);
        $(this.selector.getSelected()).focus();
    };
    
};