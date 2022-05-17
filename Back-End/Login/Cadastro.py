
#Inserir Email e Senha no banco de dados

#O python atuará como um programa serverside
from flask import Flask, request
from flask import redirect, url_for, render_template
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


#fins de teste
#OBS:Ele passa os parâmetros pela Url
@app.route('/teste', methods = ['POST', 'GET'])
def teste():
    # return f'User {User} e Senha {Senha}'
    #try:
    if(request.method == 'POST'):# or request.method == 'GET'):
        print(request.form('User'))
        return render_template('index.html',
         User_HTML = request.form('User'),
         Senha_HTML = request.form('Senha'))
    else:
        return render_template('index.html', User_HTML = 'Usuário', Senha_HTML = 'Senha')




#Função da página de cadastro
@app.route('/cadastro', methods = ['POST'])
def cadastro():

    #Recupera os dados do input html
    if(request.method == 'POST'):
        User = request.form['email']
        Senha = request.form['password']
        User_data = (User, Senha)

    try:
    #Insere os dados no MySQL por meio dos comandos
        add_User = 'INSERT INTO logins (Email, Senha) VALUES (%s, %s)'
        cursor.execute(add_User, User_data)
        comms.commit()
        #comms.close()
        return redirect(url_for('teste', User=User, Senha=Senha))
        # return f'Cadastro feito" Bem vindo, {User}. Sua senha {Senha}'

    except mysql.connector.errors.IntegrityError:

        print("O usuário já existe. Tente novamente")
        #comms.close()
        return 'Usuário já existe! ERRO 001'

    except mysql.connector.errors.OperationalError:
        return f'Erro no servidor: {User} e {Senha}'



#Ler dados de usuário no banco de dados
@app.route('/login', methods = ['POST'])
def login():
    if(request.method == 'POST'):
        User = request.form['email']
        Senha = request.form['password']
        get_user = "SELECT Email, Senha FROM logins"
        cursor.execute(get_user)

        # try:
            #pegar os logins
        for(Email, Senha) in cursor:
              # print(f'Email: {Email}')
              # print(f'Senha: {Senha}')
              # print(f'USER_ID = {USER_ID}')
              if(User == Email and Senha == Senha):
                  print('Deu good')
                  print(f'U: {User}, E:{Email},S1:{Senha}, S2:{Senha}')
                  return redirect(url_for('home'))
                  return f'Login válido'

        # except Exception:
        # #     #Está dando TypeError
        #      print("os dados não existem no banco de dados")
        #      print(str(Exception))
        #      return 'SALVE'
        # except:
        #     return 'o erro'
        #finally:
        #     #return redirect(url_for('cadastro'))
        #     print ('Aoba')



#Operação para deletar todos os logins
#NÂO UTILIZAR EM AMBIENTE DE PRODUÇÂO
@app.route('/delete', methods = ['POST'])
def delete():
    email_list = []
    senhas_list = []
    lista_banco = {'Emails: ' : email_list, 'Senhas:' : senhas_list}
    deletar = "DELETE FROM logins"
    cursor.execute(deletar)
    get_user = "SELECT Email, Senha FROM logins"
    cursor.execute(get_user)
    for(Email, Senha) in cursor:
        email_list.append(Email)
        senhas_list.append(Senha)
    comms.commit()
    return lista_banco




#Processo para que o aplicativo seja exportado e executado ao clicar no botão HTMl

if (__name__ == '__main__'):
    app.run(debug= True)
