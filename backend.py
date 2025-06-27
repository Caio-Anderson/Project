import mysql.connector
from mysql.connector import Error
from settings import conectar_banco

import re
import bcrypt
import os
import sys
import time as tm
from rich import print
from tabulate import tabulate
from datetime import datetime, date, time


def limpar_tela ():

      if os.name == 'nt':
        os.system('cls')
       
        os.system('echo off && cls')
   
      else:
          os.system('printf "\033c\033[3J"')  
    
      sys.stdout.flush()
      tm.sleep(0.2) 
      print("\n" * 3)

def menu():


    while True:

        limpar_tela()

        logo = '''

     ██╗ █████╗ ██████╗  █████╗ ██████╗ ██╗
     ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗██║
     ██║███████║██████╔╝███████║██████╔╝██║
██   ██║██╔══██║██╔══██╗██╔══██║██╔══██╗██║
╚█████╔╝██║  ██║██████╔╝██║  ██║██║  ██║██║
 ╚════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
                                           
'''
        print(logo)
    
        
        print('Olá seja bem vindo a escola de dança Jabari')
        print('Para agendar uma aula precisamos fazer um cadastro primeiro, Após o cadastro execute o login para agendar sua aula')
        print('\n1 - login 🔒')
        print('2 - cadastro 🖋️')
        print('3 - Sair 👋')

        try:

            opcao = int(input('Digite a opção >> '))
            
            if opcao == 1:
                login_usuario()

            elif opcao == 2:
                cadastro_usuario()

            elif opcao == 3:
                limpar_tela()
                print('Saindo...')
                break
            else:
                print('Opção inválida ❌')
        
        except ValueError:
            print('Digite apenas números!')

    
def cadastro_usuario():

    limpar_tela()

    print('\n<<<<<< Cadastro do Usuário >>>>>>\n')

    while True:

            nome = str(input('Digite Seu nome >>')).strip()
    
            if not re.fullmatch(r'^[A-Za-zÀ-ÿ\s]+$', nome):
                print('Digite apenas caracteres!, não insira números, e também não deixe vazio!')
            
            elif re.fullmatch(r'^[A-Za-zÀ-ÿ\s]+$', nome):
                break
            

    while True:

        telefone = input('Digite seu telefone >>').strip()

        if len(telefone) == 11 and telefone.isdigit():
            break
        print('Seu telefone precisa dos 11 digitos, não insira espaços ou o -')

    while True:
        
        email = input('Digite seu email >>').strip()

        if re.fullmatch(r'^[\w\.-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$', email):
            break
        
        else:
            print('Email inválido! ou erro de digitação, digite novamente')



    while True:
        
        username = input('Digite o seu nome de usuário >>').strip().lower()

        if len(username) >= 5:
            break
        print('Seu nome de usuário tem que ter ao menos 5 caracteres!')


    while True:
        senha = input('Digite sua senha >>').strip()

        if len(senha) >=4:
            senha_usuario_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            break
        print('Sua senha deve ter ao menos 4 caracteres!')



    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        cursor.execute( 'SELECT 1 FROM tbl_usuarios WHERE username = %s OR email_usuario = %s', (username, email))
        
        
        if cursor.fetchone():
            print('Username ou e-mail já cadastrado! ❌')
            return 
        
        comando = '''INSERT INTO tbl_usuarios 
                     (nome_usuario,email_usuario, telefone_usuario, username, senha) 
                     VALUES (%s, %s,%s, %s, %s)'''
        

        valores = (nome,email, telefone, username, senha_usuario_hash)
        
        cursor.execute(comando, valores)
        
        
        conexao.commit()
        print('\nUsuário cadastrado com sucesso!✔️\n')
        

    except mysql.connector.Error as err:
        print(f'Erro ao cadastrar o usuario ❌ {err}')
        input('\nPressione Enter para continuar...')
        conexao.rollback()
    
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()
      

