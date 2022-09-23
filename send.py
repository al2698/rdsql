from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

content = MIMEMultipart()  #建立MIMEMultipart物件
content["subject"] = "Learn Code With Mike"  #郵件標題
content["from"] = "de45amiku@gmail.com"  #寄件者
content["to"] = "as355132@asjh.ntpc.edu.tw" #收件者
content.attach(MIMEText("Demo python send email"))  #郵件內容

with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
    try:
        smtp.ehlo()  # 驗證SMTP伺服器
        smtp.starttls()  # 建立加密傳輸
        smtp.login("de45amiku@gmail.com", "hsjhzdqoqbfyzpro")  # 登入寄件者gmail
        smtp.send_message(content)  # 寄送郵件
        print("Complete!")
    except Exception as e:
        print("Error message: ", e)
