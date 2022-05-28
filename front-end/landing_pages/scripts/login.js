var prosseguir = window.document.getElementById('prosseguir')

var cadastro   = NaN

prosseguir.addEventListener('click', regis)

function regis(){
    var emailHtml = document.getElementById('email')
    var senhaHtml = document.getElementById('password')

    var senha = senhaHtml.value
    var email = emailHtml.value

    cadastro = `E-mail: ${email} \nSenha: ${senha}`

    //A função "emailRegistrado" tem o intuito de ilustrar o funcionamento do IF e deve ser substituida pela função correta
    if (emailRegistrado().jaRegistrado){
        window.alert('Email Já cadastrado !')
    }

    //Variável "email_Cadastrado" tem o intuito de ilustrar o funcionamento do IF e deve ser substituida pela váriavel correta
    if (email != email_Cadastrado){
        window.alert('Email Inválido !')
    }

    //Variável "senha_Cadastrada" tem o intuito de ilustrar o funcionamento do IF e deve ser substituida pela váriavel correta
    if (senha != senha_Cadastrada){
        window.alert('Senha Inválida !')
    }
}
