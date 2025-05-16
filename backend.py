import mysql.connector
from mysql.connector import Error
from settings import conectar_banco

import bcrypt
from datetime import datetime, date, time

def menu():
    while True:
        print('Olá seja bem vindo a escola de dança Jabari')
        print('Para agendar uma aula precisamos fazer um cadastro primeiro, Após o cadastro execute o login para agendar sua aula')
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
        username = input('Digite o seu nome de usuário >>').strip().lower()

        if len(username) >= 5:
            break
        print('Seu nome de usuário tem que ter ao menos 5 caracteres')


    while True:
        senha = input('Digite sua senha >>').strip()

        if len(senha) >=4:
            senha_usuario_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            break
        print('Sua senha deve ter ao menos 4 caracteres')



    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
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
        

    except mysql.connector.Error as err:
        print(f'Erro ao cadastrar o usuario {err}')
        conexao.rollback()
    
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()
     # Garante que a conexão será fechada mesmo se houver erro   

def agendamento_usuario():

    print('\n<<<<<<<Seja bem-vindo ao agendamento da escola Jabari>>>>>>')
    print('\nEscolha a seguir o dia, horário, estilo de dança e seu grau de experiência com o estilo')

    while True:
        dia = input('Digite o dia desejado (YYYY-MM-DD) >> ') 
        try:
            data_aula = datetime.strptime(dia, '%Y-%m-%d').date()

            dia_aula = data_aula.day
            mes_aula =  data_aula.month
            ano_aula = data_aula.year

            data_atual = datetime.now().date()

            aula_valida = (
                (ano_aula > data_atual.year) or
                (ano_aula == data_atual.year and mes_aula > data_atual.month) or
                (ano_aula == data_atual.year and mes_aula == data_atual.month and dia_aula >= data_atual.day )
            )
            if aula_valida:
                break
            else:
                print('Data inválida ou já passou. Digite uma data futura e Use YYYY-MM-DD')
        except ValueError:
            print('Formato inválido. Use YYYY-MM-DD(ex 2025-05-24.)')

    
    """"
    try:
       
       conexao = conectar_banco()
       cursor = conexao.cursor()
       
       cursor.execute( 'SELECT 1 FROM agendamentos WHERE dia = %s and horario = %s', (dia, horario))
        
        
       if cursor.fetchone():
        print('Dia e hórario já cadastrado!, Se deseja agendar outra aula neste mesmo dia escolha outro horário')
        return
       """


    
    
    
    while True:
        horario = input('Digite o horário desejado (no formato (HH:MM)): ')
        try:
            hora_aula = datetime.strptime(horario, "%H:%M").time()
            hora_inicio = time(8,0)
            hora_fim = time(17,0)
            
            if hora_inicio <=hora_aula <=hora_fim:
               
               break
            else:
                print('Horario invalido. Escolha entre 08:00 e 17:00.')
        except:
            print('Formato invalido. Use HH:MM (ex:10:40).')

   
    
    
    while True:
        estilos_disponiveis = ['HIP HOP', 'BLACK CHARME', 'AFRO BEAT' ]
        print(f'Estes são nossos estilos de dança disponivéis!')
        print('\n'.join(estilos_disponiveis))

        estilo_escolhido = input('Digite o estilo de dança escolhido: ').strip().upper()
        if estilo_escolhido in estilos_disponiveis:
            print(f'Você escolheu o estilo {estilo_escolhido}')
            break
        else:
            print('Estilo não disponivel. Selecione um estilo da lista')
        
    print(f'\nAula de {estilo_escolhido} agendada para o {dia} às {horario}')
    print(f'\nCaso tenha interesse em outro estilo de dança ou em fazer mais aulas, faça outro agendamento!. Tenha um ótimo dia e obrigado pela preferência\n')



def login_usuario():
    
    conexao = conectar_banco()
    cursor = conexao.cursor()

    username = input('Digite seu nome de usuário >>').lower().strip()
    senha = input('Digite sua senha >>').strip()

    cursor.execute('SELECT senha FROM usuarios WHERE username = %s',(username,))
    comando = cursor.fetchone()

    if comando and bcrypt.checkpw(senha.encode('utf-8'), comando[0].encode('utf-8')):
        print('Login bem sucedido!')
        agendamento_usuario()
    
    elif username == 'Admin':
        menu_adm()

    else:
        print('Senha ou Usuario incorretos!')
        

    
    cursor.close()
    conexao.close()



