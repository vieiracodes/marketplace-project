var prosseguir = window.document.getElementById('prosseguir')

var cadastro   = NaN

prosseguir.addEventListener('click', regis)

function regis(){
    var emailHtml = document.getElementById('email')
    var senhaHtml = document.getElementById('password')

    var senha = senhaHtml.value
    var email = emailHtml.value

    cadastro = `E-mail: ${email} \nSenha: ${senha}`
}