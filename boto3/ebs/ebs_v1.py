# # https://docs.aws.amazon.com/boto3/latest/reference/services/
import boto3

# #iam = boto3.client('iam')
# ec2 = boto3.client('ec2')
# https://docs.aws.amazon.com/boto3/latest/reference/services/ec2/service-resource/volumes.html
#https://github.com/100daysofdevops/100daysofdevops/blob/master/boto3/cleaning_old_ebs_vol/cleaning_old_ebs_vol.py
ec2 = boto3.resource('ec2')
#print(ec2.volumes.all())
#for volume in ec2.volumes.all():
#    print(volume.id)

vol_status={"Name":"status","Values":["available"]}
for volume in ec2.volumes.filter(Filters=[vol_status]):
    print(f"volume {volume.id} is available")
    volume.delete()
    print(f"Deleted volume {volume.id}")