def agendamento_usuario(usuario_id):

    limpar_tela()


    print('\n<<<<<<<Seja bem-vindo ao agendamento da escola Jabari>>>>>>\n')
    print('\nEscolha a seguir o dia, horário, estilo de dança, seu grau de experiência com o estilo e o professor!')

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
        
        except ValueError:
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
    

    while True:
        

        try:
            conexao = conectar_banco()
            cursor = conexao.cursor(dictionary=True)

            cursor.execute('''SELECT tbl_professores.id_professor as 'ID', tbl_professores.nome_professor as 'Professor', tbl_estilos.nome_estilo as 'Estilo' 
                           FROM tbl_professores JOIN tbl_estilos ON tbl_professores.professor_estilo = tbl_estilos.id_estilo WHERE tbl_professores.professor_estilo = %s
                           ''',(estilo_escolhido,))
            resultados = cursor.fetchall()

            if not resultados:
                print('Nenhum cadastro registrado ou encontrado')
                input('Aperte enter para voltar....')
                return

            if resultados:
             print('\n' + '='*60)
             print('📝LISTA DE PROFESSORES'.center(60))
             print('='*60)

             print(tabulate(resultados, headers='keys', tablefmt= 'fancy_grid', stralign = 'center', numalign = 'center', showindex = False))
             print(f'\nTotal de Cadastros: {len(resultados)}')

            
            ids_validos = [str(prof['ID']) for prof in resultados]

            while True:
                try:
                     professor_id = input('Digite o número do ID do professor que deseja fazer a aula (caso deseje desistir do agendamento digite 0) >> ')
                
                     if professor_id == '0':
                        return
                
                     if professor_id not in ids_validos:
                        print('ID errado! selecione um da lista')
                        continue
                
                     break

                except (ValueError, IndexError):
                    print('Insira apenas números!')   
            
            professor_id = int(professor_id)
            break   

        except mysql.connector.Error as err:
            print(f'Erro ao procurar{err}')
            input('\nPressione Enter para continuar...')

        


    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
       
        cursor.execute( '''SELECT 1 FROM tbl_agendamentos WHERE dia = %s AND horario = %s AND usuario_id = %s ''', (dia, horario, usuario_id))
        
        
        if cursor.fetchone():
            print('\nDia e hórario já cadastrado!, Se deseja agendar outra aula neste mesmo dia escolha outro horário\n')
            return
       

        cursor.execute('''SELECT COUNT(*) FROM tbl_agendamentos WHERE professor_id = %s AND dia = %s AND horario = %s''', (professor_id, dia, horario))
        agendamentos_existente = cursor.fetchone()[0]
        
        aula_coletiva = agendamentos_existente > 0

        if not aula_coletiva:
            
            cursor.execute('''INSERT INTO tbl_agendamentos (dia, horario, usuario_id, estilo_agendamento,professor_id,aula_coletiva) VALUES (%s,%s,%s, %s,%s,%s)''',(dia, horario, usuario_id, estilo_escolhido,professor_id,aula_coletiva))
            
        
        else:
            cursor.execute('UPDATE tbl_agendamentos SET aula_coletiva = 1 WHERE aula_coletiva = 0')
            cursor.execute('''INSERT INTO tbl_agendamentos (dia, horario, usuario_id, estilo_agendamento,professor_id,aula_coletiva) VALUES (%s,%s,%s, %s,%s,%s)''',(dia, horario, usuario_id, estilo_escolhido,professor_id,aula_coletiva))
            
            

        cursor.execute('UPDATE tbl_usuarios SET dificuldade_id = %s WHERE id_usuario = %s',(dificuldade_id, usuario_id))

        conexao.commit()
        print(f'\nAula de {estilo_escolhido} agendada para o {dia} às {horario} 😄\n')
        print(f'\nCaso tenha interesse em outro estilo de dança ou em fazer mais aulas, faça outro agendamento!. Tenha um ótimo dia e obrigado pela preferência 😃\n')
        input('Digite enter para continuar....')

    except mysql.connector.Error as err:
      print(f'Erro no agendamento{err}')
      input('\nPressione Enter para continuar...')
      conexao.rollback()
    
    finally:
        cursor.close()
        conexao.close()





