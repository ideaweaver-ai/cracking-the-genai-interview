import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('hostname', username='plakhera', password='password')

stdin, stdout, stderr = ssh.exec_command('free -m')

print(stdout.read().decode('utf-8'))

ssh.close()
