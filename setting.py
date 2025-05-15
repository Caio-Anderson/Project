import mysql.connector


def conectar_banco():
    conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="toor",
    database="teste_danca"
    )