def listar_usuario():

    limpar_tela()
    
    conexao = conectar_banco()
    if not conexao:
        return 

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute ('''SELECT id_usuario as "ID", nome_usuario as "Nome",
                        email_usuario as "E-mail",telefone_usuario as "Telefone",
                        DATE_FORMAT(criado_em, '%d/%m/%Y %H:%i') as "Cadastrado em", DATE_FORMAT(atualizado_em, '%d/%m/%Y %H:%i') as 
                        'Atualizado em',tipo_usuario as 'tipo' FROM tbl_usuarios''') #dateformat formata a data para o nosso padrão
        resultados = cursor.fetchall()

        if resultados:
            
            print('📝LISTA DE CADASTROS'.center(100))

            print(tabulate(resultados, headers='keys', tablefmt= 'simple_grid', stralign = 'center', numalign = 'center', showindex = False))
            print(f'\nTotal de Cadastros: {len(resultados)}')
            input('\nPressione Enter para continuar...')
            limpar_tela()
            return
        else:
         print('Nenhum cadastro registrado ou encontrado')



    except mysql.connector.Error as err:
        print(f'Erro❌{err}')
        input('\nPressione Enter para continuar...')
        conexao.rollback()
    
    finally:
            cursor.close()
            conexao.close()


def listar_professor():
    
    limpar_tela()
    conexao = conectar_banco()

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute ('''SELECT id_professor as "ID", nome_professor as "Professor",
                        email_professor as "E-mail",telefone_professor as "Telefone"
                        FROM tbl_professores''')
        resultados = cursor.fetchall()

        if resultados:
            
            print('📝LISTA DE PROFESSORES'.center(60))
            print(tabulate(resultados, headers='keys', tablefmt= 'simple_grid', stralign = 'center', numalign = 'center', showindex = False))
            print(f'\nTotal de Cadastros: {len(resultados)}')

        else:
         print('Nenhum cadastro registrado ou encontrado')



    except mysql.connector.Error as err:
        print(f'Erro❌ {err}')
        input('\nPressione Enter para continuar...')
        conexao.rollback()
    
    finally:
            cursor.close()
            conexao.close()


def atualizar_cadastro_aluno():

    limpar_tela()
    listar_usuario()
    
    while True:
        try: 
            
            usuario_id = input('Digite o ID do usuário que deseja atualizar os dados caso deseje voltar, digite (voltar) >> ')

            if usuario_id == 'voltar':
                return

            elif usuario_id and usuario_id.isdigit():
                break

        except (ValueError, IndexError):
            print('Digite apenas números!')
            

    conexao  = conectar_banco()
    if not conexao:
        return
    
    try:
        cursor = conexao.cursor(dictionary=True)

        cursor.execute('SELECT tbl_usuarios.id_usuario, tbl_usuarios.nome_usuario, tbl_usuarios.email_usuario, tbl_usuarios.telefone_usuario FROM tbl_usuarios WHERE id_usuario = %s', (usuario_id,))
        usuario = cursor.fetchone()

        if not usuario:
            print('Usuário não encontrado!❌')
            return

        print('\nDados Atuais')
        print(tabulate([usuario], headers='keys', tablefmt= 'fancy_grid'))
    
        print('\nCampos disponivéis para alteração: ')

        campos = {'1': ('nome_usuario', 'nome'), '2': ('email_usuario', 'email'), '3': ('telefone_usuario', 'Telefone')} #dicionario para armazenar meus campos de alteração
    
        for key, (coluna_transformacao, transformacao) in campos.items(): #a key é o número que eu atribui dentro da variavel campos
            print(f'{key} - {transformacao}')  #o número 1 é para ele pegar dentro do dicionario, o texto para exibir para o usuario se fosse 0 mostraria o campo do banco de dados


        campo_escolhido = input('\nDigite o número do campo que deseja atualizar >>  ')
        

        if not campo_escolhido in campos:
            print('Campo inexistente ou erro de digitação')
            return

        transformacao = campos[campo_escolhido][1] #olha o dicionario e procura o nome do campo que esta dentro do mysql
        atualizacao = input(f'Digite o novo {transformacao} >> ') #faz com que a função campos receba o número no campo escolhido e busque no dicionario o nome do campo


        coluna_transformacao = campos[campo_escolhido][0]

        if coluna_transformacao not in ('nome_usuario', 'email_usuario', 'telefone_usuario'):
            raise ValueError('Tentativa negada')
        
        comando = "UPDATE tbl_usuarios   SET  `{}` = %s WHERE id_usuario = %s".format(coluna_transformacao)    
        cursor.execute(comando, (atualizacao, usuario_id))
        
        conexao.commit()
        print('\nDados atualizados com sucesso!')

    
    except mysql.connector.Error as err:
        print(f'Erro na atualização{err}')
        conexao.rollback()
    
    finally:
            cursor.close()
            conexao.close()


