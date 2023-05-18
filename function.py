from database import *# from datetime import datetime,timezone,timedelta,datetime
import datetime
from time import sleep
import sys
import serial

today = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))# 轉換時區 -> 東八區
dtoday = datetime.datetime.strptime(today.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')

BKstate ={'1':'0',"2":"0",'3':'0','4':'0'}

def DateControl():                                          #時間格式
    str1 = ''.join(today.strftime("%Y-%m-%d %H:%M:%S"))
    return str1

def Compute(unumber):                                       # 定價
    a = ClientSearch(unumber)
    if a[4] == '2':
        d = str(a[3])
        dbtime = datetime.datetime.strptime(d,'%Y-%m-%d %H:%M:%S')
        e = dtoday - dbtime
        if e.days==0:
            return int(e.seconds/1800)*30 
        elif (dtoday.hour*20+int(dtoday.minute/30)*10) > 100:
            return (e.days+1)*100
        else:
            return e.days*100+dtoday.hour*20+int(dtoday.minute/30)*10
    else:
        return ''
def Statechenk():                 #狀態確認 
    data = SearchAll()
    if len(data) > 0:
        for record in data:
            if record[4] == '1': 
                Transform = datetime.datetime.strptime(record[3],'%Y-%m-%d %H:%M:%S')
                TimeLimit = Transform + datetime.timedelta(minutes=15)
                t = dtoday - TimeLimit       
                if t.seconds > 0 and t.days >= 0:
                    RecordLogin(record[2],record[0],record[3],TimeLimit,None,'未報到')
                    AdminDelete(record[2])
                print(t.days)
            else:
                print(record[4])
    print(BKstate)

def Stateload():                 #狀態讀取
    data = SearchAll()
    if len(data) > 0:
        for record in data:
            BKstate.update({record[1]:record[4]})
    print(BKstate)
    return BKstate

def Arduino(choice):                                #未完成

    COM_PORT = 'COM4'  # 根據連結的Arduino的通訊埠修改設定
    BAUD_RATES = 9600
    Ser = serial.Serial(COM_PORT, BAUD_RATES)
    try:
        if choice == '1':
            print('傳送激磁指令')
            Ser.write(b'ON\n')  # 訊息必須是位元組類型
            sleep(0.5)  # 暫停0.5秒，再執行底下接收回應訊息的迴圈
        elif choice == '2':
            print('傳送關閉指令')
            Ser.write(b'OFF\n')
            sleep(0.5)
        elif choice == 'e':
            Ser.close()
            print('再見！')
            sys.exit()
        else:
            print('指令錯誤…')
        while Ser.in_waiting:
            mcu_feedback = Ser.readline().decode()  # 接收回應訊息並解碼
            print('控制板回應：', mcu_feedback)
    except KeyboardInterrupt:
        Ser.close()
        print('再見！')

def StateReset(pnumber):
    BKstate[f'{pnumber}'] = 0