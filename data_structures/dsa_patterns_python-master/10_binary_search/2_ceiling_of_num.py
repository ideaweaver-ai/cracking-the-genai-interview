# Copyright © 2020 way2FAANG


# Time: O(log(n) | Space: O(1)
def search_ceiling_of_a_number(arr, key):
    if key > arr[-1]:
        return -1

    start, end = 0, len(arr) - 1
    while start <= end:
        mid = start + (end - start) // 2

        if key == arr[mid]:
            return mid
        elif key < arr[mid]:
            end = mid - 1
        else:
            start = mid + 1
    # when the loop terminates - the key is not found and arr[start] becomes greater than arr[end]
    # also till the last iteration key is between arr[start] and arr[end], hence the next biggest num will be arr[start]
    return start


def main():
    print(search_ceiling_of_a_number([4, 6, 10], 6))
    print(search_ceiling_of_a_number([1, 3, 8, 10, 15], 12))
    print(search_ceiling_of_a_number([4, 6, 10], 17))
    print(search_ceiling_of_a_number([4, 6, 10], -1))


main()
