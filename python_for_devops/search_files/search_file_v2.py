import os

search_path = "/etc"
file_name = "passwd"

found = False

for root, directories, files in os.walk(search_path):
    if file_name in files:
        full_path = os.path.join(root, file_name)
        print(f"File found: {full_path}")
        found = True

if not found:
    print("File not found")
