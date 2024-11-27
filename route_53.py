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

session = boto3.session.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, aws_session_token=session_token, region_name='us-east-1')


#route53_client = session.client('route53')
sts_client = session.client('sts')
org_client = session.client('organizations')



 








def get_accounts():
    accounts_paginator = org_client.get_paginator('list_accounts')
    accounts_page_iterator = accounts_paginator.paginate()
    
    #print('[*] Getting accounts...')
    accounts_list = []

    for page in accounts_page_iterator:  
        for account in page['Accounts']:
            accounts_list.append(account)

    return accounts_list





def assume_role(account_id, role_name):
    # Assume the role in the target account
    sts_client = boto3.client('sts')

    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"

    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="AssumeRoleSession"
    )

    # Extract temporary credentials from the response
    credentials = response['Credentials']
    
    return credentials



def get_hosted_zone_ids():
    client = boto3.client('route53')

    hosted_zone_ids = []
    next_marker = None
    
    while True:
        # List hosted zones with pagination if necessary
        if next_marker:
            response = client.list_hosted_zones(Marker=next_marker)
        else:
            response = client.list_hosted_zones()

        # Extract the hosted zone IDs and append to the list
        hosted_zone_ids.extend([zone['Id'] for zone in response['HostedZones']])
        
        # Check if there is a next page of results
        next_marker = response.get('NextMarker')
        if not next_marker:
            break  # No more pages, exit the loop

    return hosted_zone_ids







def get_routes_from_zone(account_id, zone_id):
    assume_role_arn = "arn:aws:iam::" + account_id + ":role/" + assumeRoleName
    assumedRoleObject = sts_client.assume_role(RoleArn=assume_role_arn, RoleSessionName="OrgAssumeRole")
    
    credentials = assumedRoleObject['Credentials']

    route53_client = boto3.client('route53',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'])
    

    
    pprint.pp(zone_id)

    # clean up the string
    zone_id = zone_id[12:]
    print(zone_id)

    for zone in zones:
        # List the record sets in the specified hosted zone
        response = route53_client.list_resource_record_sets(HostedZoneId=zone_id)

        a_records = []
        cname_records = []

        # Loop through the record sets and filter A and CNAME records
        for record in response['ResourceRecordSets']:
            if record['Type'] == 'A':
                a_records.append(record)
            elif record['Type'] == 'CNAME':
                cname_records.append(record)

        pprint.pp(a_records)
        return a_records, cname_records



def get_zones_from_account_id(account_id):
    #for account in get_accounts():


    assume_role_arn = "arn:aws:iam::" + account_id + ":role/" + assumeRoleName
    assumedRoleObject = sts_client.assume_role(RoleArn=assume_role_arn, RoleSessionName="OrgAssumeRole")
    
    credentials = assumedRoleObject['Credentials']

    client=boto3.client('route53',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'])
    
    response = client.list_hosted_zones()

    for zone in response['HostedZones']:
        print(f"\t{zone['Name']} -> {zone['Id']}")
    print("\n")

    return response['HostedZones']


def get_account_details(account_name):
    '''To retrieve only a specific AWS account (based on the account name or account ID)
    using AWS Organizations, you can filter the results after calling the list_accounts
    API, as AWS Organizations does not support filtering by account name directly in the
    API request itself.
    
    :returns:'''

    accounts_paginator = org_client.get_paginator('list_accounts')
    accounts_page_iterator = accounts_paginator.paginate()

    for page in accounts_page_iterator:  
        for account in page['Accounts']:
            if account['Name'] == account_name:
                print(f"Account: {account['Name']}, ID: {account['Id']}")
                return account




if __name__ == '__main__':
    # whitespace
    print('\n')
    # We really don't need to get the accounts, we already have them by name
    # 4 accounts
    accounts = ['inmar-eretail-deploy'] #, 'inmar-eretail-log', 'inmargrocerydev', 'inmargroceryprod']


    for account in accounts:
        account_details = get_account_details(account)
        zones = get_zones_from_account_id(account_details['Id'])

        # loop through each zone
        for zone in zones:
            get_routes_from_zone(account_details['Id'], zone['Id'])
        
        #for zone_group in account_details
        #get_zones_from_account(account_details)