# Copyright © 2020 way2FAANG
# LeetCode: 704


# Time: O(log(n)) | Space: O(1)
def binary_search(arr, key):
    start, end = 0, len(arr) - 1
    is_ascending = arr[start] < arr[end]  # identify order of sorting

    while start <= end:  # to have equal to sign - middle can be calculated with just 1 value in array
        # Calculate mid - this way avoids overflow in other languages
        mid = start + (end - start) // 2

        # key found - return index
        if key == arr[mid]:
            return mid

        # array is in ascending order
        if is_ascending:
            # key is less than arr[mid], so it must be in first half
            if key < arr[mid]:
                end = mid - 1  # focus our search on first half (second half elimiated from next iteration)
            else:
                # key is greater than arr[mid], so it must be in second half
                start = mid + 1  # focus our search on second half (first half elimiated from next iteration)
        # array us in descending order
        else:
            # key is less than arr[mid], so it must be in second half as array is sorted in descending order
            if key < arr[mid]:
                start = mid + 1
            else:
                # key is greater than arr[mid], so it must be in first half as array is sorted in ascending order
                end = mid - 1
    return -1  # key not found


def main():
    print(binary_search([4, 6, 10], 10))
    print(binary_search([1, 2, 3, 4, 5, 6, 7], 5))
    print(binary_search([10, 6, 4], 10))
    print(binary_search([10, 6, 4], 4))


main()
