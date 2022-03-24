
import socket 
import threading
from tkinter import *
from tkinter.font import Font
import os
import UserLog as UL
import GoldRequest as GR
import sqlite3
print("[STARTING] server is starting...")

class Server :
    def __init__(self):
        
        #----------------------------------------------------------SOCKET
        self.HEADER = 64
        self.PORT = 5050
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # tao socket #socket.AF_INET Chap nhan IP4
        self.server.bind(self.ADDR)# Dat ten cho socket
        self.Clients=[]
        self.conns=[]
        # self.USER={'quanquan':'123','lmao':'123'}
        threading.Thread(target=self.start).start() #Tao thread de listen client
        #----------------------------------------------------------CREAT DATA BASE
        UL.Generater_Server_User_Data()    
        GR.Generater_Base_Using_Data()
        Clock=[]
        GR.Gold_Exchange_refresh_Clock(Clock,30)
        Clock[0].start()
        #----------------------------------------------------------GETTING DATA FORM API
        self.data=''
        #----------------------------------------------------------UI
        self.screen= Tk()
        bigfont=Font(family="Helvetica",size=26)
        labfont=Font(family="Helvetica",size=19)
        mesfont=Font(family="Helvetica",size=12)

        self.screen.title("SERVER")
        self.screen.geometry("600x650")
        self.screen.resizable(width=False,height=False)

        self.mes=Label(self.screen,text="Server message",font=mesfont)
        self.mes.place(x=10,y=60)
        lab_ip=Label(self.screen,text="IP: "+self.SERVER,font=labfont)
        lab_port=Label(self.screen,text="Port: "+str(self.PORT),font=labfont)
        lab_ip.place(x=10,y=10)
        lab_port.place(x=200,y=10)
        btn_logout=Button(self.screen,text="log out",command=self.offline)
        
        notic=Label(self.screen,text="")
        self.mylist = Listbox(self.screen ,width=50,height=80)
        self.mylist.place(y=120,x=20)
        btn_logout.place(x=500,y=10)

        self.screen.protocol("WM_DELETE_WINDOW", self.offline)

        self.screen.mainloop();

    def updateUIClient(self,conn,addr,connect) : #Hàm update UI 
        if(connect):
            self.mes.config(text=f"[NEW CONNECTION] {addr} connected\n CONNECTION COUNT:{threading.activeCount() - 3}") 
            self.Clients.append(addr)
            self.conns.append(conn)
        else:
            self.mes.config(text= f"[DISCONNECTION] {addr} disconnected\n CONNECTION COUNT:{threading.activeCount() - 4}")
            self.Clients.remove(addr)
            self.conns.remove(conn)
        self.mylist.delete(0, END)
        for Client in self.Clients:
            self.mylist.insert(END, f"{Client}")

    def handlexcept(self,conn,addr):#Hàm handle lỗi 
        conn.close()    
        self.updateUIClient(conn,addr,False)
        print(f"({addr} just disconected )[ACTIVE CONNECTIONS]  {threading.activeCount() - 4}") 
   
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
    def handle_client(self,conn, addr):#Hàm xử lý từng client
        try:
            self.updateUIClient(conn,addr,True)
            connected = True
            while connected:
                msg=self.recieve(conn)
                print(f"[{addr}] {msg}")
                #----------------------------------------------------------Nơi handle các yêu cầu từ client
                if msg == self.DISCONNECT_MESSAGE:
                    connected = False

                if msg == 'login':#----------------------------login
                    user=self.recieve(conn)
                    passw=self.recieve(conn)
                    print(user,passw)
                    temp =UL.Check_User_Password(user,passw)
                    if temp == "Accept":
                        self.send("Dang nhap thanh cong",conn)
                    else:
                        self.send(temp,conn)
                if msg=='signup':
                    user=self.recieve(conn)
                    passw=self.recieve(conn)
                    print(user,passw)
                    temp =UL.Sign_Up_Data_To_Server(user,passw)
                    if temp == "Accept":
                        self.send("Dang ky thanh cong",conn)
                    else:
                        self.send(temp,conn)
                if msg == 'search':#----------------------------search
                    gold=self.recieve(conn)
                    date=self.recieve(conn)
                    print(gold,date)
                    self.data= GR.Search_for_gold_during_day(GR.Search_for_day(date),gold)
                    print(self.data)
                    self.send(self.data,conn)
                # self.send(api.strdata(self.data,msg),conn)
            self.handlexcept(conn,addr)
        except:
            self.handlexcept(conn,addr)
        
    def offline(self):#Hàm xử lý khi logout
        self.screen.destroy()
        for conn in self.conns:
            conn.send("Server hien da offline".encode(self.FORMAT))
            conn.close()   
        os._exit(0)
        
    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 3}")

A=Server();