def atualizar_cadastro_professor():


    
    listar_professor()
    
    while True:
        
        try: 
            
            professor_id = input('Digite o ID do usuário que deseja atualizar os dados caso deseje voltar, digite (voltar) >> ')

            if professor_id == 'voltar':
                return

            elif professor_id and professor_id.isdigit():
                break

        except (ValueError, IndexError):
            print('Digite apenas números!')
            

    conexao  = conectar_banco()
    
    if not conexao:
        return
    
    try:
        cursor = conexao.cursor(dictionary=True)

        cursor.execute('''SELECT tbl_professores.id_professor, tbl_professores.nome_professor, 
                       tbl_professores.telefone_professor, tbl_professores.email_professor FROM tbl_professores WHERE id_professor = %s''', (professor_id,))
        professor = cursor.fetchone()

        if not professor:
            print('professor não encontrado!❌')
            return

        print('\nDados Atuais')
        print(tabulate([professor], headers='keys', tablefmt= 'fancy_grid'))
    
        print('\nCampos disponivéis para alteração: ')

        campos = {'1': ('nome_professor', 'nome'), '2': ('email_professor', 'email'), '3': ('telefone_professor', 'Telefone')} #dicionario para armazenar meus campos de alteração
    
        for key, (coluna_transformacao, transformacao) in campos.items(): #a key é o número que eu atribui dentro da variavel campos
            print(f'{key} - {transformacao}')  #o número 1 é para ele pegar dentro do dicionario, o texto para exibir para o usuario se fosse 0 mostraria o campo do banco de dados


        campo_escolhido = input('\nDigite o número do campo que deseja atualizar >>  ')

        if not campo_escolhido in campos:
            print('Campo inexistente ou erro de digitação')
            return

        transformacao = campos[campo_escolhido][1] #olha o dicionario e procura o nome do campo que esta dentro do mysql
        atualizacao = input(f'Digite o novo {transformacao} >> ') #faz com que a função campos receba o número no campo escolhido e busque no dicionario o nome do campo


        coluna_transformacao = campos[campo_escolhido][0]

        if coluna_transformacao not in ('nome_professor', 'email_professor', 'telefone_professor'):
            raise ValueError('Tentativa negada')
        
        comando = "UPDATE tbl_professores   SET  `{}` = %s WHERE id_professor = %s".format(coluna_transformacao)    
        cursor.execute(comando, (atualizacao, professor_id))
        
        conexao.commit()
        print('\nDados atualizados com sucesso!')

    
    except mysql.connector.Error as err:
        print(f'Erro na atualização{err}')
        conexao.rollback()
    
    finally:
            cursor.close()
            conexao.close()


def atualizar_cadastro():

    
    while True:
     
     limpar_tela()
     
     try:

        opcao = int(input('Digite o número de quem você gostaria de atualizar (1 - alunos, 2 - professores, 3 - voltar) >> '))

        if opcao == 1:
            atualizar_cadastro_aluno()

        elif opcao == 2:
            atualizar_cadastro_professor()

        elif opcao == 3:
            return
        
        else:
            print('Opção inválida!')
            input('\nAperte enter para tentar denovo.....')


     except (ValueError, IndexError):
        print('Digite apenas números')
        input('\nAperte enter para tentar denovo.....')



def excluir_cadastro_aluno():

    listar_usuario()

    while True:

        try:
            usuario_id = int(input('Digite o id do usuario que gostaria de deletar >> '))

            if usuario_id:
                break

        except (ValueError, IndexError):
            print('\nDigite apenas números!\n')
            input('\nAperte enter para tentar denovo....')

        
    
    
    confirmacao = input('Deseja realmente deletar este usuario? se sim digite:(sim) se não digit (não) >> ').lower().strip()
    
    if confirmacao == 'não':
        print('Deleção cancelada ✔️')
        return
    

    conexao = conectar_banco()
    if not conexao:
        return
    
    try:
        
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM tbl_usuarios WHERE id_usuario = %s',(usuario_id,))

        if cursor.rowcount >0:
            conexao.commit()
            print('\nUsuário deletado com sucesso')
        
        else:
            print('Nenhum usuário deletado, ou id não foi encotrado')
    

         
    except mysql.connector.Error as err:
        print(f'Erro na deleção{err}')
        input('\nPressione Enter para continuar...')
        conexao.rollback()
    
    finally:
            cursor.close()
            conexao.close()



