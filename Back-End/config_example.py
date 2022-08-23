#Arquivo de configurações do programa
# Alterar os dados de exemplo para os dados do seu banco de dados, caso queira
# simular o site (você pode inserir um banco de dados local, por exemplo).

class app_config():
    secret_key = 'inserir_chave_secreta'

    static_folder = 'static' #Inserir um caminho personalizado para a pasta de arquivos estáticos (o padrão é 'static').
    template_folder = 'templates' #Inserir um caminho personalizado para a pasta de templates (o padrão é 'templates').

#Banco de dados
class db_config():
    #Variável que indica a plataforma padrão de configuração do banco de dados
    platform="Inserir_a_plataforma(exemplo, PostgreSQL)" #MySQL está implementado
    # também, mas exige algumas modificações no código

    #Inserir o host de hospedagem do seu banco de dados
    host="Endereço_do_host"

     #Inserir o usuário de acesso ao seu banco de dados
    user="Nome_do_Usuário"

    #Inserir a senha de acesso ao seu banco de dados:
    password="Senha_de_acesso"

    #Inserir o banco de dados.
    database="Nome_do_banco_de_dados"

Config_email = {
"MAIL_SERVER": 'smtp.(provedor_do_seu_email).com',
"MAIL_PORT": 000, #(verificar o número do seu provedor de email),
"MAIL_USE_TLS": False, #Caso queira ativar o TLS, mude para True,
"MAIL_USE_SSL": True, #Caso queira desativar o SSL, mude para False,
"MAIL_USERNAME": 'seuemail_de_feedback@exemplo.com',
"MAIL_PASSWORD": 'A_senha_do_seu_email',
"MAIL_DEFAULT_SENDER": 'seuemail_de_feedback@exemplo.com' #Ou algum outro email padrão de envios.
}
