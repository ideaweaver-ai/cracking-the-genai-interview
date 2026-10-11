# Leetcode 567 - Find All Anagrams in a String
from typing import List

class Solution:
    # O(N+M) time | O(k) space, M - len of p, k distinct chars in p
    def findAnagrams(self, s: str, p: str) -> List[int]:
        # Output
        result = []
        # Window metric - related to pattern
        pattern_freq_map = {}
        for char in p:
            pattern_freq_map[char] = pattern_freq_map.get(char, 0) + 1
        # Window start and metric
        start = 0
        matched = 0
        for end in range(len(s)):
            right_char = s[end]
            # Expand - slightly different then others
            if right_char in pattern_freq_map:
                pattern_freq_map[right_char] -= 1
                if pattern_freq_map[right_char] == 0:
                    matched += 1
            # Validate
            if end >= len(p) - 1:
                if matched == len(pattern_freq_map):
                    result.append(start)
                # Shrink
                left_char = s[start]
                if left_char in pattern_freq_map:
                    if pattern_freq_map[left_char] == 0:
                        matched -= 1
                    pattern_freq_map[left_char] += 1
                start += 1
        return result

def main():
    sol = Solution()
    assert sol.findAnagrams("cbaebabacd", "abc") == [0,6]
    assert sol.findAnagrams("abab", "ab") == [0,1,2]

main()
