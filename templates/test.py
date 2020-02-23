#-*- coding: utf-8 -*-
import smtplib

from email.mime.text import MIMEText

from email.mime.base import MIMEBase

from email.mime.image import MIMEImage

from email import encoders

import io



# 메일 서버를 설정합니다.

server = smtplib.SMTP('smtp.gmail.com', '465')



# 로그인이 필요하면 로그인 설정

server.login('gusrl1005','skdus0330@')



# 보내는 사람, 받는 사람 설정

sender = 'gusrl1005@naver.com'

to = 'gusrl100%@daum.net'

cc = 'gusrl1005@daum.net'



# 메세지 구성

msg = MIMEBase('multipart','mixed')

msg['Subject'] = '[Test] Send Email'

msg['From'] = sender

msg['To'] = to

msg['Cc'] = cc





with io.open('file_name.html','r') as f:

    emailtext = f.read()



attachment = 'attachment_file_name.png'



fp = open(attachment, 'rb')                                                    

img = MIMEImage(fp.read())

fp.close()

img.add_header('Content-ID', '<{}>'.format(attachment))

msg.attach(img)



# 메일 본문 작성

# html 로 되어있던 파일을 불러 오고 거기에 파일을 붙여서 보냅니다.

msgText = MIMEText('%s, <img src="cid:%s" >' % (emailtext, attachment), 'html')  





# 메세지를 메일에 붙여 줍니다.

msg.attach(msgText)



# 메일 서버를 이용하여 메일을 발송합니다.

server.sendmail(sender, msg["To"].split(",") + msg["Cc"].split(","), msg.as_string())

server.quit()



print('OK')



