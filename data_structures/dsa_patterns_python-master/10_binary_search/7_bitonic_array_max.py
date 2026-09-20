# Copyright © 2020 way2FAANG
# LeetCode: 852


# Time: O(log(n)) | Space: O(1)
def find_max_in_bitonic_array(arr):
    start, end = 0, len(arr) - 1
    while start < end:  # ** imp - since we are going to move range to mid and not mid + 1 or mid -1
        mid = start + (end - start) // 2
        if arr[mid] < arr[mid + 1]:
            # we need to reduce array size in default case
            # if we check arr[mid] > arr[mid-1] -> start = mid. This will fail for [1, 3, 8, 12] ascending arr?
            # Because when we reach[8, 12] , start = 2, end=3, middle =2 and we are stuck in loop
            start = mid + 1  # arr[mid] cannot be max - less than the next element
        else:  # since arr is bitonic (arr[mid])>arr[mid+1])
            # we need to look at first half
            end = mid  # since arr[mid] is greater than arr[mid+1], hence it could be max
    return arr[start]  # since loop will break when start==end, arr[end] would also point to max num in array


def main():
    print(find_max_in_bitonic_array([1, 3, 8, 12, 4, 2]))
    print(find_max_in_bitonic_array([3, 8, 3, 1]))
    print(find_max_in_bitonic_array([1, 3, 8, 12]))
    print(find_max_in_bitonic_array([10, 9, 8]))
    print(find_max_in_bitonic_array([12, 8, 3, 1]))
    print(find_max_in_bitonic_array([2, 8, 5, 3, 1]))


main()
