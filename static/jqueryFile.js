$(document).ready(function() {
    $("#loadingButton").css("visibility", "hidden");
    $("#data").keyup(function() {
        $("#loadingButton").css("visibility", "visible");
        var value = $("#data").val();
        $.post("/searchCard/",
        {
            userData: value,
        },
        function(data, status){
            $("#replace").empty();
            $("#replace").append(data);
            $("#loadingButton").css("visibility", "hidden");
        });
    });
});