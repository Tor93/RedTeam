#-*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import io
import smtplib
import numpy as np
import pymysql
import re
import time

start = time.time()


app =Flask(__name__)


#DB 연동
conn = pymysql.connect(host='localhost', user='root', password='1',
db='emailtest', charset='utf8')
curs = conn.cursor()


# Mail config 설정 
app.config.from_pyfile('./conf/config.py') 		# 메일 서버 정보config 지정
mail = Mail(app)


@app.route("/")
def index():
    return render_template("index.html")



# email.html 과 연동
@app.route("/email",methods = ['POST','GET'] )
def email1():
    if request.method=='POST':
        senders = request.form['email_sender']
        title = request.form['email_title']
        receiver = request.form['email_receiver']
        content = request.form['email_content']
        receiver = re.split('[ ,]+',receiver) 			# ","로 구분자 줌으로써 대량 메일 전송 가능
    else:    
        return render_template('email.html')
    return email2(senders, receiver, title, content)




# Email 전송 로직
# 고도화 예정 -> 메일 발송 성공, 오류 예외처리 -> 성공적으로 발송된 Mail 갯수를 Count 하는 Data 필요
def email2(senders, receiver,title,content):
    try:
        for person in receiver:	
            receiver2 = []
            receiver2.append(person)	
            msg = Message(title, sender = senders, recipients = receiver2)
            msg.html = content + '<a href="http://192.168.80.134:5000/dashboard?link=%s">https://google.com</a>' % code()
            mail.send(msg)
            sql = "insert into user(email_address, email_sent) values(%s,%s)"
            curs.execute(sql,(receiver2, 'Sent'))
            conn.commit()
        return Dashboard()
    except Exception as ex:
        print("에러 발생",ex)

## read1 파라미터의 데이터 값을 만들기 위해 필요한 로직
def code():
    conn = pymysql.connect(host='localhost', user='root', password='1',
    db='emailtest', charset='utf8')
    curs = conn.cursor()
    curs.execute('SELECT user_id from user ORDER BY user_id DESC limit 1')
    user_id = curs.fetchone()
    user_id1 = user_id[0]
    return user_id1



#email Sent counting  -> 메일이 성공적으로 보내졌는지 확인하는 함수
def Sent_add():
    conn = pymysql.connect(host='localhost', user='root', password='1',
    db='emailtest', charset='utf8')
    curs = conn.cursor()
    curs.execute('SELECT count(email_sent) from user')
    Sent = curs.fetchone()
    conn.close()
    return Sent[0]



#email read couting  -> 메일 읽은 사람을 Count 하기 위해 필요한 함수
def reading():
    conn = pymysql.connect(host='localhost', user='root', password='1',
    db='emailtest', charset='utf8')
    curs = conn.cursor()
    Read = request.args.get('read1','')
    sql = "UPDATE user SET email_read='OK' WHERE user_id=%s"
    curs.execute(sql, Read)
    conn.commit()
    curs.execute('SELECT count(email_read) from user where email_read="OK"')
    read12 = curs.fetchone()
    conn.close()
    return read12[0]


#email link_click couting  -> 링크 클릭한 사람을 Count 하기 위해 필요한 함수
def clicked():
    conn = pymysql.connect(host='localhost', user='root', password='1',
    db='emailtest', charset='utf8')
    curs = conn.cursor()
    CClick = request.args.get('link','')
    sql = "UPDATE user SET email_link_click='OK' WHERE user_id=%s"
    curs.execute(sql, CClick)
    conn.commit()
    curs.execute('SELECT count(email_link_click) from user where email_link_click="OK"')
    click = curs.fetchone()
    conn.close()
    return click[0]




# Dashboard 데이터 전송 로직 
@app.route('/dashboard', methods=['GET'])
def Dashboard():
    print(code())
    return render_template('chart.html', sent=Sent_add(), read = reading(), link_click = clicked())



if __name__ == '__main__':
   app.run(debug=True, host = '0.0.0.0')


print("time :", time.time() - start)