def excluir_cadastro_professor():

    listar_professor()
    while True:

        try:
            professor_id = int(input('Digite o id do usuario que gostaria de deletar >> '))

            if professor_id:
                break

        except (ValueError, IndexError):
            print('\nDigite apenas números!\n')
            input('\nAperte enter para tentar denovo....')

        
    
    
    confirmacao = input('Deseja realmente deletar este usuario? se sim digite:(sim) se não digit (não) >> ').lower().strip()
    
    if confirmacao == 'não':
        print('Deleção cancelada ✔️')
        return
    

    conexao = conectar_banco()
    if not conexao:
        return
    
    try:
        
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM tbl_professores WHERE id_professor = %s',(professor_id,))

        if cursor.rowcount >0:
            conexao.commit()
            print('\nProfessor deletado com sucesso')
        
        else:
            print('Nenhum professor deletado, ou id não foi encotrado')
    

         
    except mysql.connector.Error as err:
        print(f'Erro na deleção{err}')
        input('\nPressione Enter para continuar...')
        conexao.rollback()
    
    finally:
            cursor.close()
            conexao.close()



def excluir_cadastro():
    
    limpar_tela()

    while True:
       
        try:
            
            opcao = int(input('Digite quem você deseja excluir (1 - aluno, 2 - professor ou 3 - voltar)>> '))

            if opcao == 1:
                excluir_cadastro_aluno()


            elif opcao == 2:
                excluir_cadastro_professor()
            
            elif opcao ==3:
                return

            else:
                print('Opção invalida!')
                input('\nAperte enter para tentar denovo....')
        
        
        except (ValueError, IndexError):
            print('\nDigite apenas números!')
            input('\nAperte enter para tentar denovo....')
    



def adicionar_professor():
   
    limpar_tela()
    listar_usuario()

    while True:
        try:

            professor_id = (input('Digite o ID do usuário que ira ser professor (caso queira voltar digite (voltar))>> '))
            
            if professor_id == 'voltar':
                return

            elif professor_id and professor_id.isdigit():
                break

        except ValueError:
            print('Digite apenas números!')

        except IndexError:
            print('Digite apenas números!')

    while True:
        
        try:

            especialidade = int(input('Digite a especialidade dele(1 - BLACK CHARME, 2 - HIP HOP, 3 - AFRO BEAT)>> '))
            
            if especialidade:
                break

        except ValueError:
            print('Digite apenas números!')

        except IndexError:
            print('Digite apenas números!')


    
    conexao = conectar_banco()

    try:

            cursor = conexao.cursor(dictionary=True)


            cursor.execute('''SELECT nome_usuario, email_usuario, telefone_usuario FROM tbl_usuarios WHERE id_usuario = %s ''',(professor_id,))
            professor = cursor.fetchone()

            if not professor:
             print('Usuário não encontrado!')
             return
    
        
            cursor.execute(''' UPDATE tbl_usuarios SET tipo_usuario = 'professor' WHERE id_usuario = %s''',(professor_id,))

            cursor.execute('''INSERT INTO tbl_professores (id_usuario_professor,nome_professor,telefone_professor,email_professor,professor_estilo) VALUES (%s,%s, %s, %s, %s)''', 
                        (professor_id,professor['nome_usuario'], professor['telefone_usuario'], professor['email_usuario'], especialidade))
        
            conexao.commit()
            print(f'\nProfessor {professor['nome_usuario']} adicionado com sucesso!\n')
            input('Aperte enter para continuar!')
    
    except mysql.connector.Error as err:
        print(f'Erro{err}')
        input('\nPressione Enter para continuar...')
        conexao.rollback()
    
    finally:
            cursor.close()
            conexao.close()

        

