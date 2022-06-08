

#-------------------------------<Configurações>--------------------------------#
#O python atuará como um programa serverside
from flask import Flask, request
from flask import redirect, url_for, render_template, flash
from flask_login import (LoginManager,UserMixin, login_user, logout_user,
 current_user, login_required)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from flask import jsonify
import psycopg2
from random import seed, randint
import werkzeug.exceptions
from flask import Response, make_response
# import mysql.connector #comunicação com o banco de dados
# from mysql.connector import errors

#Importação de variáveis de ambiente e outras configurações, caso necessário
is_validation = None
verify_code = ''
User_data = None

Config_email = {
"MAIL_SERVER": 'smtp.gmail.com',
"MAIL_PORT": 465,
"MAIL_USE_TLS": False,
"MAIL_USE_SSL": True,
"MAIL_USERNAME": 'emailverify.gamesplace@gmail.com',
"MAIL_PASSWORD": 'ocfqpzwspsaypngi',
"MAIL_DEFAULT_SENDER": 'emailverify.gamesplace@gmail.com'
}


#Criação de uma instância do Flask
app = Flask(__name__)
app.secret_key = 'insert_secret_key'
login_manager = LoginManager()
login_manager.__init__(app)
# login_manager.login_view = 'login'
# login_manager.login_message = 'Precisa logar, bro'
# login_manager.login_message_category = "info"
app.config.update(Config_email)
mail = Mail(app)
# def page_error(e):
#     try:
#         return render_template('landing_pages/html/page_error.html', status_code=e), 410
#     except:
#         return render_template('landing_pages/html/page_error.html', status_code='e')

# app.register_error_handler(404, page_error)
# app.register_error_handler(410, page_error)
# app.register_error_handler(404, page_error)

class User(UserMixin):
    pass

class Banco_de_dados():
    def __init__(self):
        self.Auth_tokens = None

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
        try:
            cursor.execute(get_user)
            self.Auth_tokens = cursor.fetchone()
            return self.Auth_tokens
        except TypeError:
            print('levantou a exceção interna')
            return None




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
    if(db.Auth_tokens != None):
        if email not in db.Auth_tokens:
            return

    User_token = User()
    User_token.id = email
    return User_token


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if(db.Auth_tokens != None):
        if email not in db.Auth_tokens:
            return

    User_token = User()
    User_token.id = email
    return User_token



#--------------------------------<Autenticação>--------------------------------#

#Função da página de cadastro
@app.route('/cadastro', methods = ['GET','POST'])
def cadastro():
    # a função reseta sempre que a pagina recarrega.
    # ver um modo mais eficiente de persistir o status da página e o código da
    # validação para a próxima etapa
    #print('is validation resetou')
    global is_validation
    global verify_code
    global User_data
    #print(f'mas o valor de validation é: {is_validation}')
    #Recupera os dados do input html
    if(request.method == 'POST'):
        # try:
        #     is_validation = request.args['isvalidation']
        # except:
        #     is_validation = None
        if(is_validation == None):

            email = request.form['email']
            Senha = generate_password_hash(request.form['password'], method ='sha256')
            email_exists = db.verificar_user(email)
            if(not email_exists):
                for i in range(4):
                    verify_code+=str(randint(0, 9))
                print(f'Código: {verify_code}')

                msg = Message(
                subject= 'Verificação de email - Gamesplace',
                recipients=[email, "emailverify.gamesplace@gmail.com"],
                html= render_template('landing_pages/html/corpo_email.html', verify_code=verify_code)
                )
                mail.send(msg)

                User_data = (email, Senha)

                is_validation = 'email_verify'
                #print(is_validation)
                return render_template('landing_pages/html/email_verify.html')
            else:
                return redirect(url_for('error', error='Usuário já existe! Tente outro email'))

        elif(is_validation == 'email_verify'):
            try:
                email_code = request.form['email_code']
                if(request.form['verify_code'] == 'verify_code'):
                    print(f'is_validation2: {is_validation}')
                    if(email_code == verify_code):
                        # print(f'v_c(1): {verify_code[1]}')
                        try:
                            db.inserir_user(User_data)

                            #inserir o valor perfil no HTML (será mostrado o usuário no canto)
                            flash('Cadastro concluído!')
                            return redirect(url_for('home'))

                        except psycopg2.errors.UniqueViolation:
                            return redirect(url_for('error', error='Usuário já existe! Tente outro email'))

                        finally:
                            #encerra a comunicação com o banco de dados independente do resultado
                            print('aqui deu finally')
                            print(f'is_validation3: {is_validation}')
                            db.comms.close()
                            verify_code = ''
                            is_validation = None

                    else:
                        print('Código inválido')
                        return redirect(url_for('error', error='Código inválido!'))
                        # return redirect(url_for('cadastro'))
            except werkzeug.exceptions.BadRequestKeyError:
                return redirect(url_for('error', error='Página recarregada!'))

        else:
            return '21'
    else:
        is_validation = None
        verify_code = ''
        User_data = None
        return render_template('landing_pages/html/cadastro.html')



