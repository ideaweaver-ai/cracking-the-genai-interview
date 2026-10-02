import os

search_path = "/etc"
file_name = "passwd"

for root, directories, files in os.walk(search_path):
    print(f"Searching in {root}")
    if file_name in files:
        print(os.path.join(root, file_name))
