import customtkinter
from settings import conectar_banco
import mysql.connector
from mysql.connector import Error
from PIL import Image
import bcrypt
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

customtkinter.set_appearance_mode('dark')

def teste():

  
    label = customtkinter.CTkLabel(app,text='', width=180, height=270,corner_radius=15,bg_color='black',fg_color='#154360')
    label.place(relx=0.5,rely=0.5,anchor='center')
    
    
    voltar = customtkinter.CTkButton(app, text='Campo de testes', fg_color='#48c9b0',command=lambda: menu(),text_color='white',hover_color='#17a589',corner_radius=15,bg_color='#17202a',width=120)
    voltar.place(rely=0.54, relx=0.535,anchor = 'center')


def cadastro():
 

    label = customtkinter.CTkLabel(app, width=270,height=380,fg_color="#17202a",corner_radius=15,bg_color='black',text='')
    label.place(rely=0.4,relx=0.5,anchor='center')


    mensagem = customtkinter.CTkTextbox(app, text_color='white',fg_color='#17202a',width=160, height=50,font=('Times New Roman',20),border_width=0,bg_color='#17202a')
    mensagem.tag_config('center',justify='center')
    mensagem.insert('0.0','Crie sua conta','center')
    mensagem.configure(state='disabled')
    mensagem.place(rely=0.28,relx=0.5,anchor='center')
    mensagem.lift() 

    nome_usuario = customtkinter.CTkEntry(app, placeholder_text='Digite seu nome...',width=230,fg_color='#212f3d',border_width=0.8)
    nome_usuario.place(rely=0.33,relx=0.5,anchor='center')
 

    email_usuario = customtkinter.CTkEntry(app, placeholder_text='Digite seu email...',border_color='gray',width=230,fg_color='#212f3d',border_width=0.8)
    email_usuario.place(rely=0.37,relx=0.5,anchor='center')


    telefone_usuario = customtkinter.CTkEntry(app, placeholder_text='Digite seu telefone...',border_color='gray',width=230,fg_color='#212f3d',border_width=0.8)
    telefone_usuario.place(rely=0.41,relx=0.5,anchor='center')

 
    usuario = customtkinter.CTkEntry(app, placeholder_text='Crie um nome de usuário...',border_color='gray',fg_color='#212f3d',width=230,border_width=0.8)
    usuario.place(rely=0.45,relx=0.5,anchor='center')

    senha_usuario = customtkinter.CTkEntry(app, placeholder_text='Crie uma senha...', border_color='gray',show='*',width=230,fg_color='#212f3d',border_width=0.8)
    senha_usuario.place(rely=0.49, relx=0.5, anchor='center')



    def validar_cadastro():
        
        
        nome = nome_usuario.get()
        email = email_usuario.get()
        telefone = telefone_usuario.get()
        username = usuario.get()
        senha = senha_usuario.get()
        
    
        if nome:
            nome_usuario.configure(border_color='gray')

        elif not nome:
            nome_usuario.configure(border_color="red")
            return

        if  re.match(r"[^@]+@[^@]+\.[^@]+", email):
            email_usuario.configure(border_color='gray')  

        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            email_usuario.configure(border_color="red")
            return

        if telefone.isdigit() and len(telefone) ==11:
            telefone_usuario.configure(border_color='gray')

        elif not telefone.isdigit() or len(telefone) < 11:
            telefone_usuario.configure(border_color="red")
            return
        
        if not username:
            usuario.configure(border_color="red")
            return
        
        if senha:
          senha_usuario_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        elif not senha:
            senha_usuario.configure(border_color="red")
            return


        try:

            conexao = conectar_banco()
            cursor = conexao.cursor()


            cursor.execute( 'SELECT 1 FROM tbl_usuarios WHERE email_usuario = %s', (email,))
            if cursor.fetchone():
                
                mensagem = customtkinter.CTkTextbox(app, text_color='red',fg_color='#17202a',width=200, height=30,font=('arial',10),border_width=0,bg_color='#17202a')
                mensagem.tag_config('center',justify='center')
                mensagem.insert('0.0','Email já cadastrado!','center')
                mensagem.configure(state='disabled')
                mensagem.place(rely=0.28,relx=0.5,anchor='center')
                mensagem.after(2000,mensagem.destroy)
                return 


            cursor.execute( 'SELECT 1 FROM tbl_usuarios WHERE username = %s', (username,))
            if cursor.fetchone():
                
                mensagem = customtkinter.CTkTextbox(app, text_color='red',fg_color='#17202a',width=200, height=30,font=('arial',10),border_width=0,bg_color='#17202a')
                mensagem.tag_config('center',justify='center')
                mensagem.insert('0.0','Nome de usuário já cadastrado','center')
                mensagem.configure(state='disabled')
                mensagem.place(rely=0.28,relx=0.5,anchor='center')
                mensagem.after(2000,mensagem.destroy)
                return 

            
            cursor.execute( '''INSERT INTO tbl_usuarios 
                     (nome_usuario,email_usuario,telefone_usuario,username,senha) 
                     VALUES (%s,%s,%s,%s,%s) ''',(nome,email,telefone,username,senha_usuario_hash))
        

            conexao.commit()
            if conexao.commit:
                nome_usuario.delete(0, 'end')
                email_usuario.delete(0, 'end')
                telefone_usuario.delete(0, 'end')
                usuario.delete(0,'end')
                senha_usuario.delete(0,'end')

                mensagem = customtkinter.CTkTextbox(app, text_color='white',fg_color='#17202a',width=238, height=40,font=('arial',15),border_width=0.8, corner_radius=15,bg_color='black')
                mensagem.insert('0.0','CADASTRO BEM SUCEDIDO!')
                mensagem.configure(state='disabled')
                mensagem.place(rely=0.65,relx=0.5,anchor='center')
                mensagem.after(2000,mensagem.destroy)  
            
        except Error as e:
            raise e


        cursor.close()
        conexao.close()
        



    confirmacao = customtkinter.CTkButton(app, text='Confirmar',command=validar_cadastro,fg_color='#58d68d',text_color='white',hover_color='#239b56',corner_radius=15,bg_color='#17202a',width=120)
    confirmacao.place(rely=0.54, relx=0.465, anchor='center')

    voltar = customtkinter.CTkButton(app, text='Voltar', fg_color='#48c9b0',command=lambda: menu(),text_color='white',hover_color='#17a589',corner_radius=15,bg_color='#17202a',width=120)
    voltar.place(rely=0.54, relx=0.535,anchor = 'center')


