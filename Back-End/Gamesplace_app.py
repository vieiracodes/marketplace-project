#-------------------------------<Configurações>--------------------------------#

# Core do aplicativo
from flask import Flask, request, redirect, url_for, render_template, flash

#Sistema de login e autenticação - Expansão flask
from flask_login import (LoginManager, UserMixin, login_user, logout_user,
current_user, login_required)

#Criptografia de senha
from werkzeug.security import generate_password_hash, check_password_hash

#Geração de código para validação de email
from random import seed, randint

#Sistema de envio de emails - Expansão flask
from flask_mail import Mail, Message

#Comunicação com o banco de dados PostgreSQL
import psycopg2

#Comunicação com o banco de dados MySQL
# import mysql.connector
# from mysql.connector import errors #para tratamento de erros e exceções

#arquivo de configuração de variáveis de ambiente e outros dados usados no programa
from config import app_config, db_config, Config_email

#Para tratamento de erros e exceções
import werkzeug.exceptions


#Importação de variáveis de ambiente e outras configurações, caso necessário
is_validation = None
verify_code = ''
User_data = None
status_code = 404 #Código de teste padrão

#Criação de uma instância do Flask
app = Flask(__name__,
static_folder=app_config.static_folder,
template_folder=app_config.template_folder)

app.secret_key = app_config.secret_key
login_manager = LoginManager()
login_manager.__init__(app)
app.config.update(Config_email)
mail = Mail(app)

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
                host = db_config.host,
                user = db_config.user,
                password = db_config.password,
                database = db_config.database,
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

    #Operação para verificar todos os logins
    #NÂO UTILIZAR EM AMBIENTE DE PRODUÇÂO
    def get_all_users(self):
        self.comms = self.conectar_banco()
        cursor = self.comms.cursor()
        email_list = []
        senhas_list = []
        get_all_user = "SELECT Email FROM logins"
        cursor.execute(get_all_user)
        for(Email) in cursor:
            email_list.append(Email)
        self.comms.commit()
        return email_list


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
    # ver um modo mais eficiente de persistir o status da página e o código da
    # validação para a próxima etapa
    global is_validation
    global verify_code
    global User_data

    #Recupera os dados do input html
    if(request.method == 'POST'):
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
                return render_template('landing_pages/html/email_verify.html')
            else:
                return redirect(url_for('error', error='Usuário já existe! Tente outro email'))

        elif(is_validation == 'email_verify'):
            try:
                email_code = request.form['email_code']
                if(request.form['verify_code'] == 'verify_code'):
                    print(f'is_validation2: {is_validation}')
                    if(email_code == verify_code):
                        try:
                            db.inserir_user(User_data)
                            print('inserido!')
                            #inserir o valor perfil no HTML (será mostrado o usuário no canto)
                            # flash('Cadastro concluído!')
                            return redirect(url_for('home'))

                        except psycopg2.errors.UniqueViolation:
                            return redirect(url_for('error', error='Usuário já existe! Tente outro email'))

                        finally:
                            #encerra a comunicação com o banco de dados independente do resultado

                            print(f'is_validation3: {is_validation}')
                            db.comms.close()
                            verify_code = ''
                            is_validation = None

                    else:
                        print('Código inválido')
                        #Substituir essa página por
                        return redirect(url_for('error', error='Código inválido!'))

                        #popup flash nessa página
                        # return redirect(url_for('cadastro'))
            except werkzeug.exceptions.BadRequestKeyError:
                return redirect(url_for('error', error='Página recarregada!'))

        else:
            return render_template('landing_pages/html/page_error.html', status_code='002',
            complete_status= f'002 - Erro na etapa de cadastro')
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

        try:
            #se os valores existirem, são retornados
            if(Auth_tokens != None):
                Senha_hash = check_password_hash(Auth_tokens[1], Senha)

                if(Senha_hash == True):
                    User_token = User()
                    User_token.id = email
                    login_user(User_token, remember=lembra_user)

                    # flash('Login concluído!')
                    #popup flash nessa página
                    return redirect(url_for('home'))

                else:
                    # flash('Senha incorreta!')
                    #popup flash nessa página
                    return redirect(url_for('login'))

            #se Auth_tokens == None
            else:
                #Substituir essa página por
                return redirect(url_for('error', error='Usuário não encontrado no cadastro!'))

            #enviar um popup
                # flash('Usuário não encontrado!')
                #popup flash nessa página
                # return redirect(url_for('login'))
        except TypeError:
            return redirect(url_for('error', error='Usuário não encontrado'))
                #enviar um popup
                    # flash('Usuário não encontrado!')
                    #popup flash nessa página
                    # return redirect(url_for('login'))

        #encerra a comunicação com o banco de dados independente do resultado
        finally:

            db.comms.close()

    else:
        return render_template('landing_pages/html/login.html')

