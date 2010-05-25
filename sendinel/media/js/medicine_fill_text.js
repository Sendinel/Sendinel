$(document).ready(function(){
    $("#select-medicine").change(function(){
        var text = "";
        if ( $("#select-medicine :selected").val() != "0" ){
            var chosen_medicine = $("#select-medicine :selected").text();
            chosen_medicine = chosen_medicine.substr(0, chosen_medicine.lastIndexOf("(")-1);
            text = template_text.replace("$medicine", chosen_medicine);
        }
        $("#id_text").val(text);
        $("#id_text").keyup();
        return false;
    });
});