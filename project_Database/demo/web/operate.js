function open_login_HTML() {
    window.open("login.html")
}

function open_register_HTML(){
    window.open("register.html")
}

function register_submitForm() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const data = { "username": username, "password": password };
    
}

function login_submitForm() {
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            const data = { "username": username, "password": password };
            
}

