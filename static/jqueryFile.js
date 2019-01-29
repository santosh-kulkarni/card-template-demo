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

    $("#clicksubmit").click(function() {
        var select =  $('#dropDownId').val();
        var name = $("#subname").val();
        var price = $("#subprice").val();
        if(select == "" || select == "...") {
            alert("Please Choose Your Category");
        }
        else if(name == "") {
            alert("Please Enter the subject Name");
        }
        else if (price == "") {
            alert("Please Enter Price");
        }
       else {
            $.ajax({
                method: "get",
                url : "/searchCard/putdata/",
                data : {
                    "select" : select,
                    "name" : name,
                    "price" : price
                },
                success: function(data) {
                    alert("Your Data is Added");
                    window.location.href = "/";
                }
            });
        }
    });

});
