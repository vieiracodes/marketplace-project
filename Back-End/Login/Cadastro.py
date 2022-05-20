

#-------------------------------<Configurações>--------------------------------#
#O python atuará como um programa serverside
from flask import Flask, request
from flask import redirect, url_for, render_template
import psycopg2
# import mysql.connector #comunicação com o banco de dados
# from mysql.connector import errors

#Importação de variáveis de ambiente e outras configurações, caso necessário



#Criação de uma instância do Flask
app = Flask(__name__)


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
    #Para PostgreSQL (Usado na plataforma Heroku)
    elif(platform == 'PostgreSQL'):
        comms = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="Pi3!4159",
            database="postgres"
        )

    return comms



#--------------------------------<Autenticação>--------------------------------#

#Função da página de cadastro
@app.route('/cadastro', methods = ['POST'])
def cadastro():
    comms = conectar_banco()
    cursor = comms.cursor()
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
        #return redirect(url_for('teste', User=User, Senha=Senha))
        return f'Cadastro feito Bem vindo, {User}. Sua senha {Senha}'

    # except mysql.connector.errors.IntegrityError:
    #     return 'Usuário já existe! Tente outro email'
    #
    # except mysql.connector.errors.OperationalError:
    #     return f'Erro no servidor: {User} e {Senha}'

    except psycopg2.errors.UniqueViolation:
            return f'Usuário já existe! Tente outro email'

    finally:
        #encerra a comunicação com o banco de dados independente do resultado
        comms.close()


#Ler dados de usuário no banco de dados
@app.route('/login', methods = ['POST'])
def login():
    comms = conectar_banco()
    cursor = comms.cursor()
    if(request.method == 'POST'):
        User = request.form['email']
        Senha = request.form['password']
        #verificar se o login e senha estão no banco de dados
        get_user = f"""SELECT Email, Senha FROM logins
         WHERE Email = '{User}' AND Senha = '{Senha}'"""

        try:
            cursor.execute(get_user)
            Auth_tokens = cursor.fetchone()
            #print(Auth_tokens)
            #se os valores existirem, são retornados
            return f"""<h2> Usuário: {Auth_tokens[0]} </h2>
             <h2> Senha: {Auth_tokens[1]}</h2>"""

        #se não existirem (TypeError pois retorna um Nonetype)
        except TypeError:

            #retorna a mensagem abaixo
            return 'Usuário não encontrado'

        #encerra a comunicação com o banco de dados independente do resultado
        finally:

            comms.close()



#--------------------------------<Marketplace>---------------------------------#
@app.route('/', methods = ['POST'])
def market():
    #comms = conectar_banco()
    #cursor = comms.cursor()
        #Elementos que podem ser enviados ao banco de dados:
            #Produto (Título)
            #Preço
            #Fotos (Caminho das imagens, talvez)
            #Estado do anúncio (aberto, encerrado)

    return 'Página do Marketplace: Não implementada ainda'

#-----------------------------------<Fórum>------------------------------------#
@app.route('/forum', methods = ['POST'])
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
    get_user = "SELECT Email, Senha FROM logins"
    cursor.execute(get_user)
    for(Email, Senha) in cursor:
        email_list.append(Email)
        senhas_list.append(Senha)
    comms.commit()
    return lista_banco



#fins de teste
#OBS:Ele passa os parâmetros pela Url
@app.route('/teste', methods = ['POST', 'GET'])
def teste():
    comms = conectar_banco()
    cursor = comms.cursor()
    # return f'User {User} e Senha {Senha}'
    #try:
    if(request.method == 'POST'):# or request.method == 'GET'):
        #print(request.form('User'))
        return render_template('index.html',
         User_HTML = request.form('User'),
         Senha_HTML = request.form('Senha'))
    else:
        return render_template('index.html', User_HTML = 'Usuário', Senha_HTML = 'Senha')








#Processo para que o aplicativo seja exportado e executado ao clicar no botão HTMl

if (__name__ == '__main__'):
    app.run(debug= True)
