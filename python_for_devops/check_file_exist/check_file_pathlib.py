from pathlib import Path

path = Path("/etc/passwd")

if not path.exists():
    print("Path does not exist")

elif path.is_file():
    print("It is a file")

elif path.is_dir():
    print("It is a directory")
