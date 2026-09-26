# LeetCode: 713 - Subarray Product Less Than K

from typing import List


# Time: O(n) | Space: O(1)
def numSubarrayProductLessThanK(nums: List[int], k: int) -> int:
    # Output variable
    num_subarrays = 0
    # Define window start and metric
    start, product = 0, 1

    # Expand window
    for end in range(len(nums)):
        # expand
        product *= nums[end]

        # validate
        while product >= k and start <= end:
            # shrink
            product /= nums[start]
            start += 1

        # we have a valid window
        # num of subarrays between start and end is end-start+1 (create subarrays from end to start - this way we won't double count)
        num_subarrays += end - start + 1

    return num_subarrays


def main():
    print(numSubarrayProductLessThanK([2, 5, 3, 10], 30))
    print(numSubarrayProductLessThanK([8, 2, 6, 5], 50))


main()
