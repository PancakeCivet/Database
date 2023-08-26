function login() {
    window.close();
    window.open("login.html")
}

function register(){
    window.close();
    window.open("register.html")
}

function other(){
    window.close();
    localStorage.setItem("username", "游客模式");
    window.open("goods.html")
}