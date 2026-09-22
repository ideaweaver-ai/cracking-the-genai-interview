"""Run all examples or one: python 03_string_functions.py common_functions"""


def common_functions():
    message = "  Python Basics  "
    cleaned = message.strip().lower()
    print(cleaned, cleaned.replace("basics", "strings"))
    print(cleaned.startswith("python"), cleaned.find("basics"))


def split_and_join():
    words = "learn python one step at a time".split()
    print(words, "-".join(words))


def build_string_in_linear_time():
    characters = []
    for character in "python":
        characters.append(character.upper())
    # List appends plus one join build the final string in O(n) total time.
    print("".join(characters))


EXAMPLES = {
    "common_functions": common_functions,
    "split_and_join": split_and_join,
    "linear_build": build_string_in_linear_time,
}

if __name__ == "__main__":
    import sys

    for example in ([sys.argv[1]] if len(sys.argv) > 1 else EXAMPLES):
        EXAMPLES[example]()
