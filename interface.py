import customtkinter
from settings import conectar_banco
import mysql.connector
from mysql.connector import Error
from PIL import Image
import bcrypt
import re

customtkinter.set_appearance_mode('dark')


def cadastro():
   


    mensagem = customtkinter.CTkTextbox(app, text_color='white',fg_color='black',width=100, height=100,font=('arial',15),border_width=0)
    mensagem.insert('0.0','CADASTRO')
    mensagem.configure(state='disabled')
    mensagem.place(rely=0.3,relx=0.5,anchor='center')  


    nome_usuario = customtkinter.CTkEntry(app, placeholder_text='Nome',border_color='white')
    nome_usuario.place(rely=0.35,relx=0.5,anchor='center')
 

    email_usuario = customtkinter.CTkEntry(app, placeholder_text='email',border_color='white')
    email_usuario.place(rely=0.4,relx=0.5,anchor='center')


    telefone_usuario = customtkinter.CTkEntry(app, placeholder_text='telefone',border_color='white')
    telefone_usuario.place(rely=0.45,relx=0.5,anchor='center')

 
    usuario = customtkinter.CTkEntry(app, placeholder_text='Nome de usuário',border_color='white',placeholder_text_color='white',fg_color='#0e141a')
    usuario.place(rely=0.5,relx=0.5,anchor='center')

    senha_usuario = customtkinter.CTkEntry(app, placeholder_text='Senha', border_color='white',show='*')
    senha_usuario.place(rely=0.55, relx=0.5, anchor='center')


    def validar_cadastro():
        
        
        nome = nome_usuario.get()
        email = email_usuario.get()
        telefone = telefone_usuario.get()
        username = usuario.get()
        senha = senha_usuario.get()
        
    
        if nome:
            nome_usuario.configure(border_color='white')

        elif not nome:
            nome_usuario.configure(border_color="red")
            return

        if  re.match(r"[^@]+@[^@]+\.[^@]+", email):
            email_usuario.configure(border_color='white')  

        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            email_usuario.configure(border_color="red")
            return

        if telefone.isdigit() and len(telefone) ==11:
            telefone_usuario.configure(border_color='white')

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


            cursor.execute( 'SELECT 1 FROM tbl_usuarios WHERE username = %s OR email_usuario = %s', (username, email))
            if cursor.fetchone():
                
                mensagem = customtkinter.CTkTextbox(app, text_color='white',fg_color='black',width=350, height=100,font=('arial',15),border_width=0)
                mensagem.insert('0.0','NOME DE USUÁRIO JÁ CADASTRADO OU EMAIL JÁ CADASTRADO')
                mensagem.configure(state='disabled')
                mensagem.place(rely=0.7,relx=0.5,anchor='center')
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

                mensagem = customtkinter.CTkTextbox(app, text_color='white',fg_color='black',border_color='white',width=220, height=100,font=('arial',15),border_width=0)
                mensagem.insert('0.0','CADASTRO BEM SUCEDIDO!')
                mensagem.configure(state='disabled')
                mensagem.place(rely=0.7,relx=0.5,anchor='center')
                mensagem.after(2000,mensagem.destroy)  
            
        except Error as e:
            raise e


        cursor.close()
        conexao.close()
        



    confirmacao = customtkinter.CTkButton(app, text='Confirmar', command=validar_cadastro,fg_color='white',text_color='black',hover_color='gray')
    confirmacao.place(rely=0.6, relx=0.45, anchor='center')

    voltar = customtkinter.CTkButton(app, text='Voltar', fg_color='white',command=lambda: menu(),text_color='black',hover_color='gray')
    voltar.place(rely=0.6, relx=0.54,anchor = 'center')


def login():


    login = customtkinter.CTkEntry(app, placeholder_text='Usuário')
    login.place(relx=0.5,rely=0.5,anchor='center')
    
    senha_usuario = customtkinter.CTkEntry(app, placeholder_text='Senha', show='*')
    senha_usuario.place(relx=0.5,rely=0.55,anchor='center')




def troca_de_janela(opcao_selecionada):


    for widget in app.winfo_children():
     if not hasattr(widget, 'persistent'): 
        widget.destroy()
    
    if opcao_selecionada == 'login':
        login()

    elif opcao_selecionada == 'Cadastro':
       cadastro()

    elif opcao_selecionada == 'Sair':
       app.quit()

def menu():

    for widget in app.winfo_children():
        if not hasattr(widget, 'persistent'):
            widget.destroy()


    imagem = customtkinter.CTkImage(light_image=Image.open('placeholder.jpg'), size=(1920,1080))

    background = customtkinter.CTkLabel(app, image = imagem,text='')
    background.place(x=0, y=0,relwidth=1,relheight=1)
    background.persistent = True


    home = customtkinter.CTkLabel(app, text="Seja bem-vindo!", font=('arial',20), fg_color='black',bg_color='black')
    home.place(anchor='center', relx=0.5,rely=0.5)



    optionmenu = customtkinter.CTkOptionMenu(app, values=["login", "Cadastro", "Sair"],fg_color='black',button_color='black',dropdown_fg_color='black',corner_radius=0, command=troca_de_janela)   
    optionmenu.set("Opções")
    optionmenu.place(relx=0.5,rely=0.7,anchor='s')


    return app
   
app = customtkinter.CTk()
app.geometry("1920x1080")
imagem = customtkinter.CTkImage(light_image=Image.open('placeholder.jpg'), size=(1920,1080))
menu()
app.mainloop()