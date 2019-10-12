#!/usr/bin/env python
#
# A script to update AWS:IAM user account tags
# 2019 - Acme Infrastructure Security
#

import boto3
import csv

iam = boto3.client('iam')

with open('iam_users.txt') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        print(row['aws.user'], row['acme.email'])
        response = iam.tag_user(
            UserName=row['aws.user'],
            Tags=[
                {
                    'Key': 'acme.first.last',
                    'Value': row['acme.first.last']
                },
                {
                    'Key': 'acme.email',
                    'Value': row['acme.email']
                },
                {
                    'Key': 'acme.serviceaccount',
                    'Value': 'false'
                },
            ]
        )
