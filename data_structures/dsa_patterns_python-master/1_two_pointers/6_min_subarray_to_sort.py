# LeetCode: 581 - Shortest Unsorted Continuous Subarray

# Time: O(n) | Space: O(1)
def shortest_window_sort(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1

    # find first num out of place from left
    while left < len(nums) - 1 and nums[left] <= nums[left + 1]:
        left += 1

    # Array is already sorted
    if left == len(nums) - 1:
        return 0

    # find first num out of place from right
    while right > 0 and nums[right] >= nums[right - 1]:
        right -= 1

    # We have already checked the case of sorted array. right == 0 means arr is sorted

    # find min and max in the subarray that is out of order
    subarray_max, subarray_min = -float('inf'), float('inf')
    for i in range(left, right + 1):
        subarray_max = max(subarray_max, nums[i])
        subarray_min = min(subarray_min, nums[i])

    # Include outside elements that would prevent global sorting.
    while left > 0 and nums[left - 1] > subarray_min:
        left -= 1

    while right < len(nums) - 1 and nums[right + 1] < subarray_max:
        right += 1

    return right - left + 1


if __name__ == "__main__":
    print(shortest_window_sort([2,6,4,8,10,9,15]))
    print(shortest_window_sort([3,2,1]))
    # Expand the initial window [5, 2, 6, 4] to include 3, since 3 > 2.
    print(shortest_window_sort([1, 3, 5, 2, 6, 4, 7]))  # Expected: 5
