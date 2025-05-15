from datetime import datetime
from setting import conectar_banco
import bcrypt
from mysql.connector import error

def menu():
    while True:
        print('Olá seja bem vindo a escola de dança Jabari')
        print('Para agendar uma aula precisamos fazer um cadastro primeiro, Após o cadastro execute o login para se cadastrar')
        print('\n1 - login')
        print('2 - cadastro')
        print('3 - Sair')
        opcao = int(input('Digite a opção >> '))

        if opcao == 1:
            login_usuario()

        elif opcao == 2:
            cadastro_usuario()

        elif opcao == 3:
            print('Saindo...')
            break
        else:
         print('Opção inválida')
         


def cadastro_usuario():
    print('\n<<<<<< Cadastro do Usuário >>>>>>')

    while True:
        nome = input('Digite Seu nome >>').strip()
    
        if nome:
            break
        print('Digite algo, o nome não pode ser vazio')


    telefone = input('Digite seu telefone >>').strip()

    email = input('Digite seu email >>').strip()

    while True:
        username = input('Digite o seu nome de usuário >>').strip()

        if len(username) >= 5:
            break
        print('Seu nome de usuário tem que ter ao menos 5 caracteres')


    while True:
        senha = input('Digite sua senha >>').strip()

        if len(senha) >=4:
            senha_usuario_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            break
        print('Sua senha deve ter ao menos 4 caracteres')



    conexao = None 
    cursor = None

    try:
        
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute( 'SELECT 1 FROM usuarios WHERE username = %s OR email_usuario = %s', (username, email))
        
        
        if cursor.fetchone():
            print('Username ou e-mail já cadastrado!')
            return # Sai da função se já existir
        
        comando = '''INSERT INTO usuarios 
                     (nome_usuario,email_usuario, telefone_usuario, username, senha) 
                     VALUES (%s, %s,%s, %s, %s)'''
        

        valores = (nome,email, telefone, username, senha_usuario_hash)
        
        cursor.execute(comando, valores)
        
        
        conexao.commit()
        print('Usuário cadastrado com sucesso!')
        

    except mysql.connector.Error as erro:
        print(f'Erro ao cadastrar o usuario {erro}')
        conexao.rollback()
    
    finally:
        if cursor:  
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()
     # Garante que a conexão será fechada mesmo se houver erro   


