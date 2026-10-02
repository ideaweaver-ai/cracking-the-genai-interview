from pathlib import Path

search_path = Path("/etc")

for file in search_path.rglob("passwd"):
    print(file)
