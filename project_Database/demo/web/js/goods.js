$(document).ready(function () {
    let username = localStorage.getItem("username");
    if (username === null) {
    window.location.href = "login.html";
    } else {
    $(".username").text(username);
    }
    $(".logout-button").click(function () {
    localStorage.clear();
    });
    
    /*
    if( username == "游客模式"){
        
    }
    else{
    
    }
    */
    
    
    $("#out").click(function () {
        window.close();
        window.open("homepage.html")
    });
    });