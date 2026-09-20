# Copyright © 2020 way2FAANG


# Time: O(log(n)) | Space: O(1)
def search_min_diff_element(arr, key):
    def find_ceil_floor(start, end):
        while start <= end:
            mid = start + (end - start) // 2
            if key == arr[mid]:
                return [mid, mid]
            elif key < arr[mid]:
                end = mid - 1
            else:
                start = mid + 1
        return [start, end]

    # check if key is outside the array range
    if key < arr[0]:
        return arr[0]
    if key > arr[-1]:
        return arr[-1]

    # since we already tested the case where key is outside the arr range, ceil and floor will be in the array
    ceil, floor = find_ceil_floor(0, len(arr) - 1)
    if abs(arr[ceil] - key) < abs(arr[floor] - key):
        return arr[ceil]
    else:
        return arr[floor]


def main():
    print(search_min_diff_element([4, 6, 10], 7))
    print(search_min_diff_element([4, 6, 10], 4))
    print(search_min_diff_element([1, 3, 8, 10, 15], 12))
    print(search_min_diff_element([4, 6, 10], 17))


main()
