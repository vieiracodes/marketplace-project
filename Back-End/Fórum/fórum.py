#Gerenciar posts e respostas no banco de dados

#O python atuará como um programa serverside
from flask import Flask, request
from flask import redirect, url_for, render_template #Manipulação de URL e HTML
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


#CÓDIGO

#Processo para que o aplicativo seja exportado e executado ao clicar no botão HTMl

if (__name__ == '__main__'):
    app.run(debug= True)
