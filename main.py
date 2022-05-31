import time
import paramiko
import pysftp
from datetime import datetime
from tkinter import ttk, messagebox
from tkinter import *
from tkinter import filedialog as dlg

user = str
senha = str
file = str
remotedir = str
df = str

master = Tk()
master.title("Login")
master.geometry("318x397+610+153")
master.resizable(False, False)

# Funções --------------------------------------------------------

def nova_janela():
    color = '#181f2f'
    master.destroy()
    time.sleep(0.5)
    master1 = Tk()
    master1.title("Pesquisa Arquivos SFTP v1.0")
    master1.geometry("1020x390")
    master1.configure(background=color)
    master1.resizable(False, False)
    font = ("Segoe UI Light", 13)
    txt = Label(master1, text='Procurar por:', font=font, fg='white', bg=color)
    txt.place(x=30, y=20)
    txt2 = Label(master1, text='Diretório:', font=font, fg='white', bg=color)
    txt2.place(x=360, y=20)
    txt3 = Label(master1, text='Desenvolvido por:\nVítor Albuquerque', font="calibri 8", fg='white', bg=color)
    txt3.place(x=920, y=10)

    # Campos de Entrada
    file2 = Entry(master1, bd=2, font=("Calibri", 15), justify=CENTER)
    file2.place(width=200, height=33, x=140, y=20)
    remotedir2 = Entry(master1, bd=2, font=("Calibri", 15), justify=CENTER)
    remotedir2.place(width=200, height=33, x=440, y=20)

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp = pysftp.Connection('INSIRA O IP ADRESS AQUI', port=INSIRA A PORTA AQUI, username=str(user), password=str(senha),
                             cnopts=cnopts)

    def list_recursive(sftp, remotedir, file):
        try:
            for entry in sftp.listdir_attr(remotedir):
                remotepath = remotedir + "/" + entry.filename
                master1.update()
                if sftp.isdir(remotepath):
                    list_recursive(sftp, remotepath, file)
                    print(remotepath)
                    if file in remotepath:
                        df = (remotepath, datetime.fromtimestamp(entry.st_mtime),'\n')
                        input_txt.insert(END, df)
        except FileNotFoundError:
            messagebox.showerror('Erro', 'Esse diretório não existe.')

    def procurar():
        file = str(file2.get())
        remotedir = str(remotedir2.get())
        list_recursive(sftp, remotedir, file)

    bt_pesquisar = Button(master1, text='Procurar', fg='white', bg='#665f6f', font=font, command=procurar)
    bt_pesquisar.place(width=100, height=53, x=665, y=10)
    input_txt = Text(master1, bg="#E6E6FA")
    input_txt.place(width=950, height=235, x=30, y=80)
    scrollbar = ttk.Scrollbar(master1, orient='vertical', command=input_txt.yview)
    scrollbar.place(height=235, x=975, y=80)
    input_txt['yscrollcommand'] = scrollbar.set

def enviar():
    global user, senha
    user = str(userEntry.get())
    senha = str(senhaEntry.get())
    try:
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        pysftp.Connection('INSIRA O IP ADRESS AQUI', port=INSIRA A PORTA AQUI, username=user, password=senha,
                          cnopts=cnopts)
        messagebox.showinfo('Bem vindo!', 'Logado como: {}'.format(user))
        nova_janela()
    except paramiko.ssh_exception.AuthenticationException:
        messagebox.showerror('Erro', 'Usuário ou senha incorretos.\n\n'
                                     'Tente novamente!\n\n'
                                     'Obs: Insira os dados de acesso do SFTP')
    return user, senha

# Variáveis globais ------------------------------------------------------
esconda_senha = StringVar()

# Importar imagens -------------------------------------------------------
img_fundo = PhotoImage(file="fundo.png")
img_botao = PhotoImage(file="bt-img.png")

# Criação de labels ------------------------------------------------------
lab_fundo = Label(master, image=img_fundo)
lab_fundo.pack()

# Criação de caixas de entrada -------------------------------------------
userEntry = Entry(master, bd=2, font=("Calibri", 15), justify=CENTER)
userEntry.place(width=287, height=33, x=15, y=115)
senhaEntry = Entry(master, textvariable=esconda_senha, show="*", bd=2, font=("Calibri", 15), justify=CENTER)
senhaEntry.place(width=287, height=33, x=15, y=222)

# Criação de botões ------------------------------------------------------
bt_entrar = Button(master, bd=0, image=img_botao, command=enviar)
bt_entrar.place(width=84, height=44, x=118, y=295)

master.mainloop()


