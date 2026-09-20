# Copyright © 2020 way2FAANG
# LeetCode: 33


# Time: O(log(n)) | Space: O(1)
def search_rotated_array(arr, key):
    start, end = 0, len(arr) - 1
    while start <= end:
        mid = start + (end - start) // 2
        if key == arr[mid]:
            return mid

        if arr[start] < arr[mid]:  # first half is sorted
            # Remember we need only one side to be sorted for searching
            # hence we can frame search condition based on this side
            if arr[start] <= key < arr[mid]:
                end = mid - 1
            else:
                start = mid + 1
        else:  # second half is sorted
            if arr[mid] < key <= arr[end]:
                start = mid + 1
            else:
                end = mid - 1
    return -1


def main():
    print(search_rotated_array([10, 15, 1, 3, 8], 15))
    print(search_rotated_array([4, 5, 7, 9, 10, -1, 2], 10))


main()
