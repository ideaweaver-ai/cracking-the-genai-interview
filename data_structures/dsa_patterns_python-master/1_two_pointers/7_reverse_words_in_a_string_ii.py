# LeetCode: 186 - Reverse Words in a String II
# Time: O(n) | Space: O(1)
from typing import List


class Solution:
    def reverseWord(self, s: List[str], left: int, right: int) -> None:
        if left == right:
            return
        while left < right:
            # Swap characters.
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1

    def reverseWords(self, s: List[str]) -> None:
        """Do not return anything, modify s in-place instead."""
        if len(s) == 0:
            return

        # Reverse the entire sentence.
        self.reverseWord(s, 0, len(s) - 1)

        word_start, word_end = 0, None
        word_found = False
        for i in range(len(s)):
            if s[i].isspace():
                word_end = i - 1
                word_found = True
            elif i == len(s) - 1:
                word_end = i
                word_found = True

            if word_found:
                self.reverseWord(s, word_start, word_end)
                word_start = i + 1
                word_found = False


if __name__ == "__main__":
    s = ["t", "h", "e", " ", "s", "k", "y", " ", "i", "s", " ", "b", "l", "u", "e"]
    expected = ["b", "l", "u", "e", " ", "i", "s", " ", "s", "k", "y", " ", "t", "h", "e"]
    Solution().reverseWords(s)
    assert s == expected
    print(s)
