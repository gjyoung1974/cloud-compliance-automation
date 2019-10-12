#!/usr/bin/env python
#
# Get an AWS:IAM 'user' object's tags
# 2019 - Acme Infrastructure Security
#


import boto3

to_email_id = []


def get_email(user_name):
    iam = boto3.client('iam')

    try:
        response = iam.get_user(UserName=user_name)
        user = response['User']
        email = None
        if 'Tags' in user:
            for tag in user['Tags']:
                if tag['Key'] == 'acme.email':
                    email = tag['Value']
                    to_email_id.append(email)
                    return email

    except Exception as e:
        print('ERROR get_user {}'.format(user_name))
        print(e)
        raise e
    return to_email_id
