#!/usr/bin/env python

import boto3
from botocore.exceptions import ClientError
import os
import json
import pprint

access_key_id = os.environ['AWS_ACCESS_KEY_ID']
secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
session_token = os.environ['AWS_SESSION_TOKEN']
assumeRoleName = 'OrganizationAccountAccessRole'

us_regions = ["us-east-1","us-east-2","us-west-1","us-west-2"]
print('[*] Initiating boto3 session...')
session = boto3.session.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, aws_session_token=session_token, region_name='us-east-1')
print('[*] Initiating individual clients...')
sts_client = session.client('sts')
org_client = session.client('organizations')
ec2_client = session.client('ec2') 

accounts_paginator = org_client.get_paginator('list_accounts')
accounts_page_iterator = accounts_paginator.paginate()

print(accounts_page_iterator)



def get_accounts():
    print('[*] get_accounts()')
    accounts_list = []

    for page in accounts_page_iterator:  
        for acct in page['Accounts']:
            accounts_list.append(acct)
            pprint.pp(acct['Name'])
    quit()
    
    return accounts_list


'''Write function to get Route 53!

1. auth to org role
2. sts assume role into each of the 4 account ids using the org roll
3. retrieve the route 53 hosted zones + hosted zones recored for each recursuvly
4. filter that record data for A+CNAME records
5. test each endpoint w/ TLS enumeration tool
6. sslyze - testssl
???
8. develop automation script?

---

Feed it the 4 accounts

'''

def list_ec2_instances():
    print('list_ec2_instances()')
    for account in get_accounts():
        #print(account)

        try:
            assume_role_arn = "arn:aws:iam::" + account['Id'] + ":role/" + assumeRoleName
            assumedRoleObject = sts_client.assume_role(RoleArn=assume_role_arn, RoleSessionName="OrgAssumeRole")
            credentials = assumedRoleObject['Credentials']
            for region in us_regions:
                ec2_client=boto3.client('ec2',
                    aws_access_key_id=credentials['AccessKeyId'],
                    aws_secret_access_key=credentials['SecretAccessKey'],
                    aws_session_token=credentials['SessionToken'],
                    region_name=region
                )
                reservations = ec2_client.describe_instances()['Reservations']
                instance_list = []
                for reservation in reservations:
                    print(type(reservation))

                    pprint.pp(f'reservation: {reservation}')
                    print('\n\n\n')
                    for instance in reservation['Instances']:
                        pprint.pp(f'instance: {instance}')
                        instance_list.append(instance)
                        # ec2_list = ec2_client.describe_instances().append(ec2_list)
            # print(instance_list)
            # return instance_list
        except ClientError as error:
            continue
    return instance_list


instances = list_ec2_instances()
print(instances)