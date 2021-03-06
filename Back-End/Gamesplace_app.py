#-------------------------------<Configurações>--------------------------------#

# Core do aplicativo
from flask import Flask, request, redirect, url_for, render_template, flash, abort

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
from Fórum.Fórum import Forum_thread
from Login.Sua_conta.account import Account
#Para tratamento de erros e exceções

# Ver de importar apenas exceções específicas
import werkzeug.exceptions
import jinja2.exceptions


#Importação de variáveis de ambiente e outras configurações, caso necessário
# OPTIMIZE:
is_validation = None
verify_code = ''
User_data = None
status_code = 404 #Código de teste padrão

#Criação de uma instância do Flask
app = Flask(__name__,
static_folder=app_config.static_folder,
template_folder=app_config.template_folder)

#Inicialização e configuração das extensões flask
app.secret_key = app_config.secret_key
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.__init__(app)
app.config.update(Config_email)
mail = Mail(app)



# Classe usada pelo Flask Login
class User(UserMixin):
    pass

# Classe para manipulação do banco de dados
class Banco_de_dados():
    def __init__(self):
        #Não colocar None pois senão a primeira carregada da página indica como
        #como se houvesse um usuário logado já (Não entra como anônimo).
        self.Auth_tokens = []

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


                #-------------------<Contas>-------------------#

    def alterar_user(self, **config_args):
        #por algum motivo aqui dá erro se o self for chamado sem os parênteses
        self.comms = self().conectar_banco()
        cursor = self.comms.cursor()
        callback_status = {'mensagem':None, 'redirecionamento':None}

        novo_email = config_args["email"]
        senha_input = config_args["senha"]
        senha = None

        Senha_hash = check_password_hash(self().verificar_user(current_user.id)[1], senha)
        if(Senha_hash):
            if(novo_email != ''):
                alterar_dados = f"""UPDATE logins
                SET Email='{novo_email}'
                Where Email='{current_user.id}' """
            elif(senha_input != ''):
                senha_nova = generate_password_hash(senha_input, method ='sha256')
                alterar_dados = f"""UPDATE logins
                SET Senha='{senha_nova}'
                Where Email='{current_user.id}' """

            #Só pra fazer um envio ao servidor ao invés de envios de cada argumento separadamente
            elif(novo_email != '' and senha_input != ''):
                alterar_dados = f"""UPDATE logins
                SET Email='{novo_email}', Senha='{senha_nova}'
                Where Email='{current_user.id}' """

            else:
                callback_status['mensagem'] ='Algum valor de alteração precisa ser inserida!'
                callback_status['redirecionamento'] = redirect(url_for('conta'))
                self.comms.close()
                return callback_status


            cursor.execute(alterar_dados)
            self.comms.commit()
            callback_status['mensagem'] ='Dados alterados com sucesso!'
        else:
            callback_status['mensagem'] ='A senha de autenticação é inválida!'

        callback_status['redirecionamento'] = redirect(url_for('conta_feature', recurso = 'change_data'))
        self.comms.close()
        return callback_status




    def deletar_user(self, **config_args):
        self.comms = self.conectar_banco(self, platform="PostgreSQL")
        cursor = self.comms.cursor()
        callback_status = {'mensagem':None, 'redirecionamento':None}

        email = 'None' #current_user.id
        senha = config_args["senha"]

        #Senha_hash = check_password_hash(self.verificar_user(email)[1], senha)
        Senha_hash = True
        if(Senha_hash):
            # deletar = f"DELETE FROM logins WHERE Email = {email}"
            # cursor.execute(deletar)
            # self.comms.close()
            print(email)
            callback_status['mensagem'] = 'Dados excluídos com sucesso!'
            callback_status['redirecionamento'] = redirect(url_for('home'))

            #Conferir isso aqui posteriormente
            callback_status['is_target_top'] = True
        else:
            callback_status['mensagem'] ='Não foi possível deletar os dados. A senha de autenticação é inválida!'
            callback_status['redirecionamento'] = redirect(url_for('conta_feature', recurso = 'delete_user'))
            callback_status['is_target_top'] = False

        self.comms.close()
        return callback_status


