# Copyright © 2020 way2FAANG
# LeetCode: 81


def search_rotated_with_duplicates(arr, key):
    start, end = 0, len(arr)-1
    while start <= end:
        mid = start + (end-start)//2

        if key == arr[mid]:
            return mid

        while start <= end and arr[start] == arr[mid] and arr[mid] == arr[end]:
            start += 1
            end -= 1
            # update start and end and move to next iteration

        if arr[start] <= arr[mid]:  # first half sorted
            if arr[start] <= key < arr[mid]:
                end = mid - 1
            else:
                start = mid + 1

        else:  # second half sorted
            if arr[mid] < key <= arr[end]:
                start = mid + 1
            else:
                end = mid - 1

    return -1


def main():
  print(search_rotated_with_duplicates([3, 7, 3, 3, 3], 7))


main()


