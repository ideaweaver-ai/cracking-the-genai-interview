# LeetCode: 31 - Next Permutation

# Copyright © 2020 way2FAANG
# Level: Medium

from typing import List


class Solution:
    # Time: O(n) | Space: O(1)
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)

        i = n - 1
        while i > 0 and nums[i] <= nums[i - 1]:
            i -= 1

        if i > 0:
            # find the smallest num greater than nums[i-1]
            j = n - 1
            while j >= i and nums[j] <= nums[i - 1]:
                j -= 1
            # swap
            nums[i - 1], nums[j] = nums[j], nums[i - 1]

        # reverse from i to end of array
        start, end = i, n - 1
        while start < end:
            # swap
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1


if __name__ == "__main__":
    nums = [1, 2, 3]
    print(Solution().nextPermutation(nums))
