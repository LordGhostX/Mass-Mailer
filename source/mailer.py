import eel
import smtplib
from time import sleep
from random import randint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import string
import random

count = 0

eel.init("web")

@eel.expose
def startsend(host, port, login, password, subject, message, emails):
    emails = emails.split("\n")
    try:
        s = smtplib.SMTP(host=host, port=port)
        s.starttls()
        s.login(login, password)
    except Exception as e:
        print(e); return "Error setting up SMTP"
    print("Successfully logged in to SMTP")

    error = False
    eel.startAlert()
    for email in emails:
        curr_msg = message.replace("{MAIL}", email)
        msg = MIMEMultipart()
        msg['From'] = login
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(curr_msg, 'html', "utf-8"))
        s.send_message(msg)
        del msg
        global count
        count = count + 1
        print("[" + str(count) + "] Successfully sent mail to", email)
        sleep(randint(5, 10))
    eel.finishAlert()    
    s.quit()
    if error:
        return "Error occured while sending mails"
    else:
        return "Successful"

#eel.start("index.html", mode='chrome-app', port=8080, cmdline_args=['--start-fullscreen', '--browser-startup-dialog'])
eel.start("index.html")
