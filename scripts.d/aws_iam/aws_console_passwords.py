#!/usr/bin/env python
#
# Get expiring AWS IAM console user accounts with expiring passwords
# 2019 - Acme Infrastructure Security
#


import boto3
import datetime
from botocore.exceptions import ClientError
import csv
from time import sleep
from datetime import datetime
from datetime import timedelta
import dateutil.parser

from get_iam_user_tags import get_email
from send_email import send_email

import os

def aws_console_password(s_smtp):
    iam_client = boto3.client('iam')
    pass_max_days = 90

    # Request the credential report, download and parse the CSV.
    def get_credential_report(_iam_client):
        resp1 = _iam_client.generate_credential_report()
        if resp1['State'] == 'COMPLETE':
            try:
                response = _iam_client.get_credential_report()
                credential_report = response['Content']
                reader = csv.DictReader(credential_report.splitlines())
                credential_report = []
                for _row in reader:
                    credential_report.append(_row)
                return credential_report
            except ClientError as e:
                print("Unknown error getting Report: " + e.message)
        else:
            sleep(2)
            return get_credential_report(_iam_client)

    obj_credential_report = get_credential_report(iam_client)

    for row in obj_credential_report:
        # Skip IAM Users without a console password enabled.
        if row['password_enabled'] != "true":
            continue
        last_changed = dateutil.parser.parse(row['password_last_changed'])

        now = datetime.utcnow().replace(tzinfo=last_changed.tzinfo)
        diff = now - last_changed
        delta = timedelta(days=pass_max_days)

        if diff > delta:
            acme_email_id = get_email(row['user'])

            send_email(s_smtp, os.environ.get('EMAIL_FROM'), acme_email_id, 'AWS console password expiration',
                       'Hello,\n\nThe password for: AWS account: ' +
                       row['user'] + '  has reached ' + ': {0} Days'.format(diff.days) +
                       " Old.\n\nPlease visit: https://console.aws.amazon.com/iam/home?#/users/" +
                       row['user']
                       + "?section=security_credentials\n\n" +
                       "To reset your AWS console user password: click the \"Manage\" link on the "
                       "\"Console password\" row on the \"Security Credentials\" tab\n\n" +
                       "AWS User Id: " + row['user'] + "\n" +
                       "Email Id: " + str(acme_email_id))
