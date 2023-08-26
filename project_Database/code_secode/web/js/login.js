$(document).ready(function () {
    $("#submit").click(function () {
        let password = $("#pwd").val();
        let username = $("#uname").val();
        let data = { "username": username, "password": password };
        let data_json = JSON.stringify(data);
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
                    window.close();
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
