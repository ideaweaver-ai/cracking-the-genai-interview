"""Run all examples or one: python list_comprehensions.py filter"""


def transform():
    squares = [number * number for number in range(1, 6)]
    print(squares)


def filter_values():
    even_numbers = [number for number in range(10) if number % 2 == 0]
    print(even_numbers)


def nested():
    coordinates = [(row, column) for row in range(2) for column in range(3)]
    print(coordinates)


EXAMPLES = {"transform": transform, "filter": filter_values, "nested": nested}

if __name__ == "__main__":
    import sys

    for example in ([sys.argv[1]] if len(sys.argv) > 1 else EXAMPLES):
        EXAMPLES[example]()
