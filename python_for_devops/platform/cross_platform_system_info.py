import platform
import subprocess

os_name = platform.system()

print("Detected OS:", os_name)

if os_name == "Linux":
    print("Running Linux commands...")

    subprocess.run(["uname", "-a"])
    subprocess.run(["df", "-h"])

elif os_name == "Darwin":
    print("Running macOS commands...")

    subprocess.run(["sw_vers"])
    subprocess.run(["df", "-h"])

else:
    print("This script is designed for Linux and macOS.")
