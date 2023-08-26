$(document).ready(function () {
    $("#submit").click(function () {
        let password = $("#pwd").val();
        let username = $("#uname").val();
        let C_password = $("#cpwd").val();
        if(C_password == password){
            let data = { "username": username, "password": password };
            let data_json = JSON.stringify(data);
            $.ajax({
                url: "http://127.0.0.1:8080/register",
                type: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                data: data_json,
                success: function (flag) {
                    if(flag  == true){
                        window.close();
                        window.open("login.html")
                    }
                    else{
                        $("#username").after("<p style='color: red;'>User already exists</p>");
                    }
                },
            });
        }
        else{
            $("#cpwd").css("border-color", "red");
            $("#cpwd").after("<p style='color: red;'>Passwords do not match.</p>");
        }
    });
});
