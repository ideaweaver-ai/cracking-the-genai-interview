# Leetcode 209 Minimum Size Subarray Sum

from typing import List


# O(n) time | O(1) space
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        # initialize output
        min_len = len(nums)+1

        # define window start and window metric
        start, sum_ = 0, 0

        # slide window
        for end in range(len(nums)):
            # expand window
            sum_ += nums[end]
            # validate window
            while sum_ >= target:
                # window is valid
                # update result
                min_len = min(min_len, end - start + 1)
                # shrink window
                # we are using 'while' to shrink window as much as possible while having sum >= S
                sum_ -= nums[start]
                start += 1
        return min_len if min_len != len(nums)+1 else 0

# Note:
# Sliding window will not work if it has negative elements ?
# because when we shrink window we cant be certain that the new sum will be smaller

# Not needed for leetcode. The next block is only for testing locally
def main():
    sol = Solution()
    assert sol.minSubArrayLen(7, [2,3,1,2,4,3]) == 2, "test case 1 failed"
    assert sol.minSubArrayLen(4, [1,4,4]) == 1, "test case 2 failed"
    assert sol.minSubArrayLen(11, [1,1,1,1,1,1,1,1]) == 0, "test case 3 failed"

main()
