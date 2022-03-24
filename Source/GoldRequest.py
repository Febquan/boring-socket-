import time

import requests
import json
import datetime
from threading import Timer
import os
#tag : server request

APIURL = 'https://tygia.com/json.php?ran=0&rate=0&gold=1&bank=VIETCOM&date=now'


'''
Không làm ngưng nhận data nha , kiểu chỉ có 3 ngày thôi ấy, sau 3 ngày thì xóa cũ nhất thêm mới vào , bỏ cái tính năng này 
Lấy dữ liệu vô tận 
Hướng dẫn sử dụng 
** new :    cách gọi hàm không có gì thay đổi trừ hàm Generater_Base_Using_Data() có thêm chức năng 
            Clock làm việc ngay lập tức 1 lần, sau đó cứ 30' làm 1 lần // bỏ tính năgn làm ở phút 15, 45
_ gọi 1 lần ở phần main của server :
    +Generater_Base_Using_Data() //***new : chỉnh range ở dòng số 54 để có số ngày ít nhất ở trong database 
    +Truyền 1 list rỗng cho Gold_Exchange_refresh_Clock(30) //30' 
        ví dụ :
        Clock=[]
        Gold_Exchange_refresh_Clock(Clock,30)
    Sau đó gọi bắt đầu : // Có chạy thử ở dưới 
        Clock[0].start() 
    để bắt đầu quá trình 30' refresh 1 lần  
   
_ khi kết thúc chương trình :
        Clock[0]..cancel
        để kết thúc quá trình 30' refresh 1 lần  
_ tùy thích sử dụng : 
     + Day_token, Gold_token 
     Đưa ra các giá trị mà người dùng có thể tìm kiếm 
     +Search_for_day, Search_for_gold_during_day dựa trên : 
     self.data= api.getdictformapi(date)
     self.send(api.strdata(self.data,gold),conn)
- không cần thiết, đừng bao giờ gọi : 
    +_data_encode
    +_data_decode
    +Request_Gold_Exchange_Rate
    +*new : Refresh_data
*Thư mục lưu data : thư mục hiện tại / GoldEx / 
'''
#Đã test toàn bộ, bị lỗi alo là có mặt

def Generater_Base_Using_Data():  ########### Main function
    if os.path.exists('./GoldEx') :
        ''
    else:
        path = os.path.join('./', 'GoldEx')
        os.mkdir(path)
    now=datetime.datetime.now()
    Available_day=Day_token()
    date=now
    for i in range(10) :
        date_str=date.strftime('%d/%m/%Y')
        print(date_str)
        Refresh_data(date_str)
        date=date-datetime.timedelta(days=1)

def Get_Real_time(TimeFormat): ########### Dont call it
    now = datetime.datetime.now()
    current_time = now.strftime(TimeFormat)
    return current_time

def _data_encode(item,file_address): ########### Dont call it
    if item=='':
        return
    item=json.dumps(item)
    st=bytearray(item.encode('utf8'))
    for i in range(len(st)):
        if st[i] <= 60:
            st[i] += 60
        elif st[i] <= 120:
            st[i] -= 60
        elif st[i] <= 180:
            st[i] += 60
        elif st[i] <= 240:
            st[i] -= 60
    st.append(58)
    st.append(58)
    st.append(58)
    st.append(58)
    st = bytes(st)
    jsonFile = open(file_address, "wb")
    jsonFile.write(st)
    jsonFile.close()

def _data_decode(file_address): ########### Dont call it
    f=open(file_address,'rb')
    mess=f.read()
    f.close()
    re=bytearray(mess)
    for i in range(len(re)):
        if re[i] <= 60:
            re[i] += 60
        elif re[i] <= 120:
            re[i] -= 60
        elif re[i] <= 180:
            re[i] += 60
        elif re[i] <= 240:
            re[i] -= 60
    re.pop()
    re.pop()
    re.pop()
    re.pop()
    bytes(re)
    return(json.loads(re.decode('unicode-escape')))

def Request_Gold_Exchange_Rate(url=''): ########### Dont call it
    if url=='' :
        url = APIURL
    resp = requests.get(url)
    resp.encoding='utf-8-sig'
    content = resp.text.encode().decode('utf-8-sig')
    try:
        return json.loads(content)["golds"][0]['value']
    except :
        return ""

