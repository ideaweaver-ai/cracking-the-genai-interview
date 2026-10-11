# LeetCode: 239 - Sliding Window Maximum
# Level: Hard

from collections import deque
from typing import List


class Solution:
    # # BF - Time: O(n*k) | Space: O(1)
    # def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
    #     result = []
    #     n = len(nums)
    #     for i in range(n - k + 1):
    #         max_ = -float('inf')
    #         for j in range(i, i + k):
    #             max_ = max(max_, nums[j])
    #         result.append(max_)
    #     return result

    # Time: O(n) | Space: O(n)
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        result = []
        deq = deque()

        for i in range(len(nums)):
            # fixed window - remove any element out of the window
            while deq and deq[0] <= i - k:
                deq.popleft()

            # push the current element upto the max it can go
            # so that deque is monotonically decreasing
            # ** imp - deque is storing indices
            while deq and nums[deq[-1]] < nums[i]:
                deq.pop()
            deq.append(
                i)  # ** don't make a mistake here - deq is storing indices so we can remove elements out of the sliding window
            # append result when window size is reached
            if i >= k - 1:
                result.append(nums[deq[0]])

        return result


if __name__ == "__main__":
    sol = Solution()
    assert sol.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3,3,5,5,6,7]
