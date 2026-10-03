import boto3

ec2 = boto3.resource("ec2")

def lambda_handler(event, context):

    vol_status = {
        "Name": "status",
        "Values": ["available"]
    }

    for volume in ec2.volumes.filter(Filters=[vol_status]):
        print(f"Volume {volume.id} is available")

        volume.delete()

        print(f"Deleted volume {volume.id}")

    return {
        "statusCode": 200,
        "body": "Available EBS volumes deleted successfully"
    }
