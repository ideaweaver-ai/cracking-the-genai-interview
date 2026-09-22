"""Run all examples or one: python conditionals_and_loops.py while_loop"""


def conditionals():
    temperature = 18
    if temperature > 25:
        message = "warm"
    elif temperature >= 15:
        message = "mild"
    else:
        message = "cold"
    print(message)


def for_loop():
    for index, fruit in enumerate(["apple", "pear", "plum"]):
        print(index, fruit)


def while_loop():
    number = 0
    while number < 5:
        number += 1
        if number == 2:
            continue  # Skip this value and start the next iteration.
        if number == 4:
            break
        print(number)


EXAMPLES = {"conditionals": conditionals, "for_loop": for_loop, "while_loop": while_loop}

if __name__ == "__main__":
    import sys

    for example in ([sys.argv[1]] if len(sys.argv) > 1 else EXAMPLES):
        EXAMPLES[example]()
