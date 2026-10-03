import os

file = "/etc/passwd"

size = os.path.getsize(file)

print(size)
