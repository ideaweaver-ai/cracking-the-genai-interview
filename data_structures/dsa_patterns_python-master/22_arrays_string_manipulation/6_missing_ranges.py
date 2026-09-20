# Copyright © 2020 way2FAANG
# LeetCode: 163
# level: easy

from typing import List


class Solution:
    def findMissingRanges(self, nums: List[int], lower: int, upper: int) -> List[str]:
        result = []
        i = 0
        # empty array
        if not nums:
            if lower == upper:
                return [f"{lower}"]
            else:
                return [f"{lower}->{upper}"]
        # non empty array
        self.add_range(lower, nums[0] - 1, result)
        while i < len(nums) - 1:
            if nums[i + 1] != nums[i] + 1:
                # start = nums[i]+1
                # end = nums[i+1]-1
                # if start == end:
                #     result.append(str(start))
                # else:
                #     result.append(f"{start}->{end}")
                self.add_range(nums[i] + 1, nums[i + 1] - 1, result)
            i += 1
        self.add_range(nums[-1] + 1, upper, result)
        return result

    def add_range(self, start, end, result):
        if start > end:
            return
        if start == end:
            result.append(str(start))
        else:
            result.append(f"{start}->{end}")
