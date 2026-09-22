"""Run all examples or one: python time_complexity.py nested_loop"""


def single_loop():
    numbers = [2, 4, 6, 8]
    total = 0
    for number in numbers:  # Visits n items: O(n).
        total += number
    print(total)


def nested_loop():
    colors = ["red", "blue", "green"]
    pairs = []
    for first in colors:
        for second in colors:  # n * n comparisons: O(n^2).
            if first != second:
                pairs.append((first, second))
    print(pairs)


EXAMPLES = {"single_loop": single_loop, "nested_loop": nested_loop}

if __name__ == "__main__":
    import sys

    for example in ([sys.argv[1]] if len(sys.argv) > 1 else EXAMPLES):
        EXAMPLES[example]()
