import boto3



access_key_id = os.environ['AWS_ACCESS_KEY_ID']
secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
session_token = os.environ['AWS_SESSION_TOKEN']
assumeRoleName = 'OrganizationAccountAccessRole'

us_regions = ["us-east-1","us-east-2","us-west-1","us-west-2"]
print('[*] Initiating boto3 session...')
session = boto3.session.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, aws_session_token=session_token, region_name='us-east-1')




aws_profile = '...'
zone_id = 'Z2A...'
max_records = 1000


route53 = session.client('route53')



dns_records = []

dns_in_iteration = route53.list_resource_record_sets(HostedZoneId=zone_id)
dns_records.extend(dns_in_iteration['ResourceRecordSets'])

while len(dns_records) < max_records and 'NextRecordName' in dns_in_iteration.keys():
    next_record_name = dns_in_iteration['NextRecordName']
    print('listing next set: ' + next_record_name)
    dns_in_iteration = route53.list_resource_record_sets(HostedZoneId=zone_id, StartRecordName=next_record_name)
    dns_records.extend(dns_in_iteration['ResourceRecordSets'])

print('records found: ' + str(len(dns_records)))    
for record in dns_records:
    if record['Type'] == 'CNAME':
        print(record['Name'])