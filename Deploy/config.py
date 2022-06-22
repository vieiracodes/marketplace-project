#Arquivo de configurações do programa

class app_config():
    secret_key = 'insert_secret_key'
    static_folder = 'static'
    template_folder = 'templates'

#Banco de dados
class db_config():
    #Variável que indica a plataforma padrão de configuração do banco de dados
    platform="PostgreSQL"
    #Inserir o host de hospedagem do seu banco de dados
    host="ec2-52-3-2-245.compute-1.amazonaws.com"
     #Inserir o usuário de acesso ao seu banco de dados
    user="ojkcyslsolzjxw"
    #Inserir a senha de acesso ao seu banco de dados:
    password="de7fdc90c23fbfa7c949ff0b22cb8c55f8e7130c249da36863a9818fb07871f9"
    #Inserir o banco de dados.
    database="de7bgah134l4lf"

Config_email = {
"MAIL_SERVER": 'smtp.gmail.com',
"MAIL_PORT": 465,
"MAIL_USE_TLS": False,
"MAIL_USE_SSL": True,
"MAIL_USERNAME": 'emailverify.gamesplace@gmail.com',
"MAIL_PASSWORD": 'ocfqpzwspsaypngi',
"MAIL_DEFAULT_SENDER": 'emailverify.gamesplace@gmail.com'
}
