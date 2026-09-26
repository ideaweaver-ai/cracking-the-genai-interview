# LeetCode: 11 - Container With Most Water

# Copyright © 2020 way2FAANG
# Level: Medium
from typing import List


# class Solution:
#     #  BF Time: O(n**2) | Space: O(1)
#     def maxArea(self, height: List[int]) -> int:
#         max_area = 0
#         n = len(height)
#         for i in range(n-1):
#             for j in range(i+1, n):
#                 current_area = (j-i) * min(height[i], height[j])
#                 max_area = max(max_area, current_area)
#         return max_area


class Solution:
    # Time: O(n) | Space: O(1)
    def maxArea(self, height: List[int]) -> int:
        max_area = 0
        left, right = 0, len(height) - 1
        while left < right:
            current_area = (right - left) * min(height[left], height[right])
            max_area = max(max_area, current_area)
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return max_area


if __name__ == "__main__":
    print(Solution().maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]))
