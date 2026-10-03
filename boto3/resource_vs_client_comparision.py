import boto3

session = boto3.session.Session(profile_name="abc")
sts = session.client("sts")

identity = sts.get_caller_identity()

print("AWS Account:", identity["Account"])
print("AWS Identity:", identity["Arn"])

# After verification, create the service client
ec2 = session.client("ec2")
