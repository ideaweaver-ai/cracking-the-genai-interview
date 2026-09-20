# Copyright © 2020 way2FAANG
# LeetCode: 642

from typing import List


class Solution:
    # DP approach
    # Time: O(n) | Space: O(n) additional space for storing max_left and max_right heights
    def trap(self, height: List[int]) -> int:
        # Output var
        trapped_water = 0

        # value at index i indicates max height to left of i (upto i-1)
        max_left = [0 for _ in range(len(height))]
        # value at index i indicates max height to right of i (upto i+1)
        max_right = [0 for _ in range(len(height))]

        # Upload max height to left of i
        for i in range(1, len(height)):
            max_left[i] = max(max_left[i - 1], height[i - 1])

        # Upload max height to right of i
        for i in range(len(height) - 2, -1, -1):
            max_right[i] = max(max_right[i + 1], height[i + 1])

        for i in range(len(height)):
            # water level at i
            water_level = min(max_left[i], max_right[i])
            trapped_water += max(0, water_level - height[i])

        return trapped_water
