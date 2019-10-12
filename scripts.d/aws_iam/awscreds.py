import datetime
import logging
import os
import smtplib

from aws_access_key import aws_access_keys
from aws_console_passwords import aws_console_password

# entrypoint for AWS Crededntials reporting:
def aws_creds():
    s = smtplib.SMTP(os.environ.get('SMTP_HOST'), 587)
    # s.set_debuglevel(1)   # to enable smtp debug
    s.ehlo()
    s.starttls()
    s.login(os.environ.get('SMTP_USER'), os.environ.get('SMTP_PASS'))
    print("AWS Credential Aging job ran at: " +
          str(datetime.datetime.now().time()))
    aws_console_password(s)
    aws_access_keys(s)
    s.quit()


os.environ.get('HOME')
