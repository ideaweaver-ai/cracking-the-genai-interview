import sys

import boto3

ec2 = boto3.client("ec2")

# python3 ebs_snapshot.py vol-0123456789abcdef0
if len(sys.argv) < 2:
    print("Pass a volume id")
    sys.exit(1)

response = ec2.create_snapshot(
    VolumeId=sys.argv[1],
    Description="Snapshot created with boto3",
)
print(response["SnapshotId"])
