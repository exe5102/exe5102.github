from database import *
from function import *
from flask import Flask
from flask import request
from flask import url_for, redirect
from flask import session
from flask import render_template
import time
import datetime

today = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))# 轉換時區 -> 東八區
dtoday = datetime.datetime.strptime(today.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')

BuildDB()
RecordDB()
TSData ={'uphone':'',"pnumber":"",'unumber':'','stime':''}


app=Flask(__name__)
app.config['SECRET_KEY'] = 'Final-Projuct'
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/", methods=['GET', 'POST'])    #客戶訂位系統
def index():
    TSData.clear()
    Statechenk()
    Stateload()
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])   #輸入資料
def login():
    Statechenk()
    Stateload()
    if request.method == 'POST':
        unumber = request.form['unumber']
        uphone = request.form['uphone']
        if unumber == "" or  uphone == "":
            return redirect(url_for('failed'))
        else:
            TSData.update({"unumber":unumber,'uphone':uphone})
            return redirect(url_for('Select'))
    return render_template('enter.html')

@app.route("/Select", methods=['GET', 'POST'])          #選擇車位
def Select():
    Statechenk()
    Stateload()
    if request.method == 'POST':
        pnumber = request.form['pnumber']
        if pnumber != "":
            TSData.update({"pnumber":pnumber,'stime':DateControl()})
            ClientBK(TSData['uphone'],TSData['pnumber'],TSData['unumber'],TSData['stime'],1)
            return redirect(url_for('Success'))
    return render_template('select.html',State=[BKstate['1'],BKstate['2'],BKstate['3'],BKstate['4']])

@app.route("/failed")   #客戶訂位失敗
def failed():
    Statechenk()
    Stateload()
    return render_template('ResultFail.html')

@app.route("/success")  #客戶訂位成功
def Success():
    Statechenk()
    Stateload()
    return render_template('ResultSuccess.html',DBfatch= ClientSearch(TSData['unumber']))

@app.route("/Payment", methods=['GET', 'POST'])  #繳費
def Payment():
    Statechenk()
    Stateload()
    if request.method == 'POST':
        unumber = request.form['Unumber']
        spaceamount = request.form['amount']
        try:
            if  unumber != '' and spaceamount != '':
                data = ClientSearch(unumber)
                if data != None or data[4] == '2':
                    useramount = int(spaceamount)
                    amount = Compute(unumber)
                    total = useramount - amount
                    if total < 0:
                        return redirect(url_for('failed'))              #尚未更改網頁導向(繳費失敗)
                    else:
                        StateReset(data[2])
                        RecordLogin(data[2],data[0],data[3],DateControl(),amount,'繳費成功')
                        AdminDelete(unumber)
                        return redirect(url_for('index'))            #尚未更改網頁導向(繳費成功)
                else:
                    return redirect(url_for('failed'))              #尚未更改網頁導向(繳費失敗)
        except ValueError:
            return redirect(url_for('failed'))                  #尚未更改導向網頁(金額輸入錯誤)
    return render_template('Payment.html')
    
@app.route("/Report", methods=['GET', 'POST'])  #客戶報到
def report():
    Statechenk()
    Stateload()
    if request.method == 'POST':
        unumber = request.form['unumber']
        pnumber = request.form['pnumber']
        data = ClientSearch(unumber)
        if data != None and data[1] == pnumber:
            # Arduino(data[1])                            #未完成
            ClientEdit(data[0],data[1],data[2],data[3],'2')
            return redirect(url_for('index'))         #尚未更改網頁導向(報到成功)
        else:
            return redirect(url_for('failed'))          #尚未更改網頁導向(報到失敗)
    return render_template('Report.html')

@app.route("/search", methods=['GET', 'POST'])  #客戶查詢訂單
def search():
    Statechenk()
    Stateload()
    if request.method == 'POST':
        unumber = request.form['Unumber']
        data = ClientSearch(unumber)
        if data != None:
            amount = Compute(unumber)
            return render_template('search.html',DBfatch= data,Pamount = amount)
        else:
            return redirect(url_for('failed'))      #尚未更改網頁導向(查詢失敗)
    return render_template('search.html')

@app.route("/adminhomepage")   #管理端主頁
def Administration():
    Statechenk()
    Stateload()
    if "loginAdminId" in session:
        return render_template('Admin.html',account = session['loginAdminId'])
    return render_template('msg.html', msg = '請從主頁登入')

@app.route("/adminlogin", methods=['GET', 'POST'])   #管理端登入
def Adminlogin():
    Statechenk()
    Stateload()
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        if AdminCheck(account, password) == True:
            session['loginAdminId'] = account
            return redirect(url_for('Administration'))
        return render_template('msg.html', msg = '帳號密碼錯誤')
    return render_template('login.html')

@app.route("/adminlogout")    #管理端登出
def Adminlogout():
    Statechenk()
    Stateload()
    session.pop("loginAdminId", None)
    return redirect(url_for('index'))

@app.route("/admindelete" ,methods=['GET', 'POST'])  #管理端取消訂單
def Admindelete():
    Statechenk()
    Stateload()
    if "loginAdminId" in session:
        if request.method == 'POST':
            unumber = request.form['Unumber']
            Data = ClientSearch(unumber)
            if Data == None:
                return redirect(url_for('failed'))              #尚未改正網頁導向
            else:
                RecordLogin(Data[2],Data[0],Data[3],DateControl(),0,'管理端取消')
                AdminDelete(unumber)
                return render_template('ResultDelete.html', DBfatch= Data )
        return render_template('AdminDelete.html')
    return render_template('msg.html', msg = '請從主頁登入')

@app.route("/adminsearch" ,methods=['GET', 'POST']) #管理端查詢指定客戶訂單
def Adminsearch():
    Statechenk()
    Stateload()
    if "loginAdminId" in session:
        if request.method == 'POST':
            unumber = request.form['Unumber']
            if ClientSearch(unumber) == None:
                return redirect(url_for('failed'))
            else:
                amount = Compute(unumber)
                return render_template('AdminSearch.html',DBfatch=ClientSearch(unumber), Pamount = amount)
        return render_template('AdminSearch.html')
    return render_template('msg.html', msg = '請從主頁登入')

@app.route("/adminalldata")  #管理端列出所有資料           
def AdminAlldata():
    Statechenk()
    Stateload()
    if "loginAdminId" in session:
        data = SearchAll()
        print(data)
        if data == None:
            return render_template('AdminAllBooking.html')
        else:
            for i in range(0,len(data)):
                print(data[i][2])
                amuont = Compute(data[i][2])
                if amuont == None:
                    amuont = 0
                data[i][4] = amuont
            return render_template('AdminAllBooking.html' ,DBfatch=data)
    return render_template('msg.html', msg = '請從主頁登入')

@app.route("/adminlog")  #管理端列出所有紀錄          
def Adminlog():
    Statechenk()
    Stateload()
    if "loginAdminId" in session:
        return render_template('Adminlog.html' ,DBfatch=LogAll())
    return render_template('msg.html', msg = '請從主頁登入')