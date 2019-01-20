$(document).ready(function() {
    $("#data").keyup(function() {
        var value = $("#data").val();
        $.post("/searchCard/",
        {
            userData: value,
        },
        function(data, status){
            $("#replace").empty();
            $("#replace").append(data);
        });
    });
});