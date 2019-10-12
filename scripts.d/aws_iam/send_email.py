#!/usr/bin/env python
#
# Send an email to some user that needs to perform some compliance action
# 2019 - Acme Infrastructure Security
#


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP


def send_email(s_smtp, smtp_from, smtp_to, s_subject, s_message):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = s_subject
    msg["From"] = smtp_from
    # while testing force sending everything to me
    msg["To"] = 'gjyoung1974@gmail.com'
    # msg["To"] = smtp_to
    msg.attach(MIMEText('\n' + s_message, 'plain'))
    # while testing send everything to me
    s_smtp.sendmail(smtp_from, 'gjyoung1974@gmail.com', msg.as_string())
    # s_smtp.sendmail(smtp_from, smtp_to, msg.as_string())
