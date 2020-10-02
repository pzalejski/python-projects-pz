import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email = ""
pas = ""

sms_gateway = 'number@txt.att.net'

smtp = "smtp.gmail.com"
port = 587

# This will start out email server
server = smtplib.SMTP(smtp, port)
# starting the server
server.starttls()
# need to login
server.login(email, pas)

# use the MIME module to structure the message
msg = MIMEMultipart()
msg['From'] = email
msg['To'] = sms_gateway
# Make sure you add a new line in the subject
msg['Subject'] = "Loren imspum\n"
# Make sure you also add new lines to your body
body = "Loren impsum\n"
# and then attach that body furthermore you can also send html content.
msg.attach(MIMEText(body, 'plain'))

sms = msg.as_string()

server.sendmail(email,sms_gateway,sms)

# lastly quit the server
server.quit()