#EXPERIMENTAL - Para testes futuros
    def insert_payment_method(self, **kwargs):
        self.comms = self.conectar_banco(self, platform="PostgreSQL")
        cursor = self.comms.cursor()
        callback_status = {'mensagem':None, 'redirecionamento':None}

        callback_status['mensagem'] ='Não implementado ainda'
        callback_status['redirecionamento'] = redirect(url_for('conta_feature', recurso = 'insert_payment'))
        # callback_status['redirecionamento'] = redirect(url_for('conta'))
        print(callback_status['redirecionamento'])
        print()
        print(type(callback_status['redirecionamento']))
        self.comms.close()
        return callback_status




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
forum_methods = Forum_thread()


#decoradores de user_loader e request_loader, usados pelo flask_login
@login_manager.user_loader
def load_user(email):
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
    #talvez com arquivo json??
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
                # print(f'Código: {verify_code}')#DEBUG

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
                flash('Usuário já existe! Tente outro email')
                return redirect(url_for('cadastro'))
                #return redirect(url_for('error', error='Usuário já existe! Tente outro email'))

        elif(is_validation == 'email_verify'):
            try:
                email_code = request.form['email_code']
                if(request.form['verify_code'] == 'verify_code'):
                    print(f'is_validation2: {is_validation}')
                    if(email_code == verify_code):
                        try:
                            db.inserir_user(User_data)
                            # print('inserido!')#DEBUG

                            #inserir o valor perfil no HTML (será mostrado o usuário no canto)
                            flash('Cadastro concluído!')
                            return redirect(url_for('home'))

                        except psycopg2.errors.UniqueViolation:
                            flash('Usuário já existe! Tente outro email')
                            return redirect(url_for('cadastro'))

                        finally:
                            #encerra a comunicação com o banco de dados independente do resultado

                            print(f'is_validation3: {is_validation}')
                            db.comms.close()
                            verify_code = ''
                            is_validation = None

                    else:
                        print('Código inválido')

                        flash('Código inválido!')
                        return redirect(url_for('cadastro'))

                        #popup flash nessa página
                        flash('Código de validação inválido')
                        return redirect(url_for('cadastro'))
            except werkzeug.exceptions.BadRequestKeyError:
                flash('Página recarregada!')
                return redirect(url_for('cadastro'))


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
    #lembra_user = False
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
                    login_user(User_token)#, remember=lembra_user)

                    flash('Login concluído!')
                    #popup flash nessa página
                    return redirect(url_for('home'))

                else:
                    flash('Senha incorreta!')
                    #popup flash nessa página
                    return redirect(url_for('login'))

            #se Auth_tokens == []
            else:

            #enviar um popup
                flash('Usuário não encontrado!')
                #popup flash nessa página
                return redirect(url_for('login'))
        except TypeError:
                #enviar um popup
                    flash('Usuário não encontrado!')
                    #popup flash nessa página
                    return redirect(url_for('login'))

        #encerra a comunicação com o banco de dados independente do resultado
        finally:
            db.comms.close()

    else:
        return render_template('landing_pages/html/login.html')

