import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import email, password, pnum
em = email
pas = password
number = pnum

sms_gateway = pnum + '@txt.att.net'
server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)

def email_login(em, pas):

    try:
        server_ssl.ehlo()
        server_ssl.login(em,pas)
    except:
        print('sometihng went wrong')

def bitcoin_sms(em, sms_gateway, sms_subject, sms_body):
    email_login(em, pas)

    # use the MIME module to structure the message
    msg = MIMEMultipart()
    msg['From'] = em
    msg['To'] = sms_gateway
    # Make sure you add a new line in the subject
    msg['Subject'] = sms_subject
    # Make sure you also add new lines to your body
    body = sms_body
    # and then attach that body furthermore you can also send html content.
    msg.attach(MIMEText(body, 'plain'))

    sms = msg.as_string()

    server_ssl.sendmail(em,sms_gateway,sms)
    # lastly quit the server
    server_ssl.quit()



