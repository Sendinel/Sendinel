
$(document).ready(function() {
    var target = $("<div></div>");
    var img_path = media_url + "img/";

    $("#id_way_of_communication")
    .hide()
    .after(target)
    .children("option[value!=]").each(function(index) {
        var img_url = img_path + $(this).val() + ".png";
        var img = $('<img />')
                    .attr('src', img_url)
                    .attr('alt', $(this).text());

        var value = $(this).val()
        img.addClass("clickable")
            .click(function() {
                $("#id_way_of_communication").val(value)
                    .next().children("").removeClass('selected');
                $(this).addClass("selected")
            });
        target.append(img);
    })
});

