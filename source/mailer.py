import eel
import smtplib
from time import sleep
from random import randint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

eel.init("web")

@eel.expose
def startsend(host, port, login, password, subject, message, emails):
    emails = emails.split("\n")
    try:
        s = smtplib.SMTP_SSL(host=host, port=port)
        s.starttls()
        s.login(login, password)
    except Exception as e:
        print(e); return "Error setting up SMTP"
    print("Successfully logged in to SMTP")

    error = False
    for email in emails:
        curr_msg = message.replace("{MAIL}", email)
        msg = MIMEMultipart()
        msg['From'] = login
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(curr_msg, 'html', "utf-8"))
        s.send_message(msg)
        del msg
        print("Successfully sent mail to", email)
        sleep(randint(5, 30))
    s.quit()
    if error:
        return "Error occured while sending mails"
    else:
        return "Successful"

eel.start("index.html")
