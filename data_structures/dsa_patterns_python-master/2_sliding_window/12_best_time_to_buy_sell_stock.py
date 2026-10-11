# Leetcode 121 - Best Time to Buy and Sell Stock

from typing import List

# Brute Force
# O(n**2) time | O(1) space
# def maxProfit(self, arr: List[int]) -> int:
#     # Initialize output variable
#     max_profit = 0

#     # Check each combination
#     for i in range(len(arr) - 1):
#         for j in range(i + 1, len(arr)):
#             # Validate window
#             if arr[j] > arr[i]:
#                 max_profit = max(max_profit, arr[j] - arr[i])
#     return max_profit

class Solution:
    # O(n) time | O(1) space
    def maxProfit(self, arr: List[int]) -> int:
        # Initialize output variable
        max_profit = 0  # change to -float('inf') - case where we have to transact, we cannot stay out of the market

        # Define window start, no need for window metric as prices[end] - prices[start] is our metric
        start = 0

        # Expand window
        for end in range(1, len(arr)):

            profit = arr[end] - arr[start]
            max_profit = max(max_profit, profit)
            # Validate window
            if arr[end] < arr[start]:
                start = end
        return max_profit

        # Min price seen so far
        def maxProfit(self, prices: List[int]) -> int:
            max_profit = 0
            min_price_so_far = float('inf')
            for current_price in prices:
                if current_price > min_price_so_far:
                    profit = current_price - min_price_so_far
                    max_profit = max(profit, max_profit)
                else:
                    min_price_so_far = current_price
            return max_profit


if __name__ == "__main__":
    sol = Solution()
    assert sol.maxProfit([7, 4, 1, 3, 8, 4]) == 7, "Test case 1 failed"
    assert sol.maxProfit([7, 6, 5, 3, 1]) == 0, "Test case 2 failed"
