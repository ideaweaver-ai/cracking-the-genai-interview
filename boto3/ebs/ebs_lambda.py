import json
import os

import boto3
from botocore.exceptions import ClientError


def get_volume_ids(region):
    """Return every EBS volume ID in one region."""
    ec2 = boto3.client("ec2", region_name=region)
    paginator = ec2.get_paginator("describe_volumes")

    volume_ids = []
    for page in paginator.paginate():
        for volume in page["Volumes"]:
            volume_ids.append(volume["VolumeId"])
    return volume_ids


def lambda_handler(event, context):
    """Entry point Lambda calls.

    In the Lambda console, set the handler to ebs_lambda.lambda_handler.
    The function's IAM role needs permission to call ec2:DescribeVolumes.
    Lambda sets AWS_REGION to the region where the function runs.
    """
    event = event or {}
    region = event.get("region") or os.environ["AWS_REGION"]

    try:
        volume_ids = get_volume_ids(region)
    except ClientError as error:
        # EC2 does not have its own exception classes.
        # The error name is a string in the response, such as UnauthorizedOperation.
        error_info = error.response["Error"]
        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "error": error_info["Code"],
                    "message": error_info["Message"],
                }
            ),
        }

    # This shape works for an API Gateway or Lambda Function URL.
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "region": region,
                "volume_ids": volume_ids,
            }
        ),
    }
