var Knowledgebase = {
    resize_images: function(){
        var width = window.innerWidth - 400;
        var height = window.innerHeight - 150;
        
        var image = $('#picture');
        if(image.width() == 0 || image.height() == 0) {
            setTimeout(Knowledgebase.resize_images, 200);
        }
        // console.log("image width: " + image.width() + " height: " + image.height());
        
        if (image.width() > width){
            image.height( (image.height() * width) / image.width() );
            image.css("width", width);
        }
        if (image.height() > height){
            image.width( (height * image.width()) / image.height() );
            image.css("height", height)
        }
    }
};

$("#picture").ready(function() {
    Knowledgebase.resize_images();
    });
