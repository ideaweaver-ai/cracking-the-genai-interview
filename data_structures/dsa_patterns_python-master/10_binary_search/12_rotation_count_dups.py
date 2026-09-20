# Copyright © 2020 way2FAANG
# LeetCode: 154


# Time: O(log(n)) | Space : O(1)
def count_rotations(arr):
    start, end = 0, len(arr) - 1
    while start < end:
        mid = start + (end - start) // 2

        # if mid is smaller than the previous element
        if mid > start and arr[mid] < arr[mid - 1]:
            return mid

        # if mid is greater than the next element
        if mid < end and arr[mid + 1] < arr[mid]:
            return mid + 1

        # if numbers at indices start, mid, and end are same, we can't choose a side
        # the best we can do is to skip one number from both ends if they are not the smallest number
        if arr[start] == arr[mid] and arr[end] == arr[mid]:
            if arr[start+1] < arr[start]:  # if element at start+1 is not the smallest
                return start + 1
            start += 1
            if arr[end] < arr[end-1]:  # if the element at end is not the smallest
                return end
            end -= 1

        # left side is sorted, so the pivot is on right side
        if arr[start] < arr[mid] or (arr[start] == arr[mid] and arr[mid] > arr[end]):
            start = mid + 1
        else:  # right side is sorted, so the pivot is on the left side
            end = mid - 1

    # when execution reaches this line means it couldnt find an element smaller than previous element in the arr
    return 0  # the array has not been rotated


def main():
    print(count_rotations([10, 15, 1, 3, 8]))
    print(count_rotations([4, 5, 7, 9, 10, -1, 2]))
    print(count_rotations([1, 3, 8, 10]))
    print(count_rotations([6, 5, 4, 3, 2, 1]))


main()
