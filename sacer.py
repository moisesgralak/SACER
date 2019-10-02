import tkinter as tk
from tkinter import font  as tkfont
import paramiko
from time import sleep
import datetime
import telnetlib
import sqlite3






class SacerApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOrbBkp, PageOrbRbt, PageTunelMpls):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Bem Vindo", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        lf1 = tk.LabelFrame(self, text="Aperte o botão do equipamento que deseja acessar:", bg='#DCDCDC',  width=740, height=500, font=("Arial", 12, "bold"))
        button1 = tk.Button(lf1, text="Backup Radio\n Orbit", width=15, height=5,
                            command=lambda: controller.show_frame("PageOrbBkp"))
        button2 = tk.Button(lf1, text="Reboot Radio\n Orbit", width=15, height=5,
                            command=lambda: controller.show_frame("PageOrbRbt"))
        button3 = tk.Button( lf1, text="Backup Switch\n Raisecom", width=15, height=5,
                             command=lambda: controller.show_frame( "PageOrbBkp" ) )
        button4 = tk.Button( lf1, text="Reboot Switch\n Raisecom", width=15, height=5,
                             command=lambda: controller.show_frame( "PageOrbRbt" ) )
        button5 = tk.Button( lf1, text="Tuneis MPLS\n Fibra Óptica", width=15, height=5 ,
                             command=lambda: controller.show_frame( "PageTunelMpls" ) )
        button6 = tk.Button( lf1, text="Status Backbone\n Fibra Óptica", width=15, height=5,
                             command=lambda: controller.show_frame( "PageOrbRbt" ) )

        button1.place(x=50, y=40)
        button2.place( x=50, y=130 )
        button3.place( x=170, y=40 )
        button4.place( x=170, y=130 )
        button5.place( x=290, y=40)
        button6.place( x=290, y=130 )

# eixo X cada 120px
# eixo Y cada 90px

        lf1.place(x=30, y=60)