@app.route('/logout', methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    db.Auth_tokens = []
    #enviar um popup
    flash('Conta desconectada com sucesso!')
    #popup flash nessa página
    return redirect(url_for('home'))

@login_manager.unauthorized_handler
def not_logged():
    flash('Você precisa estar logado para acessar essa página!')
    return redirect(url_for('home'))


#-----------------------------------<Erros>------------------------------------#

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
app.register_error_handler(406, alter_code)
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

#Teste pra ver se tá logando
    print(db.Auth_tokens)
    print(f'current_user: {current_user}')
    try:
        print(f'Id: {current_user.id}')
    except AttributeError:
        pass
    print(f'Ativo?: {current_user.is_active}')
    print(f'Autenticado?: {current_user.is_authenticated}')
    print(f'Anônimo?: {current_user.is_anonymous}')


    #Sugestões de autocomplete na barra de pesquisa
    sugestions = ['PS4', 'PS3', 'PlayStation4', 'PlayStation3', 'PlayStation',
    'Xbox One', 'Xbox360', 'Xbox', 'Switch', 'Nintendo Switch', 'Nintendo', '3DS',
    'Nintendo 3DS']

        #Elementos que podem ser enviados ao banco de dados:
            #Produto (Título) - Ok
            #Preço - Ok
            #Fotos (Caminho das imagens, talvez)
            #Estado do anúncio (aberto, encerrado)
    return render_template('landing_pages/html/home.html', sugestions=sugestions)
    #return 'Página do Marketplace: Não implementada ainda'

#página de produtos
@app.route('/pag_produtos/<path:path>', methods = ['GET', 'POST'])
def pag_produtos(path):
    #Sugestões de autocomplete na barra de pesquisa
    #tentar captar o nome dos produtos existentes (arquivo produtos.js)
    sugestions = ['inserir sugestões de autocomplete aqui']
    return render_template(f'landing_pages/html/pag_produtos/{path}')#, sugestions=sugestions)

#Carrinho
@app.route('/carrinho.html', methods = ['GET', 'POST'])
def carrinho():
    #Sugestões de autocomplete na barra de pesquisa
    sugestions = ['PS4', 'PS3', 'PlayStation4', 'PlayStation3', 'PlayStation',
    'Xbox One', 'Xbox360', 'Xbox', 'Switch', 'Nintendo Switch', 'Nintendo', '3DS',
    'Nintendo 3DS']
    return render_template('landing_pages/html/carrinho.html', sugestions=sugestions)

#-----------------------------------<Fórum>------------------------------------#
@app.route('/forum', methods = ['GET', 'POST'])
def forum():
    sugestions = ['salve', 'aoba', 'teste1']
    threads = forum_methods.Get_threads()
    #Elementos que podem ser enviados ao banco de dados:
        #Perguntas (Título) - OK
        #Perguntas (Explicação) - OK
        #Respostas - OK
        #Estado do 'post'/pergunta(aberto, encerrado) - OK
        #Usuários que publicaram perguntas e respostas- OK

        #verificar autorização do usuário (se pode postar ou responder)- OK
        #Usar o current_user.is_authenticated

    return render_template('landing_pages/html/forum.html', sugestions=sugestions,
    threads=threads)

# Criar threads (ou tópicos)
@app.route('/forum/criar_thread', methods =['GET','POST'])
def criar_thread():
    sugestions = ['salve', 'aoba', 'teste1']
    if(request.method == 'POST'):
        if(request.form['concluir_ct'] == 'concluir_ct'):
            if(current_user.id != None):
                titulo = request.form['titulo']
                descricao = request.form['descricao']
                forum_methods.Criar_thread(current_user.id, titulo, descricao)
                flash('Thread criada!')
                #ver de redirecionar já pra página da thread
                return redirect(url_for('forum'))
            else:
                flash('Faça login para poder abrir threads!')
                return redirect(url_for('forum'))
    return render_template('landing_pages/html/criar_thread.html',sugestions=sugestions)

# Deletar threads
@app.route('/forum/delete_comment/<string:num_thread>/<string:thread_escolhida>/<string:num_post>', methods =['POST'])
def delete_comment(num_thread, thread_escolhida, num_post):
    forum_methods.Excluir_comment(num_thread, num_post)
    return redirect(url_for('forum_thread',thread_escolhida=thread_escolhida, num_thread=num_thread))

# Link das threads em específico
@app.route('/forum/<string:num_thread>/<string:thread_escolhida>', methods = ['GET', 'POST'])
def forum_thread(num_thread, thread_escolhida):
    # thread será um modelo básico, que será completado com os dados do fórum,
    # de acordo com os arquivos js (ou json)

    try:
        #Se digitar o título(thread_escolhida) errado
        if(forum_methods.Get_threads()[num_thread]["Thread_OP"]["Thread.title"] == thread_escolhida):

            sugestions = ['1', '2', 'teste1']
            comments = forum_methods.Get_threads()#{"Threads": {'1':{}}}

            if(request.method == 'POST'):
                if(current_user.id != None):
                #Para o criador do tópico (e posteriomente, algum ADM)
                    #Fechar thread
                    if(request.form.get('fechar_thread', 'None') == "Fechado"):
                        forum_methods.Editar_dado(num_thread, 'Thread.status', request.form['fechar_thread'])

                    #Reabrir thread
                    elif(request.form.get('fechar_thread', 'None') == "Aberto"):
                        forum_methods.Editar_dado(num_thread, 'Thread.status', request.form['fechar_thread'])

                    #Excluir thread
                    elif(request.form.get('excluir_thread', 'None') == 'excluir_thread'):
                        forum_methods.Excluir_thread(num_thread)
                        return redirect(url_for('forum'))

                    # #Excluir comentário

                    #Pensar numa maneira mais eficiente de fazer isso
                    #atualmente, está fazendo pela rota delete_comment

                    # elif(request.form.get('excluir', 'None') == 'excluir_comentário'):
                    #     forum_methods.Excluir_comment(request.form['excluir'])

                #Para todos os usuários logados
                    #Comentar
                    elif(request.form.get('comentar', 'None') == 'comentar'):
                        print('comentou')
                        comentario = request.form['comentario']
                        forum_methods.Comentar(current_user.id, comentario, num_thread)
                        flash('Comentário enviado!')
                        #ver de redirecionar já pra página da thread
                        comments = forum_methods.Get_threads()

                    return redirect(url_for('forum_thread',thread_escolhida=thread_escolhida, num_thread=num_thread))
                else:
                    flash('Faça login para poder comentar!')
                    return redirect(url_for('forum'))


            return render_template('landing_pages/html/thread.html',sugestions=sugestions,
            thread=thread_escolhida, num_thread=num_thread, comments=comments)
        #Tópico existe, mas o titulo foi digitado errado: erro 404
        else:
            return render_template('landing_pages/html/page_error_forum.html', status_code='Página não encontrada',
             complete_status= f'404 - Página não encontrada', detalhamento='O link pode ter sido digitado errado')


    #Garantia de que vai dar erro 404 se o link estiver errado
    except jinja2.exceptions.UndefinedError:
          return abort(404)

    #Se digitar o número da thread (num_thread) errado: erro 410
    except KeyError:
         return render_template('landing_pages/html/page_error_forum.html', status_code='410',
         complete_status= f'410 - Página não existe', detalhamento='O tópico procurado pode ter sido excluido')


#------------------------------------<Conta>-----------------------------------#
@app.route('/conta', methods = ['POST', 'GET'])
# @login_required
def conta():
    if (request.method == 'POST'):
        pass


    return render_template(f'landing_pages/html/conta.html')


#
@app.route('/conta/<string:recurso>', methods = ['POST', 'GET'])
# @login_required
def conta_feature(recurso):

    if (request.method == 'POST'):
        config_args = request.form

        # for valor_legal in request.form:
        #     print(f'{valor_legal}: {request.form.get(valor_legal)}')

        #Tomar muito cuidado com o eval


        callback_eval = eval(Account().account_config(recurso))
        #,{'__builtins__': {'getattr': getattr,
        #'Banco_de_dados': Banco_de_dados,
        #'config_args':config_args}})


        # print(callback_eval)
        # print(f'Mensagem: {callback_eval["mensagem"]}')
        print(f'Redirecionamento: {callback_eval["redirecionamento"]}')
        # print('epa')
        flash(callback_eval["mensagem"])

        return callback_eval["redirecionamento"]
    else:
        callback_eval = {'mensagem':None, 'redirecionamento':None}

    return render_template(f'landing_pages/html/pag_conta/{recurso}.html', callback_eval=callback_eval)


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
# @app.route('/solicitar_post_apenas', methods = ['POST'])
def teste():

        #Teste para envio de emails

    # msg = Message(
    # subject= 'Verificação de email - Gamesplace (Teste2)',
    # recipients=[],
    # html= render_template('landing_pages/html/corpo_email.html', verify_code='1111')
    # )
    # mail.send(msg)
    # return render_template('landing_pages/html/page_error.html', status_code='???',
    # complete_status= f'??? - Só solicitações post')
    return render_template('landing_pages/html/corpo_email.html', verify_code= '1234')

#Processo para que todo o backend e estrutura do site sejam executados ao
#rodar esse arquivo python

if (__name__ == '__main__'):
    app.run(debug= True, host = "0.0.0.0")
