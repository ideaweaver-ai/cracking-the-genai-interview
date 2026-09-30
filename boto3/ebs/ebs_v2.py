import sys

import boto3
from botocore.exceptions import ClientError


def get_volume_ids(region):
    """Return every EBS volume ID in one region."""
    ec2 = boto3.client("ec2", region_name=region)

    # describe_volumes returns one page at a time.
    # The paginator asks for the next page until none are left.
    paginator = ec2.get_paginator("describe_volumes")

    volume_ids = []
    for page in paginator.paginate():
        for volume in page["Volumes"]:
            volume_ids.append(volume["VolumeId"])
    return volume_ids


# Use the region you pass in, for example: python3 ebs.py us-east-1
# If you do not pass one, boto3 uses AWS_DEFAULT_REGION from your environment.
if len(sys.argv) > 1:
    region = sys.argv[1]
else:
    region = boto3.session.Session().region_name

if not region:
    print("Pass a region, or set AWS_DEFAULT_REGION")
    sys.exit(1)

try:
    for volume_id in get_volume_ids(region):
        print(volume_id)
except ClientError as error:
    # EC2 does not have its own exception classes.
    # The error name is a string in the response, such as UnauthorizedOperation.
    error_info = error.response["Error"]
    print("AWS error:", error_info["Code"])
    print(error_info["Message"])
    sys.exit(1)
