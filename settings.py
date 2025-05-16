import mysql.connector


def conectar_banco():
    try:
        conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="toor",
        database="escola_danca"
    )
        return conexao
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco: {err}")
        return None 