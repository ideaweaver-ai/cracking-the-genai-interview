# Copyright © 2020 way2FAANG
# LeetCode: 1095


# 1. find index of max num in bitonic array
# 2. define order agnostic binary search
# 3. perform binary search from start to mid with is_ascending=True
# 4. perform binary search from mid+1 to end with is_ascending=False


# Time: O(log(n)) | Space: O(1)
def search_bitonic_array(arr, key):
    # Time: O(log(n)) | Space: O(1)
    def find_max_index():
        # returns index of max in bitonic array
        start, end = 0, len(arr) - 1
        while start < end:
            mid = start + (end - start) // 2
            if arr[mid] < arr[mid + 1]:
                start = mid + 1
            else:
                end = mid
        # loop will break when start == end, so you can return either
        return start

    # Time: O(log(n)) | Space: O(1)
    # order-agnostic binary search
    def binary_search(start, end, is_ascending):
        while start <= end:
            mid = start + (end - start) // 2

            if key == arr[mid]:
                return mid

            if is_ascending:  # array sorted in ascending order
                if key < arr[mid]:
                    # search in first half
                    end = mid - 1
                else:  # key > arr[mid]
                    # search in second half
                    start = mid + 1
            else:  # array sorted in descending order
                if key < arr[mid]:
                    # search in second half - hint: opposite of is_ascending
                    start = mid + 1
                else:  # key > arr[mid]
                    # search in first half
                    end = mid - 1
        return -1

    max_index = find_max_index()  # O(log(n))

    key_index = binary_search(0, max_index, True)  # O(log(n))
    if key_index != -1:
        return key_index

    key_index = binary_search(max_index + 1, len(arr) - 1, False)  # O(log(n))
    return key_index


def search_bitonic_array(arr, key):
    start, end = 0, len(arr) - 1
    result = -1
    while start <= end:
        mid = start + (end - start) // 2
        if arr[start] <= arr[mid]:
            # first half is sorted
            result = binary_search(arr, key, start, mid, True)
            start = mid + 1
        else:
            # second half is sorted
            result = binary_search(arr, key, mid, end, False)
            end = mid - 1

        if result != -1:
            break
    return result


# Another way- In each iteration we can find which section is sorted and search in that
# Time: O(log(n)) | Space: O(1)
def binary_search(arr, key, start, end, is_asc):
    while start <= end:
        mid = start + (end - start) // 2
        if arr[mid] == key:
            return mid

        if is_asc:
            if key > arr[mid]:
                start = mid + 1
            else:
                end = mid - 1
        else:
            if key > arr[mid]:
                end = mid - 1
            else:
                start = mid + 1

    return -1


def main():
    print(search_bitonic_array([1, 3, 8, 4, 3], 4))
    print(search_bitonic_array([3, 8, 3, 1], 8))
    print(search_bitonic_array([1, 3, 8, 12], 12))
    print(search_bitonic_array([10, 9, 8], 10))


main()
