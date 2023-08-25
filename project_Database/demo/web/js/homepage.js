function open_login_HTML() {
    window.open("login.html")
}

function open_register_HTML(){
    window.open("register.html")
}

function other_HTML(){
    localStorage.setItem("username", "游客模式");
    window.open("goods.html")
}