"""Run all examples or one: python variables_and_types.py strings"""


def variables():
    name = "Ada"
    age = 28
    print(f"{name} is {age} years old")


def basic_types():
    count, price, active, missing = 3, 4.99, True, None
    print(type(count), type(price), active, missing)


def strings():
    word = "python"
    print(word[0], word[1:4], word + " basics")
    print("-".join(character.upper() for character in word))
    # Strings are immutable: create a new string instead of changing one character.
    print(word.replace("p", "P", 1))


EXAMPLES = {"variables": variables, "types": basic_types, "strings": strings}

if __name__ == "__main__":
    import sys

    for example in ([sys.argv[1]] if len(sys.argv) > 1 else EXAMPLES):
        EXAMPLES[example]()
