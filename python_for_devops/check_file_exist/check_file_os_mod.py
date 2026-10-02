import os

path = "/etc/passwd"

if not os.path.exists(path):
    print("Path does not exist")

elif os.path.isfile(path):
    print("It is a file")

elif os.path.isdir(path):
    print("It is a directory")
