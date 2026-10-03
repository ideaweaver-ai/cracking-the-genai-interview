import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh.connect('ec2-35-92-32-123.us-west-2.compute.amazonaws.com', username='plakhera', password='abc123')
ssh.connect('hostname', username='ec2-user', key_filename='')
stdin, stdout, stderr = ssh.exec_command('free -m')

print(stdout.read().decode('utf-8'))

ssh.close()