def Refresh_data(date='now'):
    if(date!='now'):
        date = date.replace('/', '_')
        date = date.replace('.', '_')
        date = date.replace('-', '_')
        date = date.split('_')[::-1]
    url=APIURL.replace('now','')
    url=f'{url}{"".join(date)}'
    print(url)
    item = Request_Gold_Exchange_Rate(url)
    if os.path.exists('./GoldEx'):
        if(date=='now'):
            date = Get_Real_time('%Y_%m_%d')
        else:
            date='_'.join(date)
        if item=='' :
            print('Refresh cancel')
            return
        else :
            print('pass')
        for i in item :
            i['day']="/".join(date.split('_')[::-1])
        if not os.path.exists('./GoldEx/' + date):
            path = os.path.join('./GoldEx', date)
            os.mkdir(path)
        files_in_directory = os.listdir('./GoldEx/' + date)
        filtered_files = [file for file in files_in_directory if file.endswith(".SuongQuanSon")]
        if 'backup.SuongQuanSon' in filtered_files:
            path_to_file = os.path.join('./GoldEx/' + date, 'backup.SuongQuanSon')
            os.remove(path_to_file)
        if 'late_data.SuongQuanSon' in filtered_files:
            new_file = os.path.join('./GoldEx/' + date, 'backup.SuongQuanSon')
            old_file = os.path.join('./GoldEx/' + date, 'late_data.SuongQuanSon')
            os.rename(old_file, new_file)
        file_address = os.path.join('./GoldEx/' + date, 'late_data.SuongQuanSon')
        _data_encode(item, file_address)
        print('Server updated')
    else:
        print("Sever is killed")


def Gold_Exchange_refresh_Clock(clock,mi): ################# once
    def Refresh_real_time_data(minu):
        Refresh_data()
        nextTime = datetime.datetime.now() + datetime.timedelta(minutes=minu)
        dateString = nextTime.strftime('%d-%m-%Y %H-%M-%S')
        newDate = nextTime.strptime(dateString, '%d-%m-%Y %H-%M-%S')
        delay = (newDate - datetime.datetime.now()).total_seconds()
        clock[0]=Timer(delay,Refresh_real_time_data,([minu]))
        clock[0].start()
    nextTime = datetime.datetime.now()
    dateString = nextTime.strftime('%d-%m-%Y %H-%M-%S')
    newDate = nextTime.strptime(dateString, '%d-%m-%Y %H-%M-%S')
    delay = (newDate - datetime.datetime.now()).total_seconds()
    clock.append(Timer(delay,Refresh_real_time_data,([mi])))

def Day_token():
    try:
        files_in_directory = os.listdir('./GoldEx')
        for i in range(len(files_in_directory)) :
            files_in_directory[i]="/".join(files_in_directory[i].split('_')[::-1])
        return files_in_directory
    except:
        print('All down')
        return []

def Gold_token():
    try :
        loaded = _data_decode('./GoldEx/' + Get_Real_time('%Y_%m_%d') + '/late_data.SuongQuanSon')
    except :
        try :
            loaded=[]
            files_in_directory = os.listdir('./GoldEx')
            for files in files_in_directory :
                try:
                    if(files==Get_Real_time('%Y_%m_%d')) :
                        continue
                    loaded = loaded + _data_decode('./GoldEx/' + files + '/late_data.SuongQuanSon')
                    break
                except:
                    pass
        except :
            print('All down')
            return []
    gole = []
    for i in loaded:
        if not i['type'] in gole:
            gole.append(i['type'])
    return gole

def Search_for_day(date='now'):
    if(date == 'now'):
        date=Get_Real_time('%d_%m_%Y')
    date=date.replace('/','_')
    date=date.replace('.', '_')
    date=date.replace('-', '_')
    date = date.split('_')[::-1]
    date="_".join(date)
    print(date)
    try :
        loaded = _data_decode('./GoldEx/' + date + '/late_data.SuongQuanSon')
    except:
        try:
            loaded = _data_decode('./GoldEx/' + date + '/bakup.SuongQuanSon')
        except:
            loaded=''
    return loaded

def Search_for_gold_during_day(data, gold) :
    if data=='' :
        return 'Khong co du lieu hoac nhap sai cau truc ngay thang'
    mess=''
    for i in data :
        if gold in i['type']  :
            mess= mess + "\n Buy:  {0}  Sell:{1} , Gold type : {2} , Date: {3} Des: {4}".format(i['buy'],i['sell'],i['type'],i['day'],i['brand'])
    if mess=='' : mess="Khong co du lieu"
    return mess

# Generater_Base_Using_Data()
# # # loaded=_data_decode('./GoldEx/'+Get_Real_time('%Y_%m_%d')+'/late_data.SuongQuanSon')
# # # print(loaded)
# # print(Gold_token())
# # print(Day_token())
# # print(Get_Real_time(TimeFormat="%Y:%m:%d:%H:%M:%S"))
# # #Refresh_data('12/12/2021')
# print(Search_for_gold_during_day(Search_for_day('12/12/2021'),'SJC'))
# Clock=[]
# Gold_Exchange_refresh_Clock(Clock,30)
# Clock[0].start()
# # time.sleep(60*60*2)
# # Clock[0].cancel()