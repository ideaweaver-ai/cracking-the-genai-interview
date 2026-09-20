# Copyright © 2020 way2FAANG
# LeetCode: 34


# Time: O(log(n)) | Space: O(1)
def find_range(arr, key):
    result = [- 1, -1]
    result[0] = binary_search(arr, key, True)
    if result[0] != -1:
        result[1] = binary_search(arr, key, False)
    return result


def binary_search(arr, key, find_first_matching_index):
    """Returns first matching index or last matching index of the key. Returns -1 of key not present in the array"""
    key_index = -1
    start, end = 0, len(arr) - 1

    while start <= end:
        mid = start + (end - start) // 2

        if key == arr[mid]:
            # key present in the array
            # update the index
            key_index = mid
            if find_first_matching_index:
                # since we are trying to find the first matching index for the key - go left
                end = mid - 1
            else:
                # since we are trying to find the last matching index for the key- go right
                start = mid + 1

        # normal binary search
        # be careful - use elif and not if
        elif key < arr[mid]:
            end = mid - 1
        else:
            start = mid + 1

    return key_index


# Have a look at recursive solution (for understanding) only when you have spare time. Iterative solution is better
# # Time: O(log(n)) | Space: O(log(n))
# def find_range(arr, key):
#     result = [float('inf'), -float('inf')]
#     binary_search_recursive(0, len(arr) - 1, arr, key, result)
#     return result if result[0] != float('inf') else [-1, -1]
#
#
# def binary_search_recursive(start, end, arr, key, result):
#     """Updates the range of the key in the result"""
#     # base case
#     if start > end:
#         return
#
#     # recursive calls
#     mid = start + (end - start) // 2
#     if key == arr[mid]:
#         result[0] = min(result[0], mid)
#         result[1] = max(result[1], mid)
#         binary_search_recursive(start, mid - 1, arr, key, result)
#         binary_search_recursive(mid + 1, end, arr, key, result)
#
#     if key < arr[mid]:
#         binary_search_recursive(start, mid - 1, arr, key, result)
#     else:
#         binary_search_recursive(mid + 1, end, arr, key, result)


def main():
    print(find_range([4, 6, 6, 6, 9], 6))
    print(find_range([1, 3, 8, 10, 15], 10))
    print(find_range([1, 3, 8, 10, 15], 12))


main()
