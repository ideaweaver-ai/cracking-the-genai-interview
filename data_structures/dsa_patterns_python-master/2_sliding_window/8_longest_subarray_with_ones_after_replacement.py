# Leetcode 1004 - Max Consecutive Ones III

from typing import List

class Solution:
    # O(N) time | O(1) space
    def longestOnes(self, nums: List[int], k: int) -> int:
        max_len = 0
        # Window start and metric
        start = 0
        count_zeros = 0  # easier to validate

        for end in range(len(nums)):
            if nums[end] == 0:
                count_zeros += 1
            # Make valid
            if count_zeros > k:
                if nums[start] == 0:
                    count_zeros -= 1
                start += 1
            # Update output
            max_len = max(max_len, end - start + 1)
        return max_len


def main():
    sol = Solution()
    assert sol.longestOnes([1,1,1,0,0,0,1,1,1,1,0], 2) == 6, "test case 1 failed"
    assert sol.longestOnes([0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], 3) == 10, "test case 2 failed"


main()
