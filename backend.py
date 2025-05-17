import mysql.connector
from mysql.connector import Error
from settings import conectar_banco

from tabulate import tabulate
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
    print('\n<<<<<< Cadastro do Usuário >>>>>>\n')

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
        cursor.execute( 'SELECT 1 FROM tbl_usuarios WHERE username = %s OR email_usuario = %s', (username, email))
        
        
        if cursor.fetchone():
            print('Username ou e-mail já cadastrado!')
            return # Sai da função se já existir
        
        comando = '''INSERT INTO tbl_usuarios 
                     (nome_usuario,email_usuario, telefone_usuario, username, senha) 
                     VALUES (%s, %s,%s, %s, %s)'''
        

        valores = (nome,email, telefone, username, senha_usuario_hash)
        
        cursor.execute(comando, valores)
        
        
        conexao.commit()
        print('Usuário cadastrado com sucesso!\n')
        

    except mysql.connector.Error as err:
        print(f'Erro ao cadastrar o usuario {err}')
        conexao.rollback()
    
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()
     # Garante que a conexão será fechada mesmo se houver erro   

def agendamento_usuario(usuario_id):


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
        
        estilos_disponiveis = ['1 - BLACK CHARME', '2 - HIP HOP', '3 - AFRO BEAT' ]
        print(f'Estes são nossos estilos de dança disponivéis!')
        print('\n'.join(estilos_disponiveis))

        estilo_escolhido = int(input('Digite o número de dança escolhido: '))
        if estilo_escolhido in (1, 2, 3):
            estilo_agendamento = int(estilo_escolhido)
            break
        else:
            print('Estilo não disponivel. Selecione um estilo da lista')

    
    
    while True:
        dificuldades = ['1 - iniciante', '2 - intermediário', '3 - avançado']
        print('Por favor insira abaixo o nivel que você se encontra em relação a aula')
        print('\n'.join(dificuldades))

        dificuldade_escolhida = input('Digite número do seu nivel em relação a aula: ')
        if dificuldade_escolhida in ('1', '2', '3' ):
            dificuldade_id = int(dificuldade_escolhida)
            break
        else:
            print('Por favor selecione um dos niveis presentes na lista')
    

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
       
        cursor.execute( '''SELECT 1 FROM tbl_agendamentos WHERE dia = %s AND horario = %s AND usuario_id = %s''', (dia, horario, usuario_id))
        
        
        if cursor.fetchone():
            print('\nDia e hórario já cadastrado!, Se deseja agendar outra aula neste mesmo dia escolha outro horário\n')
            return
       
        cursor.execute(''' SELECT 1 FROM tbl_agendamentos WHERE dia = %s AND horario = %s''', (dia, horario))
    
        if cursor.fetchone():
         print('\nHorário já ocupado por outro aluno! Escolha outro.')
         return
 
       
        cursor.execute('''INSERT INTO tbl_agendamentos (dia, horario, usuario_id, estilo_agendamento) VALUES (%s,%s,%s, %s)''',(dia, horario, usuario_id, estilo_escolhido))
       

        cursor.execute("UPDATE tbl_usuarios SET dificuldade_id = %s WHERE id_usuario = %s",(dificuldade_id, usuario_id))

        conexao.commit()
        print(f'\nAula de {estilo_escolhido} agendada para o {dia} às {horario}')
        print(f'\nCaso tenha interesse em outro estilo de dança ou em fazer mais aulas, faça outro agendamento!. Tenha um ótimo dia e obrigado pela preferência\n')
    
    except mysql.connector.Error as err:
      print(f'Erro no agendamento{err}')
      conexao.rollback()
    
    finally:
        cursor.close()
        conexao.close()





def listar_cadastro():
    
    conexao = conectar_banco()
    if not conexao:
        return #volta pro menu de adm

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute ('''SELECT id_usuario as "ID", nome_usuario as "Nome",
                        email_usuario as "E-mail",telefone_usuario as "Telefone",
                        DATE_FORMAT(criado_em, '%%d/%%m/%%Y %%H:%%i') as "Cadastrado em" FROM tbl_usuarios''') #dateformat formata a data para o nosso padrão
        resultados = cursor.fetchall()

        if resultados:
            print('\n' + '='*60)
            print('LISTA DE CADASTROS'.center(60))
            print('='*60)

            print(tabulate(resultados, headers='keys', tablefmt= 'fancy_grid', stralign = 'center', numalign = 'center', showindex = False))
            print(f'\nTotal de Cadastros: {len(resultados)}')

        else:
         print('Nenhum cadastro registrado ou encontrado')



    except mysql.connector.Error as err:
        print(f'Erro no agendamento{err}')
        conexao.rollback()
    
    finally:
            cursor.close()
            conexao.close()





def menu_adm():

    print('Olá seja bem vindo admin!👑, O que deseja fazer hoje?')
    
    while True:
        
        print('\n1 - Listar cadastros')
        print('2 - atualizar cadastros')
        print('3 - excluir cadastros')
        print('4 - Sair e voltar para o menu principal')
        opcao = int(input('Digite o número do que deseja fazer >> '))

        if opcao == 1:
            listar_cadastro()

        elif opcao == 2:
            atualizar_cadastro()

        elif opcao == 3:
            excluir_cadastro()

        elif opcao == 4:
            return #faz com que eu volte para o menu sem precisar executa-lo novamente
            
        else:
            print('Opção inválida')







def login_usuario():

    try: 
        conexao = conectar_banco()
        cursor = conexao.cursor()

        username = input('Digite seu nome de usuário >>').lower().strip()
        senha = input('Digite sua senha >>').strip()

        cursor.execute('SELECT id_usuario, senha FROM tbl_usuarios WHERE username = %s', (username,))
        resultado = cursor.fetchone()


        if resultado:
            usuario_id, senha_hash = resultado
            if bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8')):
                print('Login bem sucedido!')
                if username == 'admin':
                    menu_adm()
            
                else:
                    agendamento_usuario(usuario_id,)
            else:
                print('Senha incorreta!')
        
        else:
            print('Usuário não encontrado')
    
    except mysql.connector.Error as err:
        print(f'Erro ao cadastrar o usuario {err}')
        conexao.rollback()

 
        

    
        cursor.close()
        conexao.close()



if __name__ == '__main__':
    print('Erro utilize o main.py para executar o código')

