from datetime import datetime
import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="toor",
    database="escola_danca"
)
print('Olá seja bem vindo a escola de dança Jabari')
print('Para agendar uma aula precisamos fazer um cadastro primeiro, se tiver interesse digite uma das opções a seguir')
print('1 - cadastro')
print('2 - sair')
while True:
 opcao = int(input('Digite a opção: '))

 if opcao == 1:
     print('Para seu cadastro precisaremos de email e telefone, insira-os abaixo:')
     email = input('Email: ')
     telefone = input('Telefone: ')
    
     print('Agora selecione o dia, horário e estilo de dança que gostaria de praticar: ')
     while True:
        dia = input('Digite o dia desejado (DD/MM): ')
        try:
            dia_aula, mes_aula = map(int, dia.split('/'))
            data_atual = datetime.now()
            aula_valida = (
                (mes_aula >= data_atual.month) and
                (dia_aula >= data_atual.day if mes_aula == data_atual.month else True)
            )
            if aula_valida:
                break
            else:
                print(f'Data inválida ou já passou. Use DD/MM(dias futuros)')
        except:
            print(f'Formato inválido. Use DD/MM (ex:25/05).')
    
     while True:
        horario = input('Digite o horário desejado (no formato (HH:MM)): ')
        try:
            horas, minutos = map(int, horario.split(':'))
            if (8 <= horas <17) or (horas == 17 and minutos == 0):
                break
            else:
                print('Horario invalido. Escolha entre 08:00 e 17:00.')
        except:
            print('Formato invalido. Use HH:MM (ex:10:40).')
    
     estilos_disponiveis = ['salsa', 'forró', 'tango', 'Hip Hop', 'Balé', 'Zumba']
     print(f'Estilos de dança disponíveis: ')
     print(', '.join(estilos_disponiveis))


     while True:
        estilo_escolhido = input('Digite o estilo de dança escolhido: ').lower()
        if estilo_escolhido in estilos_disponiveis:
            print(f'Você escolheu o estilo {estilo_escolhido}')
            break
        else:
            print('Estilo não disponivel. Selecione um estilo da lista')


     print(f'Aula de {estilo_escolhido} agendada para o {dia} às {horario}')
     print(f'Detalhes enviados para {email}')
     print(f'Caso tenha interesse em outro estilo de dança ou em fazer mais aulas, faça outro agendamento!. Tenha um ótimo dia e obrigado pela preferência')
     print('Se não deseja outro agendamento apenas selecione a opção 2!')       
     
 elif opcao == 2:
     print('Obrigado pela visita, tenha um bom dia')
     break

 else:
     print('Opção invalida. Insira 1 ou 2')


 if opcao == 1:  
        cursorbd = db.cursor()
        comando = 'INSERT INTO usuarios (email_usuario, telefone_usuario) VALUES (%s, %s)'
        valores = (email, telefone)
        cursorbd.execute(comando, valores)
        db.commit()
        print('Aluno',email,'inserido com sucesso!')
        cursorbd.close()
        db.close()
