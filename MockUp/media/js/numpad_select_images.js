numpad.inputs.SelectField = function(originalField) {
    this.originalField = originalField;
    this.selector = null;
        
    var htmlBlock = '<div class="selectable select-div"></div>';
    
    this.createField = numpad.utils.createField;
    this.createField(htmlBlock);
    
    this.copyOriginalValues = function() {
        var fieldElement = this.fieldElement;
        $(this.originalField).children("option").each(function(index, elem) {
            var img = $('<img src="#" class="subselectable" />');
            //img.html($(this).html());
            img.attr("src","../media/img/"+$(img).html());
            img[0].originalValue = $(this).val();
            $(img).click(function() {
                fieldElement.fieldObject.selector.select(index);
                return false;
            });
            $(fieldElement).append(img);    
            
        });
    };
    this.copyOriginalValues();
    
    this.setupSelector = numpad.utils.setupSelector;
    this.setupSelector("img");
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