def visualizar_aula(professor_id):

    limpar_tela()

    try:

        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute('''SELECT DATE_FORMAT(dia, '%d/%m/%Y')AS 'Dia', TIME_FORMAT(horario, '%H:%i') as 'Horário', IF (aula_coletiva = 1, 'Sim', 'Não')as `Aula coletiva` FROM tbl_agendamentos
                        WHERE professor_id = %s''',(professor_id,))
        resultados = cursor.fetchall()

        if resultados:
           
            print('📝LISTA DE AGENDAMENTOS'.center(45))
           

            print(tabulate(resultados, headers='keys', tablefmt= 'fancy_grid', stralign = 'center', numalign = 'center', showindex = False))
            print(f'\nTotal de agendamentos: {len(resultados)}')
            input('Aperte enter para continuar....')
            
           

        else:
         print('Nenhum agendamento registrado ou encontrado')
         input('Aperte enter para voltar....')

    
    except mysql.connector.Error as err:
        print(f'Erro ao selecionar os agendamentos{err}')
        input('Aperte enter para voltar....')

        cursor.close()
        conexao.close()


def visualizar_aluno(professor_id):
    
    limpar_tela()


    visualizar_aula(professor_id)
            
            
    
    while True:
            
            print('Digite o dia e horario da aula que gostaria de ver!')

            dia = input('Digite o dia desejado (YYYY-MM-DD) >> ') 
        
            try:
                
                data_aula = datetime.strptime(dia, '%Y-%m-%d').date()
                
                if data_aula:
                    break

            except ValueError:
                print('Formato invalido!, use YYYY-MM-DD por favor')


    while True:

            horario = input('Digite o horario desejado (HH:MM) >> ') 
        
            try:
                
                hora_aula = datetime.strptime(horario, "%H:%M").time()
                
                if hora_aula:
                    break

            except ValueError:
                print('Formato invalido!, use (HH:MM) por favor')
        
        
        
    try: 
        conexao = conectar_banco()
        cursor = conexao.cursor()   

        cursor.execute('''SELECT tbl_usuarios.nome_usuario as 'nomes'
                        FROM tbl_agendamentos JOIN tbl_usuarios ON tbl_agendamentos.usuario_id = tbl_usuarios.id_usuario WHERE dia = %s AND horario = %s ''',(dia, horario))
        resultados = cursor.fetchall()

        if resultados:
           
            print('📝LISTA DE NOMES'.center(60))
            

            print(tabulate(resultados, headers='keys', tablefmt= 'fancy_grid', stralign = 'center', numalign = 'center', showindex = False))
            print(f'\nTotal de alunos agendados: {len(resultados)}')
            input('Digite enter para continuar.....')
            limpar_tela()
            return
            
            

        else:
         print('Nenhum agendamento registrado ou encontrado')
         input('Aperte enter para voltar....')

    except mysql.connector.Error as err:
        print(f'Erro ao selecionar os agendamentos{err}')
        input('Aperte enter para voltar....')

        cursor.close()
        conexao.close()



def gerenciar_aulas(professor_id):

    limpar_tela()
    
    try:
            
        while True:  
                
                limpar_tela()            

                print('O que deseja fazer?')
                print('1 - Visualizar aulas agendadas')
                print('2 - Visualizar alunos de alguma aula')
                print('3 - Voltar') 
                
                opcao = int(input('Digite aqui o número da opção que deseja >> '))

                if opcao == 1:
                    visualizar_aula(professor_id)
                    limpar_tela()

                elif opcao == 2:
                    visualizar_aluno(professor_id)
                    limpar_tela()

                elif opcao == 3:
                    limpar_tela()
                    return

    except (ValueError, IndexError):
            print('Insira apenas números!')

    



def cancelar_aula(professor_id):

    limpar_tela()

    visualizar_aula(professor_id)


    print('Digite o dia e horário da aula que gostaria de cancelar')

    while True:

            dia = input('Digite o dia desejado (YYYY-MM-DD) >> ') 
        
            try:
                
                data_aula = datetime.strptime(dia, '%Y-%m-%d').date()
                
                if data_aula:
                    break

            except ValueError:
                print('Formato invalido!, use YYYY-MM-DD por favor')


    while True:

            horario = input('Digite o horario desejado (HH:MM) >> ') 
        
            try:
                
                hora_aula = datetime.strptime(horario, "%H:%M").time()
                
                if hora_aula:
                    break

            except ValueError:
                print('Formato invalido!, use (HH:MM) por favor')
        
            

    confirmacao = input('Deseja realmente cancelar esta aula? se sim digite:(sim) se não digite (não) >> ').lower().strip()
    

    if confirmacao == 'não':
        input('Aperte enter para voltar....')
        return
    
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()


        cursor.execute('''DELETE FROM tbl_agendamentos WHERE dia = %s AND horario = %s ''',(dia,horario))


        if cursor.rowcount >0:
            conexao.commit()
            print('\aAula Cancelada com sucesso')
        
        else:
            print('Nenhuma aula cancelada, ou id não foi encotrado')
    

         
    except mysql.connector.Error as err:
        print(f'Erro na deleção{err}')
        input('\nPressione Enter para continuar...')
        conexao.rollback()




