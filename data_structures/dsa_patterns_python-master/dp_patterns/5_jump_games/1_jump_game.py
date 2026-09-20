from typing import List


class Solution:
    # BF
    # Time: O(n**n) | Space: O(1)
    # def canJump(self, nums: List[int]) -> bool:
    #     def can_jump_helper(i):
    #         # base cases
    #         if i == n - 1:
    #             return True
    #
    #         if i >= n:
    #             return False
    #         # cycle - not possible to move from here, also this cannot be the last element as we already checked
    #         if nums[i] == 0:
    #             return False
    #
    #         # recursion
    #         num_steps = nums[i]
    #
    #         for j in range(1, num_steps + 1):
    #             if can_jump_helper(i + j):
    #                 return True
    #
    #         return False
    #
    #     # main function
    #     n = len(nums)
    #     return can_jump_helper(0)

    # Memoized soln
    # Time: O(n**2) | Space: O(n)
    # def canJump(self, nums: List[int]) -> bool:
    #     # Time: O(n**n) | Space: O(1)
    #     def can_jump_helper(i, memo={}):
    #         # base cases
    #         if i == n - 1:
    #             return True
    #
    #         if i >= n:
    #             return False
    #         # cycle - not possible to move from here, also this cannot be the last element as we already checked
    #         if nums[i] == 0:
    #             return False
    #
    #         # check in memo
    #         if i in memo:
    #             return memo[i]
    #
    #         # recursion
    #         num_steps = nums[i]
    #
    #         for j in range(1, num_steps + 1):
    #             if can_jump_helper(i + j):
    #                 memo[i] = True
    #                 return memo[i]
    #
    #         memo[i] = False
    #         return memo[i]
    #
    #     # main function
    #     n = len(nums)
    #     return can_jump_helper(0)

    # DP
    # Time: O(n**2) | Space: O(n)
    def canJump(self, nums: List[int]) -> bool:
        # Time: O(n) | Space: O(1)

        # main function
        n = len(nums)
        dp = [False for _ in range(n)]
        # base cases
        dp[n - 1] = True

        # recursion for loop
        for i in range(n - 2, -1, -1):
            num_steps = nums[i]
            for j in range(1, num_steps + 1):
                if i + j < n and dp[i + j]:
                    dp[i] = True
                    break  # since we already have soln for i

        return dp[0]


if __name__ == "__main__":
    nums = [2, 3, 1, 1, 4]
    print(Solution().canJump(nums))