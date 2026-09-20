# Copyright © 2020 way2FAANG
# LeetCode: 1209
# 1209. Remove All Adjacent Duplicates in String II

class Solution:
    # Time: O(n) | Space: O(n)
    def removeDuplicates(self, s: str, k: int) -> str:
        stack = []

        for char in s:
            if stack and stack[-1][0] == char:
                stack[-1][1] += 1
                if stack[-1][1] == k:
                    stack.pop()
            else:
                stack.append([char, 1])

        return "".join(c * k for c, k in stack)