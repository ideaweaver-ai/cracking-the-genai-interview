"""Run all examples or one: python sorting_algorithms.py merge_sort"""


def insertion_sort(values):
    result = values[:]
    for index in range(1, len(result)):
        current = result[index]
        position = index - 1
        while position >= 0 and result[position] > current:
            result[position + 1] = result[position]
            position -= 1
        result[position + 1] = current
    return result


def bubble_sort(values):
    result = values[:]
    for end in range(len(result) - 1, 0, -1):
        for index in range(end):
            if result[index] > result[index + 1]:
                result[index], result[index + 1] = result[index + 1], result[index]
    return result


def merge_sort(values):
    if len(values) <= 1:
        return values
    middle = len(values) // 2
    left, right = merge_sort(values[:middle]), merge_sort(values[middle:])
    merged = []
    while left and right:
        merged.append(left.pop(0) if left[0] < right[0] else right.pop(0))
    return merged + left + right


def quick_sort(values):
    if len(values) <= 1:
        return values
    pivot = values[len(values) // 2]
    return quick_sort([item for item in values if item < pivot]) + [item for item in values if item == pivot] + quick_sort([item for item in values if item > pivot])


def sorting_patterns():
    records = [("Ada", 91), ("Lin", 84)]
    numbers = [3, 1, 2]
    print(sorted(numbers), sorted(records, key=lambda record: record[1]), sorted(numbers, reverse=True))


EXAMPLES = {"insertion_sort": insertion_sort, "bubble_sort": bubble_sort, "merge_sort": merge_sort, "quick_sort": quick_sort, "patterns": sorting_patterns}

if __name__ == "__main__":
    import sys

    selected = [sys.argv[1]] if len(sys.argv) > 1 else EXAMPLES
    for example in selected:
        if example == "patterns":
            EXAMPLES[example]()
        else:
            print(EXAMPLES[example]([5, 2, 4, 1, 3]))