def matricula(usuario_id=None):

    for widget in app.winfo_children():
            if not hasattr(widget, 'persistent'):
                widget.destroy()


    label = customtkinter.CTkLabel(app, width=340,height=380,fg_color="#17202a",corner_radius=15,bg_color='black',text='',)
    label.place(rely=0.4,relx=0.5,anchor='center')

    mensagem = customtkinter.CTkTextbox(app, text_color='white',fg_color='#17202a',width=190, height=100,font=('Times New Roman',20),border_width=0,bg_color='#17202a')
    mensagem.tag_config('center',justify='center')
    mensagem.insert('0.0','Temos preço fixo\nde\n50 reais mensal!','center')
    mensagem.configure(state='disabled')
    mensagem.place(rely=0.32,relx=0.5,anchor='center')
    mensagem.lift() 


    tempo = customtkinter.CTkOptionMenu(app,values=['1 Mês','2 Meses','3 Meses','4 Meses','5 Meses','6 Meses','7 Meses','8 Meses','9 Meses','10 Meses','11 Meses','12 Meses'],fg_color='#bb8fce',dropdown_fg_color='#e8daef',button_color='#bb8fce', button_hover_color='#bb8fce',
                                        dropdown_hover_color='#bb8fce',dropdown_text_color='black')
    tempo.set('Selecione o tempo de duração da sua matrícula')
    tempo.place(relx=0.5,rely=0.4,anchor='center')

    pagamento = customtkinter.CTkOptionMenu(app,values=['Pix','Cartão','Boleto'],fg_color='#bb8fce',button_color='#bb8fce',dropdown_fg_color='#e8daef', dropdown_text_color='black', button_hover_color='#bb8fce', dropdown_hover_color='#bb8fce', )
    pagamento.set('Métodos de pagamento')
    pagamento.place(relx=0.5,rely=0.45,anchor='center')


    def validar_matricula(usuario_id):

        tempo_selecionado = tempo.get()

        if tempo_selecionado == 'Duração':
            mensagem = customtkinter.CTkTextbox(app, text_color='white',fg_color='black',width=235, height=40,font=('arial',15),border_width=0.8, corner_radius=15,bg_color='black')
            mensagem.insert('0.0','Selecione uma duração válida!')
            mensagem.configure(state='disabled')
            mensagem.place(rely=0.65,relx=0.5,anchor='center')
            mensagem.after(2000,mensagem.destroy)
            return
        
        pagamento_selecionado = pagamento.get()

        if pagamento_selecionado == 'Métodos de pagamento':
            mensagem = customtkinter.CTkTextbox(app, text_color='white',fg_color='black',width=280, height=40,font=('arial',15),border_width=0.8, corner_radius=15,bg_color='black')
            mensagem.insert('0.0','Selecione um método de pagamento!')
            mensagem.configure(state='disabled')
            mensagem.place(rely=0.65,relx=0.5,anchor='center')
            mensagem.after(2000,mensagem.destroy)
            return

  
        try:

            meses = int(tempo_selecionado.split()[0])
            data_matricula = datetime.now().date()
            data_termino = data_matricula + relativedelta(months=meses)

            conexao = conectar_banco()
            cursor = conexao.cursor()

            cursor.execute('''SELECT 1 FROM tbl_matriculas WHERE usuario_id = %s ''',(usuario_id,))
            resultado = cursor.fetchone()

            if resultado:
                mensagem = customtkinter.CTkTextbox(app, text_color='white',fg_color='#17202a',width=200, height=40,font=('arial',15),border_width=0.8, corner_radius=15,bg_color='black')
                mensagem.insert('0.0','Você ja está matriculado!')
                mensagem.configure(state='disabled')
                mensagem.place(rely=0.65,relx=0.5,anchor='center')
                mensagem.after(2000,mensagem.destroy)
                return
            
            cursor.execute('''INSERT INTO tbl_matriculas (usuario_id, data_termino ,metodo_pagamento) VALUES (%s,%s,%s)
                           ''',(usuario_id, data_termino, pagamento_selecionado))

            
            conexao.commit()
            if conexao.commit:
                mensagem = customtkinter.CTkTextbox(app, text_color='white',fg_color='#17202a',width=250, height=40,font=('arial',15),border_width=0.8, corner_radius=15,bg_color='black')
                mensagem.insert('0.0','Matricula efetuada com sucesso!')
                mensagem.configure(state='disabled')
                mensagem.place(rely=0.65,relx=0.5,anchor='center')
                mensagem.after(2000,mensagem.destroy)

        except Error as e:
            raise e


        cursor.close()
        conexao.close()
            
    
    confirmacao = customtkinter.CTkButton(app, text='Matricular-se',command=lambda: validar_matricula(usuario_id),fg_color='#58d68d',text_color='white',hover_color='#239b56',corner_radius=15,bg_color='#17202a',width=120)
    confirmacao.place(rely=0.54, relx=0.465, anchor='center')

    
    voltar = customtkinter.CTkButton(app, text='Voltar', fg_color='#48c9b0',command=lambda: central_usuario(usuario_id),text_color='white',hover_color='#17a589',corner_radius=15,bg_color='#17202a',width=120)
    voltar.place(rely=0.54, relx=0.535,anchor = 'center')



