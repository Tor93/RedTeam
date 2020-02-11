#-*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask_mail import Mail, Message
import numpy as np

app =Flask(__name__)

# Mail config 설정 
app.config.from_pyfile('./conf/config.py') 		# 메일 서버 정보config 지정
mail = Mail(app)


@app.route("/")
def index():
    return render_template("index.html")



# email.html 과 연동
@app.route("/email",methods = ['post','get'] )
def email1():
    
    if request.method=='POST':				# 전송자, 메일 내용, 받는사람 지정
        senders = request.form['email_sender']
        title = request.form['email_title']
        receiver = request.form['email_receiver']
        content = request.form['email_content']
        receiver = receiver.split(',') 			# ","로 구분자 줌으로써 대량 메일 전송 가능
    else:    
        return render_template('email.html')
    return email2(senders, receiver, title, content)


# Email Sent Data 초기화
Sent = 0


# Email 전송 로직
# 고도화 예정 -> 메일 발송 성공, 오류 예외처리
# (추가사항) 이전 로직에서는 받는 사람이 receiver 전부로 나와 있기 때문에 받는 사람이 한명씩 보이게 하기 위해 구문 추가
def email2(senders, receiver,title,content):
    for person in receiver:		#
        receiver2 = []		 	# 받는 사람을 한명씩으로 만들기 위해 리스트에 받는 사람 한명씩 찍히도록 for 문 추가
        receiver2.append(person)	#
        msg = Message(title, sender = senders, recipients = receiver2)
        msg.body = content
        mail.send(msg)
    Sent = len(receiver)	# 메일 수신자 count =  Mail Sent Data
    return Dashboard(Sent)	# 고도화 예정 -> 성공적으로 발송된 Mail 갯수로 정확한 Data 구현


# Dashboard 데이터 전송 로직
@app.route('/dashboard')
def Dashboard(Sent):
    return render_template('chart.html', sent=Sent)	


if __name__ == '__main__':
   app.run(debug=True, host = '0.0.0.0')
