
#TALVEZ MANTER ESSE CÓDIGO JUNTO COM A FUNÇÃO DE CADASTRO

#Inserir Email e Senha no banco de dados

#O python atuará como um programa serverside
from flask import Flask, request
from flask import redirect, url_for
import mysql.connector #comunicação com o banco de dados
from mysql.connector import errors

#Criação de uma instância do Flask
app = Flask(__name__)

#Conexão com o banco de dados
comms = mysql.connector.connect(
  host="localhost",
  user="Py_auth",
  password="Py_auth",
  database="marketplace"
)
cursor = comms.cursor()

#Recupera os dados do input html
@app.route('/login', methods = ['POST'])
def login():
    if(request.method == 'POST'):
        User = request.form['email']
        Senha = request.form['password']
        get_user = "SELECT Email, Senha FROM logins"
        cursor.execute(get_user)

        try:
            #pegar os logins
            for(Email, Senha) in cursor:
                  # print(f'Email: {Email}')
                  # print(f'Senha: {Senha}')
                  # print(f'USER_ID = {USER_ID}')
                  if(User == Email and Senha == Senha):
                      print('Deu good')
                      print(f'U: {User}, E:{Email},S1:{Senha}, S2:{Senha}')
                      return f'Login válido'

        except Exception:
             #Está dando TypeError
             print("os dados não existem no banco de dados")
             print(str(Exception))
             return 'SALVE'
        # except:
        #     return 'o erro'
        #finally:
        #     #return redirect(url_for('cadastro'))
        #     print ('Aoba')





#Processo para que o aplicativo seja exportado e executado ao clicar no botão HTMl

if (__name__ == '__main__'):
    app.run(debug= True)
