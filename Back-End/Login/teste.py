
#Inserir Email e Senha no banco de dados

#O python atuará como um programa serverside
from flask import Flask, request
from flask import redirect, url_for, render_template


#Criação de uma instância do Flask
app = Flask(__name__, static_folder="Back-End\Login\templates\static")

#Recupera os dados do input html
@app.route('/pagina')
def pagina():
    return render_template('index.html', User = 'Admin', Senha = "admin123")



#Processo para que o aplicativo seja exportado e executado ao clicar no botão HTMl

if (__name__ == '__main__'):
    app.run(debug= True)
