

#-------------------------------<Configurações>--------------------------------#
#O python atuará como um programa serverside
from flask import Flask, request
from flask import redirect, url_for, render_template, flash
from flask_login import (LoginManager,UserMixin, login_user, logout_user,
 current_user, login_required,)
from werkzeug.security import generate_password_hash, check_password_hash
# from User_config import User_class
from flask import jsonify
import psycopg2
# import mysql.connector #comunicação com o banco de dados
# from mysql.connector import errors

#Importação de variáveis de ambiente e outras configurações, caso necessário



#Criação de uma instância do Flask
app = Flask(__name__)
app.secret_key = 'insert_secret_key'
login_manager = LoginManager()
login_manager.__init__(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Precisa logar, bro'
login_manager.login_message_category = "info"


class User(UserMixin):
    pass

class Banco_de_dados():
    def __init__(self):
        self.Auth_tokens = []

    #Conexão com o banco de dados
    def conectar_banco(self, platform="PostgreSQL"):

        #Para PostgreSQL
        if(platform == 'PostgreSQL'):
            comms = psycopg2.connect(
                host="ec2-52-3-2-245.compute-1.amazonaws.com",
                user="ojkcyslsolzjxw",
                password="de7fdc90c23fbfa7c949ff0b22cb8c55f8e7130c249da36863a9818fb07871f9",
                database="de7bgah134l4lf"
            )
            return comms

    def verificar_user(self, email):
        #melhorar essa atribuição depois
        self.comms = self.conectar_banco()
        #comms = self.comms
        cursor = self.comms.cursor()
        get_user = f"""SELECT Email, Senha, id FROM logins
        WHERE Email = '{email}'"""
        cursor.execute(get_user)
        self.Auth_tokens = cursor.fetchone()
        return self.Auth_tokens




    def inserir_user(self, User_data):
        #melhorar essa atribuição depois
        #conexão do banco de dados
        self.comms = self.conectar_banco()
        cursor = self.comms.cursor()
        #Insere os dados no PostgreSQL por meio dos comandos
        add_User = 'INSERT INTO logins (Email, Senha) VALUES (%s, %s)'
        cursor.execute(add_User, User_data)
        self.comms.commit()



    #Operação para deletar todos os logins
    #NÂO UTILIZAR EM AMBIENTE DE PRODUÇÂO
    def deletar_dados(self):
        self.comms = self.conectar_banco()
        cursor = self.comms.cursor()
        email_list = []
        senhas_list = []
        lista_banco = {'Emails: ' : email_list, 'Senhas:' : senhas_list}
        deletar = "DELETE FROM logins"
        cursor.execute(deletar)

        get_user = "SELECT Email, Senha, id FROM logins"
        cursor.execute(get_user)
        for(Email, Senha) in cursor:
            email_list.append(Email)
            senhas_list.append(Senha)
        self.comms.commit()
        return lista_banco



db = Banco_de_dados()


#decoradores de user_loader e request_loader, usados pelo flask_login

@login_manager.user_loader
def user_loader(email):
    if email not in db.Auth_tokens:
        return

    User_token = User()
    User_token.id = email
    return User_token


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in db.Auth_tokens:
        return

    User_token = User()
    User_token.id = email
    return User_token



#--------------------------------<Autenticação>--------------------------------#

#Função da página de cadastro
@app.route('/cadastro', methods = ['GET','POST'])
def cadastro():

    #Recupera os dados do input html
    if(request.method == 'POST'):
        email = request.form['email']
        Senha = generate_password_hash(request.form['password'], method ='sha256')

        #Senha = request.form['password']
        User_data = (email, Senha)

        try:
            db.inserir_user(User_data)

            #inserir o valor perfil no HTML (será mostrado o usuário no canto)
            flash('Cadastro concluído!')
            return redirect(url_for('home'))

        except psycopg2.errors.UniqueViolation:
            return redirect(url_for('error', error='Usuário já existe! Tente outro email'))

        finally:
            #encerra a comunicação com o banco de dados independente do resultado
            db.comms.close()
    else:
        return render_template('landing_pages/html/cadastro.html')



#Ler dados de usuário no banco de dados
@app.route('/login', methods = ['GET', 'POST'])
def login():
    lembra_user = False
    if(request.method == 'POST'):
        email = request.form['email']
        Senha = request.form['password']
        print('login')

        try:
            Auth_tokens = db.verificar_user(email)
            print(f'Auth_tokens: {Auth_tokens}')

            #se os valores existirem, são retornados
            if(Auth_tokens != None):
                Senha_hash = check_password_hash(Auth_tokens[1], Senha)
                if(Senha_hash == True):
                    User_token = User()
                    User_token.id = email
                    login_user(User_token, remember=lembra_user)
                    print('oi!')
                    print(f'\n current_user: {User_token.id} \n')
                    flash('Login concluído!')
                    #print(request.form['prosseguir'])
                    return redirect(url_for('home'))

                else:
                    print('passou aqui')
                    flash('Senha incorreta!')
                    return redirect(url_for('login'))

            #se Auth_tokens == None
            else:
                print('tá no else')
                return redirect(url_for('error', error='Usuário não encontrado no banco!'))


            #enviar um popup
                # flash('Usuário não encontrado!')
                # return redirect(url_for('login'))

        #se não existirem (TypeError pois retorna um Nonetype)
        except TypeError:
            print('tá no except')
            return redirect(url_for('error', error='Usuário não encontrado'))
                #enviar um popup
                    # flash('Usuário não encontrado!')
                    # return redirect(url_for('login'))


        #encerra a comunicação com o banco de dados independente do resultado
        finally:

            db.comms.close()

    else:
        return render_template('landing_pages/html/login.html')

@app.route('/logout', methods = ['GET','POST'])
def logout():
    logout_user()
    flash('Conta desconectada com sucesso!')
    return redirect(url_for('home'))



#página de erro customizada no futuro (se der)
@app.route('/error', methods = ['GET', 'POST'])
def error():

    try:
        error = request.args['error']
    except:
        error = 'O erro deu erro :D'

    return render_template('error.html', error=error)


#--------------------------------<Marketplace>---------------------------------#
@app.route('/', methods = ['GET', 'POST'])
def home():
    #comms = conectar_banco()
    #cursor = comms.cursor()
        #Elementos que podem ser enviados ao banco de dados:
            #Produto (Título)
            #Preço
            #Fotos (Caminho das imagens, talvez)
            #Estado do anúncio (aberto, encerrado)


    if(request.method == 'POST'):
        print(request.form['prosseguir'])
        #
        # if(request.form['janela'] == 'Login'):
        #     return redirect(url_for('login'))
        # elif(request.form['janela'] == 'Cadastro'):
        #     return redirect(url_for('cadastro'))
        # elif(request.form['janela'] == 'Deletar'):
        #     return redirect(url_for('delete'))
        # elif(request.form['janela'] == 'Forum'):
        #     return redirect(url_for('forum'))

    return render_template('landing_pages/html/home.html')
    #return 'Página do Marketplace: Não implementada ainda'



#-----------------------------------<Fórum>------------------------------------#
@app.route('/forum', methods = ['GET', 'POST'])
def forum():
    #comms = conectar_banco()
    #cursor = comms.cursor()
    #Elementos que podem ser enviados ao banco de dados:
        #Perguntas (Título)
        #Perguntas (Explicação)
        #Respostas
        #Estado do 'post'/pergunta(aberto, encerrado)
        #Usuários que publicaram perguntas e respostas

    return 'Página do Fórum: Não implementada ainda'

#------------------------------<Testes e devtools>-----------------------------#

#Operação para deletar todos os logins
#NÂO UTILIZAR EM AMBIENTE DE PRODUÇÂO
@app.route('/delete', methods = ['POST'])
def delete():
    lista_db = db.deletar_dados()
    return lista_banco



#fins de teste
#OBS:Ele passa os parâmetros pela Url
@app.route('/teste', methods = ['POST', 'GET'])
# @login_required
def teste():
    print(current_user)
    print(current_user.is_authenticated)
    return render_template('teste_login.html')
    # comms = conectar_banco()
    # cursor = comms.cursor()
    # # return f'User {User} e Senha {Senha}'
    # #try:
    # if(request.method == 'POST'):# or request.method == 'GET'):
    #     #print(request.form('User'))
    #     return render_template('index.html',
    #      User_HTML = request.form('User'),
    #      Senha_HTML = request.form('Senha'))
    # else:
        # return render_template('index.html', User_HTML = 'Usuário', Senha_HTML = 'Senha')








#Processo para que o aplicativo seja executado como um site

if (__name__ == '__main__'):
    app.run(debug= True)
