#!/usr/bin/env python
#
# Get expiring AWS IAM console user accounts with expiring API/CLI "Access Keys"
# 2019 - Acme Infrastructure Security
#

import boto3
import datetime
import time
import os

from get_iam_user_tags import get_email
from send_email import send_email


def aws_access_keys(s_smtp):
    client = boto3.client('iam', region_name='us-west-2')

    response = client.list_users()  # List all the users

    for user in response["Users"]:
        username = user['UserName']

        # for each user get the each access key
        res = client.list_access_keys(UserName=username)
        for key in res['AccessKeyMetadata']:

            # format the dates
            access_key_date = key['CreateDate']
            access_key_date = access_key_date.strftime("%Y-%m-%d %H:%M:%S")
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            access_key_date = time.mktime(datetime.datetime.strptime(
                access_key_date, "%Y-%m-%d %H:%M:%S").timetuple())
            current_date = time.mktime(datetime.datetime.strptime(
                now, "%Y-%m-%d %H:%M:%S").timetuple())
            # We get the data in seconds and convert it to days
            active_days = (current_date - access_key_date) / 60 / 60 / 24
            if active_days >= 90:
                if key['Status'] == 'Active':
                    acme_email_id = get_email(key['UserName'])
                    send_email(s_smtp, os.environ.get('EMAIL_FROM'), acme_email_id, 'AWS Access key expiration',
                               'Hello,\n\nThe AWS Access Key" '
                               + key['AccessKeyId'] + ' for: AWS account: ' +
                               key['UserName'] + '  has reached ' +
                               ': {0} Days'.format(str((int(round(active_days))))) +
                               " Old.\n\nPlease visit: https://console.aws.amazon.com/iam/home?#/users/" +
                               key['UserName'] + "?section=security_credentials\n\n" +
                               "To create a new access key: click the \"Create Access Key\" button on the "
                               "\"Access Keys\" row on the \"Security Credentials\" tab\n\n" +
                               "AWS User Id: " + key['UserName'] + "\n" +
                               "Email Id: " + str(acme_email_id))
