from django.shortcuts import redirect, render
from django.core.mail import EmailMultiAlternatives
from django.http import HttpRequest, JsonResponse,HttpResponseRedirect
from login.settings import EMAIL_HOST_USER
from miku.models import user,EmailValid
import time
from django.contrib.auth.forms import UserCreationForm
import random
from miku.form import RegisterForm,LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from oauth2client.service_account import ServiceAccountCredentials as SAC
import gspread
import datetime



import pymysql
db = pymysql.connect(host='db4free.net', port=3306, user='de45amiku', passwd='110101010', db='de45a_test', charset='utf8')
#db = pymysql.connect(host="localhost", port=3306, user='root', passwd='DE45AMIKU', db='test', charset='utf8')
def writein(NAME,LEFTTIME,JOINTIME):
    with db.cursor() as cursor:
        command = "INSERT INTO time(NAME, LEFTTIME, JOINTIME)VALUES(%s, %s, %s)"
        cursor.execute(command, (str(NAME), str(LEFTTIME), str(JOINTIME)))
        db.commit()

def read():    
    with db.cursor() as cursor:
        command = "SELECT * FROM time"
        cursor.execute(command)
        result = cursor.fetchall()
        return result

def register(request):
   form = RegisterForm()
   result = {"staue": "error", "data": ""}  # 註冊狀態字典
   if request.method == 'POST'and request.POST:
      email = request.POST.get('email')  # 獲取註冊郵箱
      pwd = request.POST.get('id_password1')  # 獲取註冊郵箱
      code = request.POST.get('value')  # 獲取註冊驗證碼
      db_email = EmailValid.objects.filter(email_address=email).first()  # 根據郵箱註冊表中的數據
      form = RegisterForm(request.POST)
      if form.is_valid():
         if db_email:  # 如果表中存在該郵箱
               if code == db_email.value:  # 如果驗證碼和庫中驗證碼一致
                  now = time.mktime(  # 獲取現在時間並轉爲秒,需要導入time包
                     datetime.now().timetuple()
                  )
                  db_now = time.mktime(db_email.times.timetuple())  # 獲取郵箱驗證表中時間轉爲秒
                  if now - db_now > 300:  # 如果驗證碼時間差大於一天
                     result['data'] = '驗證碼過期'
                     db_email.delete()  # 刪除驗證表中該註冊數據
                  else:  # 如果驗證碼未過期
                     form.save()
                     result['data']='註冊成功'
               else:  # 如果驗證碼和庫中驗證碼不一致
                  result['data'] = '驗證碼錯誤'
         else:  # 如果表中不存在該郵箱
            result['data'] = '郵箱不匹配'
   context = {
      'form': form
   }
   return render(request,'register.html',locals())

def getRandomData():
   result = str(random.randint(1000,9999))
   return result

def sendMessage(request):
   result = {"staue": "error", "data": ""}
   if request.method == 'GET' and request.GET: #確定是否有get請求
        recver = request.GET.get('email')  #獲取前端輸入的註冊郵箱，也就是發件人
        subject = "金門大學greenlife系統註冊"   #郵件主題
        text_content = ""   #發送的文本內容
        value = getRandomData()  #通過驗證碼函數獲取驗證碼是
        #帶有html樣式的文本內容
        html_content = """    
                    <div>
                        <p>
                           您的用戶驗證碼是:%s。
                           5分鐘內有效
                        </p>
                    </div>
                    """ %value
        # 確認郵件信息：主題、內容、發件人、收件人（可多人）
        message = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [recver])  
        message.attach_alternative(html_content, "text/html")  #添加帶html樣式的內容
        message.send()  #發送
        result['statue'] = 'success'
        result['data'] = '發送成功'
        miku= EmailValid.objects.filter(email_address=recver).all()
        miku.delete()

        e = EmailValid() #實例化表
        e.email_address = recver  #存入註冊郵箱
        e.value = value     #存入驗證碼
        e.times = datetime.datetime.now()  #存入時間
        e.save() #保存入數據庫
   return JsonResponse(result)

def sign_in(request):
   form = LoginForm()
   if request.method == "POST":
      username = request.POST.get("username")
      password = request.POST.get("password")
      user = authenticate(request, username=username, password=password)
      if user is not None:
         login(request, user)
         return redirect('/index/')  
   context = {
      'form': form
   }
   return render(request, 'login.html', context)

def logout(request):
   auth.logout(request)
   return HttpResponseRedirect('/index/')

def index(req):
    miku=read()
    context = {
        'miku':miku
    }
    return render(req,'index.html',context)

def drew():
   sum=int(Sheets.get_values("E2")[0][0])
   i=int(4)
   while True:
      if sum==0 or Sheets.get_values('C'+str(i))==[]:
         break
      if int(Sheets.get_values('C'+str(i))[0][0].replace(',',''))<=sum:
         Sheets.format('C'+str(i), {
            "backgroundColor": {
               "red": 0.0,
               "green": 1.0,
               "blue": 0.0
            },
            "horizontalAlignment": "LEFT",
            "textFormat": {
               "foregroundColor": {
                  "red": 0.0,
                  "green": 0.0,
                  "blue": 0.0
               },
               "fontSize": 10,
               "bold": False
            }
         })
         sum-=int(Sheets.get_values('C'+str(i))[0][0].replace(',',''))
      else :
         Sheets.format('C'+str(i), {
            "backgroundColor": {
               "red": 1.0,
               "green": 1.0,
               "blue": 1.0
            },
            "horizontalAlignment": "LEFT",
            "textFormat": {
               "foregroundColor": {
                  "red": 0.0,
                  "green": 0.0,
                  "blue": 0.0
               },
               "fontSize": 10,
               "bold": False
            }
         })
      i+=1

def dashboard(req):
   pdl=[[1,2,3],[4,5,6]]
   context={'pdl':pdl}
   return render(req,'dashboard.html',context)