class PageOrbBkp(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.lb_saida_bkp_o_l1 = tk.StringVar()
        self.lb_saida_bkp_o_l2 = tk.StringVar()
        self.lb_saida_bkp_o_l3 = tk.StringVar()
        label = tk.Label(self, text="Bem vindo a página de backup do rádio Orbit", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.lf_ro_bkp = tk.LabelFrame(self, text="Preencha os dados do equipamento", width=740,
                            height=500, font=("Arial", 12, "bold"))
        self.lb1 = tk.Label(self.lf_ro_bkp, text="Digite o IP do equipamento: ")
        self.lb1.place(x=50, y=40)
        self.lb1 = tk.Label( self.lf_ro_bkp, text="Digite o nome do arquivo: " )
        self.lb1.place(x=50, y=80)
        self.lb1 = tk.Label( self.lf_ro_bkp, text="Digite o IP do servidor FTP: " )
        self.lb1.place( x=50, y=120 )
        self.lb1 = tk.Label( self.lf_ro_bkp, text="Login FTP: ")
        self.lb1.place( x=50, y=160 )
        self.lb1 = tk.Label( self.lf_ro_bkp, text="Senha FTP: " )
        self.lb1.place( x=420, y=160 )
        self.ip = tk.Entry(self.lf_ro_bkp, width=37, font=("Arial", 12, "bold"))
        self.ip.place(x=210, y=40)
        self.nome_save_orb = tk.Entry(self.lf_ro_bkp, width=37, font=("Arial", 12, "bold"))
        self.nome_save_orb.place( x=210, y=80)
        self.ip_ftp = tk.Entry( self.lf_ro_bkp, width=37, font=("Arial", 12, "bold") )
        self.ip_ftp.place( x=210, y=120 )
        self.login_ftp = tk.Entry( self.lf_ro_bkp, width=21, font=("Arial", 12, "bold") )
        self.login_ftp.place( x=210, y=160 )
        self.senha_ftp = tk.Entry( self.lf_ro_bkp, width=21, font=("Arial", 12, "bold"), show='*' )
        self.senha_ftp.place( x=500, y=160 )
        self.bt_bkp = tk.Button( self.lf_ro_bkp, text="Backup", width=15, height=6, font=("Arial", 10, "bold"), command=self.bkp_orbit)
        self.bt_bkp.place(x=560, y=37)
        self.bt_bkp.bind("<KeyPress>", lambda e: self.bkp_orbit() if e.char == '\r'else None)
        self.lb_saida_cmd = tk.LabelFrame( self.lf_ro_bkp, text='Saída de comandos', width=650, height=120)
        self.lb_saida_bkp_orb_l1 = tk.Label(self.lb_saida_cmd, textvariable=self.lb_saida_bkp_o_l1, font=('Arial', 12))
        self.lb_saida_bkp_orb_l1.place( x=10, y=10 )
        self.lb_saida_bkp_orb_l2 = tk.Label(self.lb_saida_cmd, textvariable=self.lb_saida_bkp_o_l2, font=('Arial', 12))
        self.lb_saida_bkp_orb_l2.place( x=10, y=30 )
        self.lb_saida_bkp_orb_l3 = tk.Label(self.lb_saida_cmd, textvariable=self.lb_saida_bkp_o_l3, font=('Arial', 12))
        self.lb_saida_bkp_orb_l3.place( x=10, y=50)
        self.lb_saida_cmd.place( x=50, y=200 )
        self.lb_help = tk.LabelFrame(self.lf_ro_bkp, text='Funcionalidade da tela', width=650, height=120)
        self.txt_help = """Esta Tela serve para fazer backup do radio orbit para um servidor FTP,Fazendo com que o arquivo de configuração no formato XML possa ser carregado novamente em um novo equipamento."""
        self.msg_help = tk.Message(self.lb_help, text=self.txt_help, font=('Arial', 12), width=600)
        self.msg_help.place(x=10, y=10)
        self.msg_help.place(x=10, y=10)
        self.lb_help.place(x=50, y=330)
        self.lf_ro_bkp.place(x=30, y=60)
        button = tk.Button(self, text="Voltar para tela inicial",
                           command=lambda: controller.show_frame("StartPage"))
        button.place(x=320, y=565)


    def bkp_orbit(self):
        hostname = self.ip.get()
        save_name = self.nome_save_orb.get()
        end_ftp = self.ip_ftp.get()
        user_ftp = self.login_ftp.get()
        passwd_ftp = self.senha_ftp.get()
        cmd = 'request system configuration-files export filename ' + save_name + '_' + hostname + '.xml manual-file-server { ftp { address '+end_ftp+' username '+user_ftp+' password '+passwd_ftp+' timeout 5 } }'

        try:
            self.lb_s_l1 = 'Conectando a '+hostname+'!'
            self.lb_saida_bkp_o_l1.set(self.lb_s_l1)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname, 22, username='admin', password='Rumotr!lh0', timeout=5)
            self.lb_s_l2 = 'Conectado ao '+save_name+'!'
            self.lb_saida_bkp_o_l2.set(self.lb_s_l2)
            client.exec_command(cmd)
            client.close()
            self.lb_s_l3 = 'Backup de '+save_name+' com o IP '+hostname+' para o FTP 10.41.60.107 com sucesso!'
            self.lb_saida_bkp_o_l3.set(self.lb_s_l3)
        except Exception as e:

            self.lb_saida_bkp_o_l1.set('O equipamento ('+save_name+') IP ('+hostname+') está offline!')


class PageOrbRbt(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTunelMpls(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Esta é a pagina de controle de túneis MPLS da serra de Santos", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.lb_saida = tk.StringVar()
        self.lf_tf_main = tk.LabelFrame(self, text='Tuneis MPLS Fibra', width=740, height=500, font=('Arial', 12, 'bold'))
        self.lf_tf_des = tk.LabelFrame(self.lf_tf_main, text='Desativar tunel de:', width=500, height=150, font=('Arial', 12, 'bold'))
        self.bt_des_zev = tk.Button(self.lf_tf_des, width=15, height=5, text='Desativar\nTunel\nZPT', command=self.des_zpt)
        self.bt_des_zev.place(x=50, y=20)
        self.bt_des_zev = tk.Button( self.lf_tf_des, width=15, height=5, text='Desativar\nTunel\nZEV', command=self.des_zev)
        self.bt_des_zev.place( x=180, y=20 )
        self.bt_des_zev = tk.Button( self.lf_tf_des, width=15, height=5, text='Desativar\nTunel\nZGA', command=self.des_zga)
        self.bt_des_zev.place( x=310, y=20 )
        self.lf_tf_des.place( x=30, y=20 )
        self.lf_tf_atv = tk.LabelFrame( self.lf_tf_main, text='Ativar tunel de:', width=500, height=150, font=('Arial', 12, 'bold') )
        self.bt_atv_zev = tk.Button( self.lf_tf_atv, width=15, height=5, text='Ativar\nTunel\nZPT', command=self.atv_zpt)
        self.bt_atv_zev.place( x=50, y=20 )
        self.bt_atv_zev = tk.Button( self.lf_tf_atv, width=15, height=5, text='Ativar\nTunel\nZEV', command=self.atv_zev)
        self.bt_atv_zev.place( x=180, y=20 )
        self.bt_atv_zev = tk.Button( self.lf_tf_atv, width=15, height=5, text='Ativar\nTunel\nZGA', command=self.atv_zga)
        self.bt_atv_zev.place( x=310, y=20 )
        self.lf_saida_cmd = tk.LabelFrame(self.lf_tf_main, text='Saída comando', width=500, height=100, font=('Arial', 12, 'bold'))
        self.lb_saida_fo_cmd = tk.Label(self.lf_saida_cmd, textvariable=self.lb_saida, font=('Arial', 15, 'bold'))
        self.lb_saida_fo_cmd.place(x=50, y=20)
        self.lf_saida_cmd.place(x=30, y=360)
        self.lf_tf_atv.place( x=30, y=200 )
        self.lf_tf_main.place(x=30, y=60)
        button = tk.Button(self, text="Voltar para tela inicial",
                           command=lambda: controller.show_frame("StartPage"))
        button.place(x=340, y=565)


    def validar_texto(self, text):

        if 'disable' in text:
            print(f'interface {self.site} desativada')
            self.lb_saida.set('Tunel GRE '+self.site+' desativada')


        elif 'enable' in text:
            print( f'interface {self.site} ativada')
            self.lb_saida.set('Tunel GRE '+self.site+' ativada')


    def des_zpt(self):

        self.site = 'ZPT'
        host = '10.255.27.94'
        print( f"conectando ao host {host}..." )
        sleep( 2 )
        conect = telnetlib.Telnet( host, 23, 3 )
        print( 'Conectado!' )
        conect.read_until( b'Login:', 60 )
        conect.write( b"raisecom\r\n" )
        conect.read_until( b'Password:', 60 )
        conect.write( b"raisecom\r\n" )
        conect.write( b"enable\r\n" )
        conect.write( b"raisecom\r\n" )
        conect.write( b"conf t\r\n" )
        conect.write( b"interface port 2\r\n" )
        conect.write( b"shutdown\r\n" )
        conect.write( b"exit\r\n" )
        conect.write( b"exit\r\n" )
        conect.write( b"show interface port-list 2\r\n" )
        sleep( 2 )
        saida = conect.read_very_eager().decode( 'ascii' )
        arquivo = open( 'C:\\Users\\cs305672\\PycharmProjects\\SACER\\venv\\src\\log_gre_ssantos.txt', 'a' )
        arquivo2 = open( 'C:\\Users\\cs305672\\PycharmProjects\\SACER\\venv\\src\\log_saida_gre_ssantos.txt', 'w' )
        data = datetime.datetime.now().strftime( '%d/%m/%Y as %H:%M:%S' )
        arquivo.write( f'Desativação da interface de {self.site} realizada em {data}' )
        arquivo.write( saida )
        arquivo2.write( saida )
        arquivo.write( "\n\n" )
        arquivo.close()
        conect.close()
        self.validar_texto( saida )


    def des_zev(self):
        self.site = 'ZEV'
        host = '10.255.27.94'
        print( f"conectando ao host {host}..." )
        sleep( 2 )
        conect = telnetlib.Telnet( host, 23, 3 )
        print( 'Conectado!' )
        conect.read_until( b'Login:', 60 )
        conect.write( b"raisecom\r\n" )
        conect.read_until( b'Password:', 60 )
        conect.write( b"raisecom\r\n" )
        conect.write( b"enable\r\n" )
        conect.write( b"raisecom\r\n" )
        conect.write( b"conf t\r\n" )
        conect.write( b"interface port 6\r\n" )
        conect.write( b"shutdown\r\n" )
        conect.write( b"exit\r\n" )
        conect.write( b"exit\r\n" )
        conect.write( b"show interface port-list 6\r\n" )
        sleep( 2 )
        saida = conect.read_very_eager().decode( 'ascii' )
        arquivo = open( 'C:\\Users\\cs305672\\PycharmProjects\\SACER\\venv\\src\\log_gre_ssantos.txt', 'a' )
        arquivo2 = open( 'C:\\Users\\cs305672\\PycharmProjects\\SACER\\venv\\src\\log_saida_gre_ssantos.txt', 'w' )
        data = datetime.datetime.now().strftime( '%d/%m/%Y as %H:%M:%S' )
        arquivo.write( f'Desativação da interface de {self.site} realizada em {data}' )
        arquivo.write( saida )
        arquivo2.write(saida)
        arquivo.write( "\n\n" )
        arquivo.close()
        conect.close()
        self.validar_texto(saida)


    def des_zga(self):

        self.site = 'ZGA'
        host = '10.255.27.94'
        print( f"conectando ao host {host}..." )
        sleep( 2 )
        conect = telnetlib.Telnet( host, 23, 3 )
        print( 'Conectado!' )
        conect.read_until( b'Login:', 60 )
        conect.write( b"raisecom\r\n" )
        conect.read_until( b'Password:', 60 )
        conect.write( b"raisecom\r\n" )
        conect.write( b"enable\r\n" )
        conect.write( b"raisecom\r\n" )
        conect.write( b"conf t\r\n" )
        conect.write( b"interface port 4\r\n" )
        conect.write( b"shutdown\r\n" )
        conect.write( b"exit\r\n" )
        conect.write( b"exit\r\n" )
        conect.write( b"show interface port-list 4\r\n" )
        sleep( 2 )
        saida = conect.read_very_eager().decode( 'ascii' )
        arquivo = open( 'C:\\Users\\cs305672\\PycharmProjects\\SACER\\venv\\src\\log_gre_ssantos.txt', 'a' )
        arquivo2 = open( 'C:\\Users\\cs305672\\PycharmProjects\\SACER\\venv\\src\\log_saida_gre_ssantos.txt', 'w' )
        data = datetime.datetime.now().strftime( '%d/%m/%Y as %H:%M:%S' )
        arquivo.write( f'Desativação da interface de {self.site} realizada em {data}' )
        arquivo.write( saida )
        arquivo2.write( saida )
        arquivo.write( "\n\n" )
        arquivo.close()
        conect.close()
        self.validar_texto( saida )


    def atv_zpt(self):

        self.site = 'ZPT'
        host = '10.255.27.94'
        print( f"conectando ao host {host}..." )
        sleep( 2 )
        conect = telnetlib.Telnet( host, 23, 3 )
        print( 'Conectado!' )
        conect.read_until( b'Login:', 60 )
        conect.write( b"raisecom\r\n" )
        conect.read_until( b'Password:', 60 )
        conect.write( b"raisecom\r\n" )
        conect.write( b"enable\r\n" )
        conect.write( b"raisecom\r\n" )
        conect.write( b"conf t\r\n" )
        conect.write( b"interface port 2\r\n" )
        conect.write( b"no shutdown\r\n" )
        conect.write( b"exit\r\n" )
        conect.write( b"exit\r\n" )
        sleep( 5 )
        conect.write( b"show interface port-list 2\r\n" )
        sleep( 2 )
        saida = conect.read_very_eager().decode( 'ascii' )
        arquivo = open( 'C:\\Users\\cs305672\\PycharmProjects\\SACER\\venv\\src\\log_gre_ssantos.txt', 'a' )
        arquivo2 = open( 'C:\\Users\\cs305672\\PycharmProjects\\SACER\\venv\\src\\log_saida_gre_ssantos.txt', 'w' )
        data = datetime.datetime.now().strftime( '%d/%m/%Y as %H:%M:%S' )
        arquivo.write( f'Desativação da interface de {self.site} realizada em {data}' )
        arquivo.write( saida )
        arquivo2.write( saida )
        arquivo.write( "\n\n" )
        arquivo.close()
        conect.close()
        self.validar_texto( saida )


    def atv_zev(self):
        self.site = 'ZEV'
        host = '10.255.27.94'
        print(f"conectando ao host {host}...")
        sleep(2)
        conect = telnetlib.Telnet( host, 23, 3 )
        print('Conectado!')
        conect.read_until( b'Login:', 60 )
        conect.write( b"raisecom\r\n" )
        conect.read_until( b'Password:', 60 )
        conect.write( b"raisecom\r\n" )
        conect.write( b"enable\r\n" )
        conect.write( b"raisecom\r\n" )
        conect.write( b"conf t\r\n" )
        conect.write( b"interface port 6\r\n" )
        conect.write( b"no shutdown\r\n" )
        conect.write( b"exit\r\n" )
        conect.write( b"exit\r\n" )
        sleep( 5 )
        conect.write( b"show interface port-list 6\r\n" )
        sleep( 2 )
        saida = conect.read_very_eager().decode( 'ascii' )
        arquivo = open('C:\\Users\\cs305672\\PycharmProjects\\SACER\\venv\\src\\log_gre_ssantos.txt', 'a')
        arquivo2 = open( 'C:\\Users\\cs305672\\PycharmProjects\\SACER\\venv\\src\\log_saida_gre_ssantos.txt', 'w' )
        data = datetime.datetime.now().strftime( '%d/%m/%Y as %H:%M:%S' )
        arquivo.write( f'Desativação da interface de {self.site} realizada em {data}' )
        arquivo.write( saida )
        arquivo2.write( saida )
        arquivo.write( "\n\n" )
        arquivo.close()
        conect.close()
        self.validar_texto(saida)


    def atv_zga(self):

        self.site = 'ZGA'
        host = '10.255.27.94'
        print( f"conectando ao host {host}..." )
        sleep( 2 )
        conect = telnetlib.Telnet( host, 23, 3 )
        print( 'Conectado!' )
        conect.read_until( b'Login:', 60 )
        conect.write( b"raisecom\r\n" )
        conect.read_until( b'Password:', 60 )
        conect.write( b"raisecom\r\n" )
        conect.write( b"enable\r\n" )
        conect.write( b"raisecom\r\n" )
        conect.write( b"conf t\r\n" )
        conect.write( b"interface port 4\r\n" )
        conect.write( b"no shutdown\r\n" )
        conect.write( b"exit\r\n" )
        conect.write( b"exit\r\n" )
        sleep( 5 )
        conect.write( b"show interface port-list 4\r\n" )
        sleep( 2 )
        saida = conect.read_very_eager().decode( 'ascii' )
        arquivo = open( 'C:\\Users\\cs305672\\PycharmProjects\\SACER\\venv\\src\\log_gre_ssantos.txt', 'a' )
        arquivo2 = open( 'C:\\Users\\cs305672\\PycharmProjects\\SACER\\venv\\src\\log_saida_gre_ssantos.txt', 'w' )
        data = datetime.datetime.now().strftime( '%d/%m/%Y as %H:%M:%S' )
        arquivo.write( f'Desativação da interface de {self.site} realizada em {data}' )
        arquivo.write( saida )
        arquivo2.write( saida )
        arquivo.write( "\n\n" )
        arquivo.close()
        conect.close()
        self.validar_texto( saida )


if __name__ == "__main__":
    app = SacerApp()
    app.geometry("800x600")
    app.resizable(0,0)
    app.mainloop()
