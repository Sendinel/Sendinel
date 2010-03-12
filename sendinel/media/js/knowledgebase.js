var Knowledgebase = {
    resize_images: function(){
        var width = window.innerWidth - 300;
        var height = window.innerHeight - 300;
        var image = $('#picture_id');
        
        if (image.width() > width){
            image.height( (image.height() * width) / image.width() );
            image.width(width);
        }
        if (image.height() > height){
            image.width( (height * image.width()) / image.height() );
            image.height(height);
        }
    }
};