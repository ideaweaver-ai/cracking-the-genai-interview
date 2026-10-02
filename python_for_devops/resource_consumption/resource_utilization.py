import subprocess

commands = [
    ["ps", "aux", "--sort=-%cpu"],
    ["ps", "aux", "--sort=-%mem"],
    ["pidstat", "-d", "1", "2"],
    ["ss", "-tunap"]
]

for command in commands:

    print("\nRunning:", " ".join(command))
    print("-" * 50)

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Command failed")
            print(result.stderr)

    except FileNotFoundError:
        print(f"{command[0]} command is not installed")

    except subprocess.TimeoutExpired:
        print("Command took too long to complete")
