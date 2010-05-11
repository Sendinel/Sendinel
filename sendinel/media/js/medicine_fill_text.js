$(document).ready(function(){
    $("#select-medicine").change(function(){
        var chosen_medicine = $("#select-medicine :selected").text();
        var text = template_text.replace("$medicine", chosen_medicine);
        $("#id_text").val(text);
        $("#id_text").keyup();
        return false;
    });
});