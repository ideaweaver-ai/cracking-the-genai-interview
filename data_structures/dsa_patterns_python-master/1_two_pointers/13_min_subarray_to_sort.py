# Time: O(n) | Space: O(1)
def shortest_window_sort(arr):
    left, right = 0, len(arr) - 1

    # find first num out of place from left
    while left < len(arr) - 1 and arr[left] <= arr[left + 1]:
        left += 1

    # Array is already sorted
    if left == len(arr) - 1:
        return 0

    # find first num out of place from right
    while right > 0 and arr[right] >= arr[right - 1]:
        right -= 1

    # We have already checked the case of sorted array. right == 0 means arr is sorted

    # find min and max in the subarray that is out of order
    subarray_max, subarray_min = -float('inf'), float('inf')
    for i in range(left, right + 1):
        subarray_max = max(subarray_max, arr[i])
        subarray_min = min(subarray_min, arr[i])

    # find the right place for subarray min and max
    while left > 0 and arr[left - 1] > subarray_min:
        left -= 1

    while right < len(arr) - 1 and arr[right + 1] < subarray_max:
        right += 1

    return right - left + 1

