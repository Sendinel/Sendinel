$(document).ready(function() {
    $("#id_text").attr("jVal", "{valid:function (val) { if (val.length < 10) return false; else return true; }, message:'" + gettext("This message seems to be too short.") + "'}");
    $("#id_text").attr("jValKey", "{valid:/[ a-zA-Z0-9._%+-@:,#*]/, message:'&quot;%c&quot; " + gettext("Invalid Character - No Special Characters Allowed") + "', cFunc:'$(\\'#formContainer\\').jVal()'}");
});