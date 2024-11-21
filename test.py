'''test roll'''

sts = boto3.client('sts', 'us-east-1',
                        aws_access_key_id=access_key_id,
                  aws_secret_access_key=secret_access_key)

try:
    id = sts.get_caller_identity()
    print("Credentials are valid.")
    print("Account ID: " + id["Account"] + "\n" + "Arn: " + id["Arn"])
except ClientError:
    print("Credentials are NOT valid." + "\n")