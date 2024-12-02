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





def get_accounts():
    print('[*] Getting accounts...')
    accounts_list = []

    for page in accounts_page_iterator:  
        for acct in page['Accounts']:
            accounts_list.append(acct)
            print(type(acct))
            pprint.pp('\t'+acct['Name'])
    print('[*] Accounts retrieved!')
    
    return accounts_list