#!/usr/bin/env python

import boto3
from botocore.exceptions import ClientError
import os
import json
import pprint
import os

access_key_id = os.environ['AWS_ACCESS_KEY_ID']
secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
session_token = os.environ['AWS_SESSION_TOKEN']
assumeRoleName = 'OrganizationAccountAccessRole'

us_regions = ["us-east-1","us-east-2","us-west-1","us-west-2"]
session = boto3.session.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, aws_session_token=session_token, region_name='us-east-1')

route53_client = session.client('route53')

accounts_paginator = org_client.get_paginator('list_accounts')
accounts_page_iterator = accounts_paginator.paginate()





def get_routes(accounts):
    for account in accounts:
        # List the record sets in the specified hosted zone
        response = route53_client.list_resource_record_sets(HostedZoneId="deploy.inmar.com")

        a_records = []
        cname_records = []

        # Loop through the record sets and filter A and CNAME records
        for record in response['ResourceRecordSets']:
            if record['Type'] == 'A':
                a_records.append(record)
            elif record['Type'] == 'CNAME':
                cname_records.append(record)

        print(a_records)
        return a_records, cname_records


if __name__ == '__main__':
    # specific aws accounts
    grocery_ecommerce_accounts = ['inmar-eretail-deploy'] #,'inmar-eretail-log','inmargrocerydev','inmargroceryprod']

    get_routes(grocery_ecommerce_accounts)