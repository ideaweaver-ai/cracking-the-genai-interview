"""Run with python clean_solutions.py."""


def two_sum(numbers: list[int], target: int) -> list[int]:
    """Return indices of two values that add to target in O(n) time."""
    seen_indices: dict[int, int] = {}
    for index, number in enumerate(numbers):
        complement = target - number
        if complement in seen_indices:
            return [seen_indices[complement], index]
        seen_indices[number] = index
    return []


if __name__ == "__main__":
    # print(two_sum([2, 7, 11, 15], 9))
    print(two_sum([2, 7, 11, 15], 9))
