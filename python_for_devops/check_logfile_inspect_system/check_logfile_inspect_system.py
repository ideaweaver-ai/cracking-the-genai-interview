import os
import subprocess

log_file = "/var/log/myapp/app.log"

if not os.path.exists(log_file):
    print("Log file does not exist")

elif not os.path.isfile(log_file):
    print("Path exists, but it is not a file")

else:
    size = os.path.getsize(log_file)
    size_mb = size / (1024 * 1024)

    print(f"Log file size: {size_mb:.2f} MB")

    if size_mb > 100:
        print("Warning: Log file is larger than 100 MB")

print("\nDisk Usage:")

result = subprocess.run(
    ["df", "-h"],
    capture_output=True,
    text=True
)

print(result.stdout)
