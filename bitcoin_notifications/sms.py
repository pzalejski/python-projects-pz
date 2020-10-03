import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import email, password, pnum
em = email
pas = password
number = pnum

sms_gateway = pnum+'@txt.att.net'

try:
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.ehlo()
    server_ssl.login(em,pas)
except:
    print('sometihng went wrong')

# use the MIME module to structure the message
msg = MIMEMultipart()
msg['From'] = em
msg['To'] = sms_gateway
# Make sure you add a new line in the subject
msg['Subject'] = "Loren imspum\n"
# Make sure you also add new lines to your body
body = "Loren impsum\n"
# and then attach that body furthermore you can also send html content.
msg.attach(MIMEText(body, 'plain'))

sms = msg.as_string()

server_ssl.sendmail(em,sms_gateway,sms)
# lastly quit the server
server_ssl.quit()
