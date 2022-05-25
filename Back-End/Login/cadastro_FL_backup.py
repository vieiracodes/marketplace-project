

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


#Conexão com o banco de dados

def conectar_banco(platform="PostgreSQL"):
    # Para MySQL
    #Descomentar a importação das bibliotecas acima
    if(platform == 'MySQL'):
        comms = mysql.connector.connect(
          host="localhost",
          user="Py_auth",
          password="Py_auth",
          database="marketplace"
        )
    #Para PostgreSQL (Local)
    elif(platform == 'PostgreSQL1'):
        comms = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="INSERIR SENHA",
            database="postgres"
        )

    #Para PostgreSQL (Usado na plataforma Heroku)
    elif(platform == 'PostgreSQL'):
        comms = psycopg2.connect(
            host="ec2-52-3-2-245.compute-1.amazonaws.com",
            user="ojkcyslsolzjxw",
            password="de7fdc90c23fbfa7c949ff0b22cb8c55f8e7130c249da36863a9818fb07871f9",
            database="de7bgah134l4lf"
        )

    return comms


@login_manager.user_loader
def load_user(user_id):
    # try:
    #     return User_class1.get_id(user_id)
    # except:
    #     return None
     return User_class.get_id(user_id)


class User_class(UserMixin):
    def __init__(self, User, Senha, id):
        self.User = User
        self.Senha = Senha
        self.id = id


    def is_authenticated(self):
    	return True

    def is_active(self):
    	return True

    def is_annonymous(self):
    	return False

    def get_id(user_id):
        if user_id:
            return user_id


class User_class1(UserMixin):

    def get_id(user_id):
        if user_id:
            return user_id

    def get_user_token(user):
        if user:
            return user

#--------------------------------<Autenticação>--------------------------------#

#Função da página de cadastro
@app.route('/cadastro', methods = ['GET','POST'])
def cadastro():
    comms = conectar_banco()
    cursor = comms.cursor()


    #Recupera os dados do input html
    if(request.method == 'POST'):
        User = request.form['email']
        Senha = generate_password_hash(request.form['password'], method ='sha256')

        #Senha = request.form['password']
        User_data = (User, Senha)

        try:
        #Insere os dados no MySQL por meio dos comandos
            add_User = 'INSERT INTO logins (Email, Senha) VALUES (%s, %s)'
            cursor.execute(add_User, User_data)
            comms.commit()
        #inserir o valor perfil no HTML (será mostrado o usuário no canto)

            flash('Cadastro concluído!')
            return redirect(url_for('home'))#, perfil=User))

        # except mysql.connector.errors.IntegrityError:
        #     return redirect(url_for('error', error='Usuário já existe! Tente outro email'))
        #
        # except mysql.connector.errors.OperationalError:
        #     return redirect(url_for('error', error='Erro no servidor'))

        except psycopg2.errors.UniqueViolation:

            return redirect(url_for('error', error='Usuário já existe! Tente outro email'))
            #    return f'Usuário já existe! Tente outro email'

        finally:
            #encerra a comunicação com o banco de dados independente do resultado
            comms.close()
    else:
        return render_template('cadastro.html')



#Ler dados de usuário no banco de dados
@app.route('/login', methods = ['GET', 'POST'])
def login():
    lembra_user = False
    if(request.method == 'POST'):
        comms = conectar_banco()
        cursor = comms.cursor()
        User = request.form['email']
        Senha = request.form['password']

        print(f"Usuário: {User} Senha: {Senha} \n")

        #verificar se o login e senha estão no banco de dados
        get_user = f"""SELECT Email, Senha, id FROM logins
         WHERE Email = '{User}'"""# AND Senha = '{Senha}'"""

        #User_token = User_class('email@hash3.com', 'hash3', '5')
        # print(User_token)
        # print(User_token.User)
        # print(User_token.Senha)
        # print(User_token.id)
        #
        # login_user(User_token, remember=lembra_user)
        #load_user(Auth_tokens[2])

        try:
            cursor.execute(get_user)
            Auth_tokens = cursor.fetchone()


            #se os valores existirem, são retornados
            if(Auth_tokens != None):
                Senha_hash = check_password_hash(Auth_tokens[1], Senha)
                #Talvez tenha que usar o sqlalquemy
                User_token = User_class(Auth_tokens[0], Auth_tokens[1], Auth_tokens[2])
                print(User_token)
                print(User_token.User)
                print(User_token.Senha)
                print(User_token.id)

                if(Senha_hash == True):
                    login_user(User_token, remember=lembra_user)
                    #load_user(Auth_tokens[2])
                    load_user(User_token.id)
                    # print('logou! \n')
                    flash('Login concluído!')
                    return redirect(url_for('home'))
                else:
                    flash('Senha incorreta!')
                    return redirect(url_for('login'))

            else:
                return redirect(url_for('error', error='Usuário não encontrado no banco!'))

            #enviar um popup
                #return redirect(url_for('login'))

        #se não existirem (TypeError pois retorna um Nonetype)
        except TypeError as TE:
            return TE
        #    return redirect(url_for('error', error='Usuário não encontrado'))


        #encerra a comunicação com o banco de dados independente do resultado
        finally:

            comms.close()

    else:
        return render_template('login.html')

@app.route('/logout', methods = ['GET','POST'])
def logout():
    logout_user()
    return 'deslogado!'

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
        if(request.form['janela'] == 'Login'):
            return redirect(url_for('login'))
        elif(request.form['janela'] == 'Cadastro'):
            return redirect(url_for('cadastro'))
        elif(request.form['janela'] == 'Deletar'):
            return redirect(url_for('delete'))
        elif(request.form['janela'] == 'Forum'):
            return redirect(url_for('forum'))


    #
    # try:
    #     status = request.args['status']
    # except:
    #     status = 'Página Inicial'
    return render_template('index.html')
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
    comms = conectar_banco()
    cursor = comms.cursor()
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
    comms.commit()
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
