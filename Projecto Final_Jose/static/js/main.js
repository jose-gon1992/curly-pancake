passwordInput = document.getElementById("password-register")
passwordStatus = document.getElementById("passwordStatus")

passwordInput.addEventListener("keyup", (e) => {
    password = e.target.value
    if (password.length > 0) {
        var strongRegex = new RegExp("^(?=.{14,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*\\W).*$", "g");
        var mediumRegex = new RegExp("^(?=.{10,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))).*$", "g");
        
        if (strongRegex.test(password)) {
            passwordStatus.innerHTML = 'Força da Password: <span class="strong" style="color:green">Strong!</span>';
        } else if (mediumRegex.test(password)) {
            passwordStatus.innerHTML = 'Força da Password: <span class="strong" style="color:orange">Medium!</span>';
        } else {
            passwordStatus.innerHTML = 'Força da Password: <span class="strong" style="color:red">Weak!</span>';
        }
    }else {
        passwordStatus.innerHTML = ""
    }
})


// Fraca - Se o comprimento for menor que 10 caracteres e não contiver uma combinação de símbolos, maiúsculas e texto.
// Média - Se o comprimento for de 10 caracteres ou mais e tiver uma combinação de símbolos, maiúsculas e texto.
// Forte - Se o comprimento for de 14 caracteres ou mais e tiver uma combinação de símbolos, maiúsculas e texto.
