#!/usr/bin/python2
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText

def send_mail(to_addr, subject, text):
    from_addr = "test@gmail.de"
    google_username = "iotdashbutton77@gmail.com"
    google_app_password = "hhzhackathon17"
    message = MIMEText(text, 'plain', 'UTF-8')
    message['Subject'] = subject
    message['From'] = from_addr
    message['To'] = to_addr
    print("versendet")

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(google_username, google_app_password)
    server.sendmail(from_addr, to_addr, message.as_string())
    server.quit()