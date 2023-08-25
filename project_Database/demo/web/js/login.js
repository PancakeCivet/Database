$(document).ready(function () {
    $("#submit").click(function () {
        event.preventDefault(); 
        let password = $("#password").val();
        let username = $("#username").val();
        let data = { "username": username, "password": password };
        let data_json = JSON.stringify(data);
        $("#password").next("p").remove(); 
        $("#username").next("p").remove(); 
        $.ajax({
            url: "http://127.0.0.1:8080/login",
            type: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            data: data_json,
            success: function (type) {
                if( type == 1 ){
                    localStorage.setItem("username", username);
                    window.open("goods.html")
                }
                if( type == 2 )
                    $("#password").after("<p style='color: red;'>password mistake</p>");  
                if( type == 3 )
                    $("#username").after("<p style='color: red;'>username mistake</p>");  
            }
        });
    });
});
