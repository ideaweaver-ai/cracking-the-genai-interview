from pathlib import Path
import subprocess

log_file = Path("/var/log/myapp/app.log")

if not log_file.exists():
    print("Log file does not exist")

elif not log_file.is_file():
    print("Path exists, but it is not a file")

else:
    size_mb = log_file.stat().st_size / (1024 * 1024)

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