def agendamento(usuario_id):


    voltar = customtkinter.CTkButton(app, text='Voltar', fg_color='#48c9b0',command=lambda: central_usuario(usuario_id),text_color='white',hover_color='#17a589',corner_radius=15,bg_color='#154360',width=120)
    voltar.place(rely=0.56, relx=0.5,anchor = 'center')



def central_usuario(usuario_id):

    for widget in app.winfo_children():
            if not hasattr(widget, 'persistent'):
                widget.destroy()


    label = customtkinter.CTkLabel(app,text='', width=180, height=270,corner_radius=15,bg_color='black',fg_color='#154360')
    label.place(relx=0.5,rely=0.5,anchor='center')

    
    matricular = customtkinter.CTkButton(app,text='Matricula',text_color='white',corner_radius=15,bg_color='#154360',width=120,fg_color='#52be80',hover_color='#1e8449', command=lambda:matricula(usuario_id))
    matricular.place(rely=0.44,relx=0.5,anchor='center')

    def validar_matricula(usuario_id):

        try:

            conexao = conectar_banco()
            cursor = conexao.cursor()


            cursor.execute('''SELECT 1 FROM tbl_matriculas WHERE usuario_id = %s ''',(usuario_id,))
            resultado = cursor.fetchone()

            if not resultado:
                
                mensagem = customtkinter.CTkTextbox(app, text_color='white',fg_color='#154360',width=220, height=40,font=('arial',15),border_width=0.5, corner_radius=15,bg_color='black', border_color='Black')
                mensagem.insert('0.0','Você Não está matriculado!')
                mensagem.configure(state='disabled')
                mensagem.place(rely=0.7,relx=0.5,anchor='center') 
                mensagem.after(2000,mensagem.destroy)
                return
            
            else:
               for widget in app.winfo_children():
                    if not hasattr(widget, 'persistent'):
                        widget.destroy()

                    agendamento(usuario_id)

                
        except Error as e:
            raise e
    
    
    agendar = customtkinter.CTkButton(app,text='Agendamento', text_color='white',corner_radius=15,bg_color='#154360',width=120,fg_color='#138d75',hover_color='#0e6655', command=lambda:validar_matricula(usuario_id))
    agendar.place(rely=0.5,relx=0.5,anchor='center')

    voltar = customtkinter.CTkButton(app, text='Voltar', fg_color='#48c9b0',command=lambda: menu(),text_color='white',hover_color='#17a589',corner_radius=15,bg_color='#154360',width=120)
    voltar.place(rely=0.56, relx=0.5,anchor = 'center')



