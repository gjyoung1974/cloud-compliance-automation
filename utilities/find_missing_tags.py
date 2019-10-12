#!/usr/bin/env python
#
# Find user human uer IDs that are missing the 'acme.email' tag
# 2019 - Acme Infrastructure Security
#

import boto3
from botocore.exceptions import ClientError
import csv
from time import sleep

users_and_email_ids = []


def get_user(user_name):
    iam = boto3.client('iam')

    try:
        response = iam.get_user(UserName=user_name)
        user = response['User']
        user_email = None
        if 'Tags' in user:
            for tag in user['Tags']:
                if tag['Key'] == 'acme.email':
                    user_email = tag['Value']
                    return user_email
            if user_email is None:
                print(str(user_name) + ': missing Email tag')

    except Exception as e:
        print('ERROR get_user {}'.format(user_name))
        print(e)
        raise e


def get_missing_tags():
    iam_client = boto3.client('iam')

    # Request the credential report, download and parse the CSV.
    def get_credential_report(s_iam_client):
        resp1 = s_iam_client.generate_credential_report()
        if resp1['State'] == 'COMPLETE':
            try:
                response = s_iam_client.get_credential_report()
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
            return get_credential_report(s_iam_client)

    obj_credential_report = get_credential_report(iam_client)

    for row in obj_credential_report:
        if row['password_enabled'] != "true":
            continue  # Skip IAM Users without passwords
        user_email = get_user(row['user'])
        users_and_email_ids.append(row['user'] + ', Email: ' + str(user_email))

    # You could print(users_and_email_ids) to view the mapping of IAM user IDs and email tags
    return users_and_email_ids


get_missing_tags()
