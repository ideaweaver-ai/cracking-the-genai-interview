from typing import List
from collections import deque


class Solution:
    # Recursion
    # Time = O(n**k) | Space: O(n)
    # def maxResult(self, nums: List[int], k: int) -> int:
    #     def helper(i):
    #         # base cases
    #         if i == len(nums) - 1:
    #             return nums[-1]
    #
    #         # recursive cases
    #         max_sum = -float('inf')
    #         j = i + 1
    #         while j < len(nums) and j < i + k + 1:
    #             max_sum = max(max_sum, helper(j))
    #             j += 1
    #         return nums[i] + max_sum
    #
    #     return helper(0)

    # Top down Dp
    # Time = O(n*k) | Space: O(n)
    def maxResult(self, nums: List[int], k: int) -> int:
        n = len(nums)
        dp = [-float('inf') for _ in range(n)]

        # base cases
        dp[n - 1] = nums[n - 1]

        # recursion
        for i in range(n - 2, -1, -1):
            max_sum = -float('inf')
            j = i + 1
            # how can we reduce this O(k) loop
            while j < n and j < i + k + 1:
                max_sum = max(max_sum, dp[j])
                j += 1
            dp[i] = nums[i] + max_sum

        return dp[0]

    # Bottom up Dp - easier to understand for deque
    # Time = O(n*k) | Space: O(n)
    # def maxResult(self, nums: List[int], k: int) -> int:
    #     n = len(nums)
    #     dp = [-float('inf') for _ in range(n)]
    #     # base cases
    #     dp[0] = nums[0]
    #     # recursion
    #     for i in range(1, n):
    #         max_sum = -float('inf')
    #         j = i - 1
    #         # how can we reduce this O(k) loop
    #         while j > 0 and j < i - k - 1:
    #             max_sum = max(max_sum, dp[j])
    #             j -= 1
    #         dp[i] = nums[i] + max_sum
    #
    #     return dp[n-1]

    # Time = O(n) | Space: O(n)
    def maxResult(self, nums: List[int], k: int) -> int:
        n = len(nums)
        dp = [0 for _ in range(n)]
        # base cases
        dp[0] = nums[0]

        # int deque
        deq = deque()
        deq.append(0)
        # recursion
        for i in range(1, n):

            # how can we reduce this O(k) loop
            # use monotonic deque - sliding window max
            if deq and deq[0] < i - k:
                deq.popleft()

            dp[i] = dp[deq[0]] + nums[i]

            while deq and dp[i] >= dp[deq[-1]]:
                deq.pop()
            deq.append(i)

        return dp[n - 1]


if __name__ == "__main__":
    arr = [1, -1, -2, 4, -7, 3]
    sol = Solution()
    print(sol.maxResult(arr, 2))
