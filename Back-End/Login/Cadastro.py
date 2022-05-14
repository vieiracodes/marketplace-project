
#Inserir Email e Senha no banco de dados
from bs4 import BeautifulSoup
import mysql.connector

comms = mysql.connector.connect(
  host="localhost",
  user="Py_auth",
  password="Py_auth",
  database="marketplace"
)
cursor = comms.cursor()
#Conexão estabelecida
# print(comms)
# print(cursor)

#Recupera os dados do input html

page_get = BeautifulSoup('front-end\index.html', 'html.parser')
print(page_get)
this = page_get.find('button', id_='prosseguir')
print(this)


#Para fins de teste:
User ='jhc3@gmail.com.br'
Senha = 'password3'
User_data = (User, Senha)
try:
#Insere os dados no MySQL por meio dos comandos
    add_User = 'INSERT INTO logins (Email, Senha) VALUES (%s, %s)'
    cursor.execute(add_User, User_data)
# print(cursor)
    comms.commit()
except:
    pass
#Ler dados de usuário no banco de dados
get_user = "SELECT Email, Senha, USER_ID FROM logins "

cursor.execute(get_user)

for (Email, Senha, USER_ID) in cursor:
  print(f'Email: {Email}')
  print(f'Senha: {Senha}')
  print(f'USER_ID = {USER_ID}')
