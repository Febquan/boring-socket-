import socket
import threading
from requests import NullHandler
from tkinter import *
from tkinter.font import Font
import tkinter.ttk as exTk
import os
import datetime
class Client :
    def __init__(self):
        # self.PORT = 5050
        # self.SERVER = socket.gethostbyname(socket.gethostname())
        #----------------------------------------------------------------------------------------SOCKET
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client.connect((self.SERVER,self.PORT))
        #----------------------------------------------------------------------------------------UI
        self.screen= Tk();
        self.screen.title("Client")
        self.screen.geometry("800x500")
        self.screen.resizable(width=False,height=False)
        self.screen.rowconfigure(0, weight=1)
        self.screen.columnconfigure(0, weight=1)
        self.screen.protocol("WM_DELETE_WINDOW", self.offline)

        csfont = {'fontname':'Comic Sans MS'}
        bigfont=Font(family="Helvetica",size=24)
        labfont=Font(family="Helvetica",size=10)
        #----------------------------------------------------------------------------------------UI SERVER CONNECT
        self.serverconnF=Frame(self.screen)
        self.serverconnF.grid(row=0,column=0,sticky='nsew')
        lab_s1=Label(self.serverconnF,text="SEVER IP:", font=labfont)
        lab_s1.pack()
        #bd bg image
        lab_sport=Label(self.serverconnF,text="SEVER PORT:",font=labfont)
        lab_sport.pack()
        self.entry_S_Ip=Entry(self.serverconnF,width=20,font=labfont)
        self.entry_S_Port=Entry(self.serverconnF,width=20,font=labfont)

        self.S_notic=Label(self.serverconnF,text="")
        self.S_notic.pack()
        btn_Sconn=Button(self.serverconnF,text="Connect",command= self.connsever)
        self.S_notic.pack()

        lab_s1.place(x=130,y=160)
        lab_sport.place(x=130,y=240)
        self.S_notic.place(x=170,y=290)
        btn_Sconn.place(x=170,y=320) 
        self.entry_S_Ip.place(x=130,y=190)
        self.entry_S_Port.place(x=130,y=270)
        
        #----------------------------------------------------------------------------------------UI LOGIN
        self.loginF= Frame(self.screen)
        self.loginF.grid(row=0,column=0,sticky='nsew')
        
        lab_login=Label(self.loginF,text="Login",font=bigfont).pack(pady=50)
        lab_l1=Label(self.loginF,text="username",font=labfont).pack()
        self.loginF_user=Entry(self.loginF)
        self.loginF_user.pack()
        lab_l2=Label(self.loginF,text="password",font=labfont).pack()
        self.loginF_passw=Entry(self.loginF)
        self.loginF_passw.pack()
        self.Lnotic=Label(self.loginF,text="",bg="light yellow")
        self.Lnotic.pack()
        btn_log=Button(self.loginF,text='login',command= self.login).pack(pady=5)
        btn_signup=Button(self.loginF,text='sign up',command=lambda: self.swap(self.signupF)).pack()

        #----------------------------------------------------------------------------------------UI SIGNUP
        self.signupF= Frame(self.screen)
        self.signupF.grid(row=0,column=0,sticky='nsew')
        lab_si1=Label(self.signupF,text="Signup",font=bigfont).pack(pady=50)
        lab_siusername=Label(self.signupF,text="User name").pack()
        self.sientry_user=Entry(self.signupF)
        self.sientry_user.pack()
        lab_si2=Label(self.signupF,text="password").pack()
        self.sientry_passw=Entry(self.signupF,show='*')
        self.sientry_passw.pack()
        lab_si3=Label(self.signupF,text=" rewrite password").pack()#bd bg image
        self.sientry_repassw=Entry(self.signupF,show='*')
        self.sientry_repassw.pack()
        self.sinotic=Label(self.signupF,text="",bg="light yellow")
        self.sinotic.pack()
        btn_sicreate=Button(self.signupF,text="Create account",command=self.signup)
        btn_sicreate.pack()
        # pas1=self.entry_passw.get()
        # pas2=self.entry_repassw.get()
        # if pas1!=pas2:
        #     self.notic["text"]="Pass incorrect"
        #----------------------------------------------------------------------------------------UI HOMEPAGE
        self.homepageF=Frame(self.screen)
        self.homepageF.grid(row=0,column=0,sticky='nsew')
        lab_h1=Label(self.homepageF,text="Tra cứu giá vàng",font=bigfont)#bd bg image
        btn_logout=Button(self.homepageF,text="log out",command=self.logout)
        # frame_hscroll=Frame()
        # frame_hscroll.place(y=50,x=0)
        # scrollbar = Scrollbar(self.homepageF,width=40,orient=VERTICAL)
        # scrollbar.pack( fill = Y )
        lab_hday=Label(self.homepageF,text="Day:")
        lab_hday.place(x=10,y=60)
        self.combo_hday=exTk.Combobox(self.homepageF)
        
        
        
        # self.combo_hday.insert(0,"dd/mm/yyyy")
        #--------------------------------------get day
        def day(x):
            a = datetime.datetime.today()-datetime.timedelta(days = x)
            if (a.day<10) : day1='0'+str(a.day)+'/'
            else: day1=str(a.day)+'/'
            if (a.month<10):day1=day1+'0'+str(a.month)+"/"
            else:day1+=str(a.month)+'/'
            day1+=str(a.year)
            return day1
        dateList = []
        for i in range(10):
            dateList.append(day(i))
        self.combo_hday['values']=dateList
        self.combo_hday.current(0)
        
        
        # self.combo_hday.insert()
        # self.entry_day=Entry(self.homepageF)
        self.combo_hday.place(x=60,y=60)
        lab_gold=Label(self.homepageF,text="GOLD:")
        lab_gold.place(x=10,y=30)
        self.entry_gold=Entry(self.homepageF)
        self.entry_gold.place(x=60,y=30)
        self.hnotic=Label(self.homepageF,text="")
    
        btn_hsrch=Button(self.homepageF,text="SEARCH",command=self.search)
        btn_hsrch.place(x=370,y=50)
        self.hnotic.place(x=150,y=90)
        self.mylist = Listbox(self.homepageF ,width=90,height=17)#,  yscrollcommand = scrollbar.set 
    
        self.mylist.place(y=120,x=35)
        # scrollbar.config( command = self.mylist.yview )
        lab_h1.pack()
        btn_logout.place(x=700,y=20)
        #----------------------------------------------------------------------------------------Recieve Message form server 
        self.Servermsg=''
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        #----------------------------------------------------------------------------------------Start 
        self.swap(self.serverconnF)  
        self.screen.mainloop()
  
    
    #----------------------------------------------------------------------------------------TESTING
    def receviveServerMess(self):
        try:
            while True:

                self.Servermsg=self.recieve(self.client)
                print (self.Servermsg)                
        except:
            print("lol")

    #----------------------------------------------------------------------------------------Các hàm công cụ
    def lengthmsg(self,msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        return send_length
    def send(self,msg,conn): # Hàm gửi tin nhắn đến server 
        send_length = self.lengthmsg(msg)
        conn.sendall(send_length)
        conn.sendall(msg.encode(self.FORMAT))
    def recieve(self,conn):
        msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(self.FORMAT)
            return msg

    def swap(self,frame) :
        frame.tkraise()

    def start(self): # test
        while (True):
            msg=input("Chat: ");
            try:
                if(msg=='end'):
                    break;
                self.send(msg,self.client);
            except:
                try:
                    self.connsever()
                except:
                    print("Server khong co ket noi")

        self.client.send(self.DISCONNECT_MESSAGE)
    #----------------------------------------------------------login function 
    def login(self):
        user=self.loginF_user.get()
        passw=self.loginF_passw.get()
        try :
            request="login"
            self.send(request,self.client)
            self.send(user ,self.client)
            self.send(passw ,self.client)
            msg=self.recieve(self.client)
            print(f'Server:\n {msg}')
            if msg=="Dang nhap thanh cong" :
                self.swap(self.homepageF)
            else :
                self.Lnotic["text"]=msg
        except:
            try:
                if self.connsever() :
                    self.Lnotic["text"]="Server is now online"
                else :
                    self.Lnotic["text"]="Server is now offline"
            except:
                    pass
    #----------------------------------------------------------Signup function     
    def signup (self):
        user=self.sientry_user.get()
        passw=self.sientry_passw.get()
        repswd=self.sientry_repassw.get()
        if user=="" or passw=="" or repswd=="":
            self.sinotic["text"]="Fields cannots be empty"
            return 
        if passw!=repswd:
            self.sinotic["text"]="Nhập pass không khớp"
            return 
        try:
            request="signup"
            self.send(request,self.client)
            self.send(user ,self.client)
            self.send(passw ,self.client)
            msg=self.recieve(self.client)
            print(f'Server:\n {msg}')
            if msg=="Dang ky thanh cong" :
                self.sientry_user.delete(0, END)
                self.sientry_passw.delete(0, END)
                self.sientry_repassw.delete(0, END)
                self.swap(self.loginF)
            else :
                self.sinotic["text"]=msg
                return 

        except:
            try:
                if self.connsever() :
                    self.sinotic["text"]="Server is now online"
                else :
                    self.sinotic["text"]="Server is now offline"
            except:
                    pass
                
    #----------------------------------------------------------connect server  function     
    def connsever(self):
        host=self.entry_S_Ip.get() 
        port=self.entry_S_Port.get()
        if host=="" or port=="":
            self.S_notic["text"]="Cant be empty"
        else:
            try:
                # socket.gethostbyname(socket.gethostname())
                ADDR = (host, int(port))
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect(ADDR)
                self.swap(self.loginF)
                return True
            except:
                self.S_notic["text"]="Cant connect"
                return False
    #----------------------------------------------------------search  function     
    def search(self):
        self.mylist.delete(0,END)
        gold=self.entry_gold.get()
        date=self.combo_hday.get()
        print(date)
        try :
            request="search"
            self.send(request,self.client)
            self.send(gold,self.client)
            self.send(date ,self.client)
            msg=self.recieve(self.client)
            print(f'Server:\n{msg}')
            data=msg.split("\n")
            for line in data:
             self.mylist.insert(0,line)
        except:
            print("Server hien dang offline")
            try:
                self.connsever()
            except:
                pass
     #----------------------------------------------------------logout function 
    def logout (self):
        self.swap(self.loginF) 
    def offline(self):#Hàm xử lý khi logout
        self.screen.destroy()
        os._exit(0)    
        


B=Client()

    

