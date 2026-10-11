# Leetcode 76 - Minimum Window Substring

class Solution:
    # O(N) time | O(k) space (k distinct chars in map)
    def minWindow(self, s: str, t: str) -> str:
        # Output
        result_start, result_len = 0, len(s) + 1
        # Pattern metric - Pattern map
        pattern_freq_map = {}
        for char in t:
            pattern_freq_map[char] = pattern_freq_map.get(char, 0) + 1
        # Window start and metric
        start, matched = 0, 0
        for end in range(len(s)):
            # Expand
            right_char = s[end]
            if right_char in pattern_freq_map:
                pattern_freq_map[right_char] -= 1
                if pattern_freq_map[right_char] == 0:
                    matched += 1
            # Validate
            while matched == len(pattern_freq_map):
                if (end - start + 1) < result_len:
                    result_start = start
                    result_len = end - start + 1
                # Shrink - as much as possible
                left_char = s[start]
                if left_char in pattern_freq_map:
                    if pattern_freq_map[left_char] == 0:
                        matched -= 1
                    pattern_freq_map[left_char] += 1
                start += 1
        if result_len == len(s)+1:
            return ""
        return s[result_start:result_start + result_len]

def main():
    sol = Solution()
    assert sol.minWindow("ADOBECODEBANC", "ABC") == "BANC"
    assert sol.minWindow("a", "a") == "a"
    assert sol.minWindow("a", "aa") == ""

main()
