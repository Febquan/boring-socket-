import os
import sqlite3
#tag : Server database

'''
Hướng dẫn sử dụng 
_ gọi 1 lần ở phần main của server :
    +Generater_Server_User_Data()
_ tùy thích sử dụng : 
    +Check_User_Password
    +Password_Changer
    +Sign_Up_Data_To_Server
_ dành cho Debug : 
    +Reset_Server
    +Data_User_Prints
- không cần thiết, đừng bao giờ gọi : 
    +Check_Server_User_Data_Exists
    +Search_User
    +Get_Real_time
- Admin tag : không khuyến khích
'''
#Đã test toàn bộ, bị lỗi alo là có mặt

def Check_Server_User_Data_Exists():   ########### Dont call it
    if(os.path.exists('./Uuser.db')) :
        return True
    else :
        return False
def Generater_Server_User_Data():  ########### Main function
    if(Check_Server_User_Data_Exists()):
        return
    else:
        db_path = os.path.join("./Uuser.db")
        conn = sqlite3.connect(db_path)
        conn.execute('''CREATE TABLE USERSTORAGE
                 (ID TEXT NOT NULL,
                 USERNAME TEXT NOT NULL,
                 PASSWORD TEXT NOT NULL);''')
        conn.commit()
        with conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO USERSTORAGE VALUES(?,?,?)", ('MANAGER', 'quanquan', '123'))
            conn.commit()
        conn.close()
        print('User_base created')
        return
def Search_User(Username):   ############# Dont call it
    if(not Check_Server_User_Data_Exists()):
        return 'No base data found'
    db_path = os.path.join("./Uuser.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM USERSTORAGE")
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM USERSTORAGE")
        while True:
            row = cur.fetchone()
            if row == None:
                title= 'Not yet'
                break
            if row[1] == Username:
                title= 'Already exists'
                break
    con.close()
    return title
def Data_User_Prints():   ################# Check all available user
    if (not Check_Server_User_Data_Exists()):
        return 'No base data found'
    db_path = os.path.join("./Uuser.db")
    con = sqlite3.connect(db_path)

    cur = con.cursor()
    cur.execute("SELECT * FROM USERSTORAGE")
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM USERSTORAGE")
        while True:
            row = cur.fetchone()
            if row == None:
                 break
            print(row)
    return
def Check_User_Password(Username,Password):  ########### Main function
    if(not Check_Server_User_Data_Exists()):
        return 'No base data found'
    if(Search_User(Username)!='Already exists'):
        return 'Không tồn tại tài khoản này'
    db_path = os.path.join("./Uuser.db")
    con = sqlite3.connect(db_path)

    cur = con.cursor()
    cur.execute("SELECT * FROM USERSTORAGE")
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM USERSTORAGE")
        while True:
            row = cur.fetchone()
            if row == None:
                title= 'Wrong Username'
                break
            if row[1] == Username:
                if (row[2] == Password):
                    title= 'Accept'
                    break
                else:
                    title= 'Wrong Password'
                    break

    con.close()
    return title
def Password_Changer(Username,NewPassword):   ########### Main function
    if (not Check_Server_User_Data_Exists()):
        return 'No base data found'
    if(Search_User(Username)!='Already exists'):
        return 'Wrong Username'
    db_path = os.path.join("./Uuser.db")
    con = sqlite3.connect(db_path)

    with con:
        cur = con.cursor()
        cur.execute("UPDATE DATABASE SET PASSWORD=? WHERE USERNAME=?", (NewPassword, Username))
        con.commit()
    con.close()
    return 'Done'
def Sign_Up_Data_To_Server(Username,Password):  ########### Main function
    if (not Check_Server_User_Data_Exists()):
        return 'No base data found'
    if(Search_User(Username)=='Already exists'):
        return 'Tài khoản này đã tồn tại'
    Id=Get_Real_time(TimeFormat="%Y%m%d%H%M%S") # +client ID
    db_path = os.path.join("./Uuser.db")
    con = sqlite3.connect(db_path)
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO USERSTORAGE VALUES(?,?,?)", (Id, Username, Password))
    con.close()
    return 'Accept'

def Get_Real_time(TimeFormat):
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime(TimeFormat)
    return current_time

#tag :  Admin server config
def Reset_Server():
    if(Check_Server_User_Data_Exists()):
        os.remove('./Uuser.db')
    files_in_directory = os.listdir('./')
    filtered_files = [file for file in files_in_directory if file.endswith(".SuongQuanSon")]
    for file in filtered_files:
        path_to_file = os.path.join('./', file)
        os.remove(path_to_file)

def Admin_Power_Checker(AdminAccount,AdminPassWord):
    if(AdminAccount!='m4n4g3r#@'):
        #block connect in secs
        #something goes here
        return False
    else :
        if(not Check_Server_User_Data_Exists()):
            return False
        else :
            if(Check_User_Password(AdminAccount,AdminPassWord)=='Accept'):
                return True
            else :
                #block connect in secs
                #something goes here
                return False
def Admin_Reset(AdminAccount,AdminPassWord):
    if(Admin_Power_Checker(AdminAccount,AdminPassWord)):
        Reset_Server()