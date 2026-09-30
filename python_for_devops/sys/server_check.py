import sys
import subprocess

if len(sys.argv) < 2:
    print("Usage: python check_server.py <hostname>")
    sys.exit(1)

server = sys.argv[1]

print(f"Checking connectivity to {server}...")

subprocess.run(["ping", "-c", "4", server])
