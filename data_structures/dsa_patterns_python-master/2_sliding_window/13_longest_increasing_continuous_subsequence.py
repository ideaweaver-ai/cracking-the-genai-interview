# Leetcode 674 - Longest Continuous Increasing Subsequence
from typing import List


class Solution:
    def findLengthOfLCIS(self, nums: List[int]) -> int:
        max_len = 0
        start = 0
        for end in range(len(nums)):
            # Validate
            if end > 0 and nums[end] <= nums[end - 1]:
                # Make window valid
                start = end
            max_len = max(max_len, end - start + 1)
        return max_len


if __name__ == "__main__":
    sol = Solution()
    assert sol.findLengthOfLCIS([1, 3, 5, 4, 7]) == 3, "test case 1 failed"
    assert sol.findLengthOfLCIS([2, 2, 2, 2, 2]) == 1, "test case 2 failed"
