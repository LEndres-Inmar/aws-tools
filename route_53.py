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

route53_client = session.client('route53')



'''
Alright... so without specifying an account, it runs off the access keys and secrets you give it. Neat.
'''


def get_all_hosted_zone_ids():
    # Create a Route 53 client
    #client = boto3.client('route53')

    # Initialize a list to store hosted zone IDs
    hosted_zone_ids = []

    # Start with the first request
    next_marker = None
    while True:
        # Call list_hosted_zones with the next_marker if it exists
        if next_marker:
            response = route53_client.list_hosted_zones(Marker=next_marker)
        else:
            response = route53_client.list_hosted_zones()

        # Extract the hosted zone IDs and add them to the list
        hosted_zone_ids.extend([zone['Id'] for zone in response['HostedZones']])

        # Check if there is a next page (next_marker), if so, continue
        next_marker = response.get('NextMarker')
        if not next_marker:
            break  # No more pages, break out of the loop

    print(f'hosted zones: {hosted_zone_ids}')
    return hosted_zone_ids

# Example usage
hosted_zone_ids = get_all_hosted_zone_ids()

# Print all hosted zone IDs
for zone_id in hosted_zone_ids:
    print(zone_id)



def get_routes(accounts):
    for account in accounts:
        # List the record sets in the specified hosted zone
        response = route53_client.list_resource_record_sets(HostedZoneId="Z2J5S9MTWWRUXF")

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


if __name__ == '__main__':
    # specific aws accounts
    #grocery_ecommerce_accounts = ['inmar-eretail-deploy','inmar-eretail-log'] #,'inmargrocerydev','inmargroceryprod']

    #get_all_hosted_zone_ids()
    #get_routes(grocery_ecommerce_accounts)
    pass