#Ler dados de usuário no banco de dados
@app.route('/login', methods = ['GET', 'POST'])
def login():
    lembra_user = False
    if(request.method == 'POST'):

        email = request.form['email']
        Senha = request.form['password']

        Auth_tokens = db.verificar_user(email)
        #print(Auth_tokens)
        try:
            #se os valores existirem, são retornados
            if(Auth_tokens != None):
                Senha_hash = check_password_hash(Auth_tokens[1], Senha)

                if(Senha_hash == True):
                    User_token = User()
                    User_token.id = email
                    login_user(User_token, remember=lembra_user)

                    flash('Login concluído!')
                    return redirect(url_for('home'))

                else:
                    flash('Senha incorreta!')
                    return redirect(url_for('login'))

            #se Auth_tokens == None
            else:
                return redirect(url_for('error', error='Usuário não encontrado no banco!'))


            #enviar um popup
                # flash('Usuário não encontrado!')
                # return redirect(url_for('login'))

        #se não existirem (TypeError pois retorna um Nonetype)
        except TypeError:
            #print('levantou a exceção externa')
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


#-----------------------------------<Erros>------------------------------------#
teste_code = 404
def teste_alter_code(e):
    global teste_code
    teste_code = e.code
    return page_error(e)

@app.errorhandler(teste_code)
def page_error(e):
    try:
        return render_template('landing_pages/html/page_error.html', status_code=e.code,
        complete_status= f'{e.code} - {e.name}'),teste_code
    except:
        return render_template('landing_pages/html/page_error.html', status_code='???',
        complete_status= f'??? - Erro não encontrado')

app.register_error_handler(400, teste_alter_code)
app.register_error_handler(401, teste_alter_code)
app.register_error_handler(403, teste_alter_code)
app.register_error_handler(404, teste_alter_code)
app.register_error_handler(405, teste_alter_code)
app.register_error_handler(410, teste_alter_code)

app.register_error_handler(500, teste_alter_code)
app.register_error_handler(501, teste_alter_code)
app.register_error_handler(502, teste_alter_code)
app.register_error_handler(503, teste_alter_code)
app.register_error_handler(504, teste_alter_code)
app.register_error_handler(505, teste_alter_code)



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

        #verificar autorização do usuário (se pode postar ou responder)
        #Usar o current_user.is_authenticated

    return 'Página do Fórum: Não implementada ainda'

#------------------------------<Testes e devtools>-----------------------------#

#Operação para deletar todos os logins
#NÂO UTILIZAR EM AMBIENTE DE PRODUÇÂO
@app.route('/delete', methods = ['POST'])
def delete():
    lista_db = db.deletar_dados()
    return lista_db



#fins de teste
#OBS:Ele passa os parâmetros pela Url
@app.route('/teste', methods = ['POST', 'GET'])
# @login_required
def teste():
    return render_template('landing_pages/html/page_error.html')
    # msg = Message(
    # subject= 'Verificação de email - Gamesplace (Teste)',
    # recipients=["jherrerocavadas@gmail.com","emailverify.gamesplace@gmail.com"],
    # html= render_template('landing_pages/html/corpo_email.html', verify_code='543216')
    # )
    # mail.send(msg)
    #
    # return render_template('landing_pages/html/corpo_email.html', verify_code= 'enviado!')

    # print(f'current_user: {current_user}')
    # print(f'current_user.id: {current_user.id}')
    # print(f'current_user.is_authenticated: {current_user.is_authenticated}')
    # return render_template('teste_login.html')
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
