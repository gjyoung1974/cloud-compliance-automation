#!/usr/bin/env python
#
# A script to update AWS:IAM service account tags
# 2019 - Acme Infrastructure Security
#

import boto3
import csv

iam = boto3.client('iam')

with open('svc_accounts.txt') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        print(row['aws.user'], row['owner'])
        response = iam.tag_user(
            UserName=row['aws.user'],
            Tags=[
                {
                    'Key': 'acme.owner',
                    'Value': row['owner']
                },
                {
                    'Key': 'acme.description',
                    'Value': row['description']
                },
                {
                    'Key': 'acme.serviceaccount',
                    'Value': 'true'
                },
            ]
        )
