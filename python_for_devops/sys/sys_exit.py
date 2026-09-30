import sys
import os

if os.path.exists("test.txt"):
    print("File exists")
else:
    print("File does not exist")
    sys.exit(1)