def login():

 
    label = customtkinter.CTkLabel(app, width=270,height=220,fg_color="#17202a",corner_radius=15,bg_color='black',text='')
    label.place(rely=0.4,relx=0.5,anchor='center')


    mensagem = customtkinter.CTkTextbox(app, text_color='white',fg_color='#17202a',width=160, height=50,font=('Times New Roman',20),border_width=0,bg_color='#17202a')
    mensagem.tag_config('center',justify='center')
    mensagem.insert('0.0','Faça seu login','center')
    mensagem.configure(state='disabled')
    mensagem.place(rely=0.33,relx=0.5,anchor='center')
    mensagem.lift() 


    login_usuario = customtkinter.CTkEntry(app, placeholder_text='Usuário')
    login_usuario.place(relx=0.5,rely=0.37,anchor='center')
    
    senha_usuario = customtkinter.CTkEntry(app, placeholder_text='Senha', show='*')
    senha_usuario.place(relx=0.5,rely=0.41,anchor='center')
    
    try:
        

        def validar_login():

            conexao = conectar_banco()
            cursor = conexao.cursor()

            username = login_usuario.get()
            senha_get = senha_usuario.get()

            if not username:
                login_usuario.configure(border_color="red")
                mensagem = customtkinter.CTkTextbox(app, text_color='white',fg_color='#17202a',width=195, height=40,font=('arial',15),border_width=0.8, corner_radius=15,bg_color='black')
                mensagem.insert('0.0','Insira algo!')
                mensagem.configure(state='disabled')
                mensagem.place(rely=0.65,relx=0.5,anchor='center')
                mensagem.after(2000,mensagem.destroy)
                return

            if not senha_get:
                senha_usuario.configure(border_color="red")
                mensagem = customtkinter.CTkTextbox(app, text_color='white',fg_color='#17202a',width=195, height=40,font=('arial',15),border_width=0.8, corner_radius=15,bg_color='black')
                mensagem.insert('0.0','Insira algo!')
                mensagem.configure(state='disabled')
                mensagem.place(rely=0.65,relx=0.5,anchor='center')
                mensagem.after(2000,mensagem.destroy)
                return
            
            cursor.execute('SELECT id_usuario, senha, tipo_usuario FROM tbl_usuarios WHERE username = %s', (username,))
            usuario = cursor.fetchone()
        
            if not usuario:
                mensagem = customtkinter.CTkTextbox(app, text_color='white',fg_color='#17202a',width=195, height=40,font=('arial',15),border_width=0.8, corner_radius=15,bg_color='black')
                mensagem.insert('0.0','Usuário não cadastrado!')
                mensagem.configure(state='disabled')
                mensagem.place(rely=0.65,relx=0.5,anchor='center')
                mensagem.after(2000,mensagem.destroy) 
                return

            senha_hash = usuario[1]
            
            if not bcrypt.checkpw(senha_get.encode('utf-8'), senha_hash.encode('utf-8')):
                mensagem = customtkinter.CTkTextbox(app, text_color='white',fg_color='#17202a',width=145, height=40,font=('arial',15),border_width=0.8, corner_radius=15,bg_color='black')
                mensagem.insert('0.0','Senha incorreta!')
                mensagem.configure(state='disabled')
                mensagem.place(rely=0.65,relx=0.5,anchor='center')
                mensagem.after(2000,mensagem.destroy) 
                return

            if usuario and bcrypt.checkpw(senha_get.encode('utf-8'), senha_hash.encode('utf-8')):
                mensagem_login = customtkinter.CTkTextbox(app, text_color='white',fg_color='#17202a',width=170, height=40,font=('arial',15),border_width=0.8, corner_radius=15,bg_color='black')
                mensagem_login.insert('0.0','Login bem sucedido!')
                mensagem_login.configure(state='disabled')
                mensagem_login.place(rely=0.65,relx=0.5,anchor='center')
                
                def destruir_widget():
                    for widget in app.winfo_children():
                        if not hasattr(widget, 'persistent'):
                            widget.destroy()

                    central_usuario(usuario[0])           
                
                mensagem_login.after(2000,destruir_widget)
                
                cursor.close()
                conexao.close()
    
    except Error as e:
            raise e

  
    botao_login = customtkinter.CTkButton(app, text='Login',fg_color='#58d68d',text_color='white',hover_color='#239b56',corner_radius=15,bg_color='#17202a',width=120,command=validar_login)
    botao_login.place(rely=0.47,relx=0.465,anchor='center')

    voltar = customtkinter.CTkButton(app, text='Voltar', fg_color='#48c9b0',command=lambda: menu(),text_color='white',hover_color='#17a589',corner_radius=15,bg_color='#17202a',width=120)
    voltar.place(rely=0.47, relx=0.535,anchor = 'center')

