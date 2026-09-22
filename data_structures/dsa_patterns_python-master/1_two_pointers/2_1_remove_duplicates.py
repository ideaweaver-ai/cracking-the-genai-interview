# O(N) time | O(1) space
def remove_duplicates(arr):
    # Placeholder to track where next unique num should be placed
    next_unique_num_index = 1

    for i in range(len(arr)):
        # Imp to have check - i > 0
        # When we find a unique num, place it at next_unique_index and increment index by 1
        if i > 0 and arr[i] != arr[i - 1]:
            arr[next_unique_num_index] = arr[i]
            next_unique_num_index += 1
    return next_unique_num_index


def main():
    print(remove_duplicates([2, 3, 3, 3, 6, 9, 9]))
    print(remove_duplicates([2, 2, 2, 11]))


main()
