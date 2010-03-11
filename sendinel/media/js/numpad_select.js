numpad.inputs.SelectField = function(originalField) {
    this.originalField = originalField;
    this.selector = null;
        
    var htmlBlock = '<div class="selectable select-div"></div>';
    
    this.createField = numpad.utils.createField;
    this.createField(htmlBlock);
    
    this.copyOriginalValues = function() {
        var fieldElement = this.fieldElement;
        $(this.originalField).children("option").each(function(index) {
            var a = $('<a href="#""></a>');
            a.html($(this).html());
            a[0].originalValue = $(this).val();
            $(a).click(function() {
                fieldElement.fieldObject.selector.select(index);
                return false;
            });
            $(fieldElement).append(a);    
        });
    };
    this.copyOriginalValues();
    
    this.setupSelector = numpad.utils.setupSelector;
    this.setupSelector("a");
    this.selector.select(this.originalField.selectedIndex);
 
    this.handleSubmit = function() {
        this.originalField.selectedIndex = this.selector.selected;
    };
    
    // this.handleDeselected is not needed because selection stays on unfocus
    
    this.handleSelected = function() {
        var selected = this.selector.selected;
        this.selector.select(selected);
        $(this.selector.getSelected()).focus();
    };
    
};