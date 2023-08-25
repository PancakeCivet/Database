$(document).ready(function () {
    $("#submit").click(function () {
        event.preventDefault(); 
        $("#C_password").next("p").remove(); 
        $("#username").next("p").remove(); 
        let password = $("#password").val();
        let username = $("#username").val();
        let C_password = $("#C_password").val();
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
            $("#C_password").css("border-color", "red");
            $("#C_password").after("<p style='color: red;'>Passwords do not match.</p>");
        }
    });
});
