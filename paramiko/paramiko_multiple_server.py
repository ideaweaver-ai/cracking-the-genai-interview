import paramiko

servers = [
    'hostname1',
    'hostname2'
]

username = 'plakhera'
password = 'password'
command = 'free -m'

for host in servers:
    print(f'===== {host} =====')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
        print(stdout.read().decode('utf-8'))
        error = stderr.read().decode('utf-8').strip()
        if error:
            print(error)
    except Exception as exc:
        print(f'Failed: {exc}')
    finally:
        ssh.close()