@app.route('/logout', methods = ['GET','POST'])
def logout():
    logout_user()
    #enviar um popup
    # flash('Conta desconectada com sucesso!')
    #popup flash nessa página
    return redirect(url_for('home'))

#-----------------------------------<Erros>------------------------------------#

#Página de erro - Trocar no futuro por popups flash
@app.route('/error', methods = ['GET', 'POST'])
def error():

    try:
        error = request.args['error']
    except:
        error = 'O erro deu erro :D'

    return render_template('error.html', error=error)

def alter_code(e):
    global status_code
    status_code = e.code
    return page_error(e)

@app.errorhandler(status_code)
def page_error(e):
    try:
        return render_template('landing_pages/html/page_error.html', status_code=e.code,
        complete_status= f'{e.code} - {e.name}'),status_code
    except:
        return render_template('landing_pages/html/page_error.html', status_code='???',
        complete_status= f'??? - Erro desconhecido')

#Alguns status de erro a serem exibidos na página de erro
#Erros de cliente
app.register_error_handler(400, alter_code)
app.register_error_handler(401, alter_code)
app.register_error_handler(403, alter_code)
app.register_error_handler(404, alter_code)
app.register_error_handler(405, alter_code)
app.register_error_handler(410, alter_code)

#Erros de servidor
app.register_error_handler(500, alter_code)
app.register_error_handler(501, alter_code)
app.register_error_handler(502, alter_code)
app.register_error_handler(503, alter_code)
app.register_error_handler(504, alter_code)
app.register_error_handler(505, alter_code)



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
    return render_template('landing_pages/html/home.html')
    #return 'Página do Marketplace: Não implementada ainda'

#página de produtos
@app.route('/pag_produtos/<path:path>', methods = ['GET', 'POST'])
def pag_produtos(path):
    return render_template(f'landing_pages/html/pag_produtos/{path}')

#Carrinho
@app.route('/carrinho.html', methods = ['GET', 'POST'])
def carrinho():
    return render_template('landing_pages/html/carrinho.html')

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

    return render_template('landing_pages/html/forum.html')


#------------------------------<Testes e devtools>-----------------------------#

#Operação para deletar todos os logins
#NÂO UTILIZAR EM AMBIENTE DE PRODUÇÂO
#Descomentar a linha abaixo para habilitar a rota de delete(/delete)
# @app.route('/delete', methods = ['POST', 'GET'])
def delete():
    lista_db = db.deletar_dados()
    return render_template('landing_pages/html/page_error.html', status_code='000',
    complete_status= lista_db)

# @app.route('/view_signatures', methods = ['POST', 'GET'])
def view_signatures():
    lista_db = db.get_all_users()
    return render_template('landing_pages/html/page_error.html', status_code='001',
    complete_status= lista_db)


#fins de teste

#Descomentar a linha abaixo para habilitar a rota de testes(/teste)
# @app.route('/teste', methods = ['POST', 'GET'])
# @login_required #Para fazer teste com página protegida, descomente essa também
def teste():

    # msg = Message(
    # subject= 'Verificação de email - Gamesplace (Teste2)',
    # recipients=[],
    # html= render_template('landing_pages/html/corpo_email.html', verify_code='1111')
    # )
    # mail.send(msg)

    return render_template('landing_pages/html/corpo_email.html', verify_code= '1234')

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



#Processo para que todo o backend e estrutura do site sejam executados ao
#rodar esse arquivo python

if (__name__ == '__main__'):
    app.run(debug= True)