def menu_professor(professor_id):

    limpar_tela()



    try:
            
        while True:  
                
                limpar_tela()

                print(f'Olá professor o que deseja fazer?')
                print('1 - Gerenciar aulas agendadas')
                print('2 - Cancelar aula')
                print('3 - Voltar') 
                
                opcao = int(input('Digite aqui o número da opção que deseja >> '))

                if opcao == 1:
                    gerenciar_aulas(professor_id)

                elif opcao == 2:
                    cancelar_aula(professor_id)

                elif opcao == 3:
                    return

    except (ValueError, IndexError):
            print('Insira apenas números!')


def menu_adm():
  
  
 while True:  

    limpar_tela()

    try:
       
        

        print('Olá seja bem vindo admin!👑, O que deseja fazer hoje?')
        print('\n1 - Listar cadastros 📃 ')
        print('2 - atualizar cadastros ♻️ ')
        print('3 - excluir cadastros 🗑️ ')
        print('4 - Adicionar professores 💼')
        print('5 - Listar professores 📃')
        print('6 - Sair e voltar para o menu principal')

    
       
        opcao = int(input('Digite o número do que deseja fazer >> '))

        if opcao == 1:
            limpar_tela()
            listar_usuario()
            
            
        elif opcao == 2:
            limpar_tela()
            atualizar_cadastro()

        elif opcao == 3:
            limpar_tela()
            excluir_cadastro()

        elif opcao == 4:
            limpar_tela()
            adicionar_professor()

        elif opcao == 5:
            limpar_tela()
            listar_professor()
            input('\nPressione Enter para voltar...')
            
        
        elif opcao == 6:
            limpar_tela()
            return
            
        else:
            print('Opção inválida')
            input('Pressione Enter para tentar denovo...')
    
    except (ValueError,IndexError):
        print('Digite apenas números!')



def login_usuario():

    limpar_tela()

    logo = '''

     ██╗ █████╗ ██████╗  █████╗ ██████╗ ██╗
     ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗██║
     ██║███████║██████╔╝███████║██████╔╝██║
██   ██║██╔══██║██╔══██╗██╔══██║██╔══██╗██║
╚█████╔╝██║  ██║██████╔╝██║  ██║██║  ██║██║
 ╚════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
                                           
'''

    print(logo)

    try: 
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)
    
        while True:
            
                username = input('Digite seu nome de usuário >>').lower().strip()

                if username:
                    break
                print('Não pode ser vazio!')

        while True:

            senha = input('Digite sua senha >>').strip()
        
            if senha:
                break
            print('Não pode ser vazio!')

        cursor.execute('SELECT id_usuario, senha, tipo_usuario FROM tbl_usuarios WHERE username = %s', (username,))
        usuario = cursor.fetchone()

        if not usuario:
            print('Usuário não encontrado!')    
            input('Digite enter para voltar')
            return

        usuario_id = usuario['id_usuario']
        senha_hash = usuario['senha']
        tipo = usuario['tipo_usuario']
        
        if not bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8')):
                print('Senha incorreta!')

        if tipo == 'professor':

            if not bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8')):
                print('Senha incorreta!')
                return

            cursor.execute('''SELECT id_professor FROM tbl_professores WHERE id_usuario_professor = %s''', (usuario_id,))
            professor = cursor.fetchone()
    
            if not professor:
                print("❌ Cadastro de professor incompleto!")
                input("Pressione Enter para voltar...")
                return
    
            menu_professor(professor['id_professor'])
            

        elif username == 'admin':
            menu_adm()

        elif tipo == 'aluno':
            agendamento_usuario(usuario_id) 
                
       

    
    
    except mysql.connector.Error as err:
        print(f'Erro{err}')
        input('Aperte enter para continuar....')
        conexao.rollback()

 
        cursor.close()
        conexao.close()

    




if __name__ == '__main__':
    print('Erro utilize o main.py para executar o código!')