def troca_de_janela(opcao_selecionada):

    for widget in app.winfo_children():
     if not hasattr(widget, 'persistent'): 
        widget.destroy()
    
    if opcao_selecionada == 'login':
        login()

    elif opcao_selecionada == 'Cadastro':
       cadastro()

    elif opcao_selecionada == "Teste":
        teste()

    elif opcao_selecionada == 'Sair':
       app.quit()

def menu():

    for widget in app.winfo_children():
        if not hasattr(widget, 'persistent'):
            widget.destroy()

    imagem = customtkinter.CTkImage(Image.open('placeholder.jpg'), size=(1920,1080))

    background = customtkinter.CTkLabel(app, image = imagem,text='')
    background.place(x=0, y=0,relwidth=1,relheight=1)
    background.persistent = True


    saudacao = customtkinter.CTkImage(Image.open('welcome.jpg'),size=(700,300))
    home = customtkinter.CTkLabel(app,image=saudacao,text="" )
    home.place(anchor='center', relx=0.5,rely=0.5)

    optionmenu = customtkinter.CTkOptionMenu(app, values=["login", "Cadastro", "Sair", "Teste"],fg_color='black',button_color='black',dropdown_fg_color='black',corner_radius=0, command=troca_de_janela)   
    optionmenu.set("Opções")
    optionmenu.place(relx=0.5,rely=0.7,anchor='s')

    return app
   
app = customtkinter.CTk()
app.geometry("1920x1080")
app.title('Tompinha')
imagem = customtkinter.CTkImage(light_image=Image.open('placeholder.jpg'), size=(1920,1080))
menu()
app.mainloop()