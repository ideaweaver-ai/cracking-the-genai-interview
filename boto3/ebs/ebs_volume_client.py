import boto3

ec2 = boto3.client("ec2")

response = ec2.describe_volumes(
    Filters=[
        {
            "Name": "status",
            "Values": ["available"]
        }
    ]
)

for volume in response["Volumes"]:
    volume_id = volume["VolumeId"]

    print(f"Volume {volume_id} is available")

    ec2.delete_volume(VolumeId=volume_id)

    print(f"Deleted volume {volume_id}")
