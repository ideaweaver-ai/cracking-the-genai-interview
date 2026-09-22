"""Demonstrates common operation costs; run with python common_operation_complexity.py."""


def list_operations():
    numbers = [10, 20, 30]
    print(numbers[1])  # Indexing is O(1).
    numbers.append(40)  # Append is amortized O(1).
    numbers.insert(1, 15)  # Middle insertion shifts items: O(n).
    print(numbers)


def hash_collections():
    phone_book = {"Ada": "555-0100"}
    tags = {"python"}
    phone_book["Lin"] = "555-0101"
    tags.add("algorithms")
    print(phone_book["Ada"], "python" in tags)  # Average lookup/membership: O(1).


def sorting_cost():
    numbers = [3, 1, 2]
    print(sorted(numbers))  # Comparison sorting is typically O(n log n).


if __name__ == "__main__":
    list_operations()
    hash_collections()
    sorting_cost()
