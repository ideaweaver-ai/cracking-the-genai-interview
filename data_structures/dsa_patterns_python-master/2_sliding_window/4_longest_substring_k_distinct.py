# Leetcode 340 - Longest Substring with At Most K Distinct Characters

# O(N) time | O(1) space - max 26 chars ( or 36 including digits)
class Solution:
    def lengthOfLongestSubstringKDistinct(self, s: str, k: int) -> int:
        # input validation - do it later (during interviews)
        if s is None or k <= 0:
            return 0

        # initialize output variable
        max_len = 0
        # define window start and window metric
        start = 0
        char_freq_map = {}

        # slide window
        for end in range(len(s)):
            # expand window
            right_char = s[end]
            char_freq_map[right_char] = char_freq_map.get(right_char, 0) + 1
            # validate window
            while len(char_freq_map) > k:
                # shrink window
                left_char = s[start]
                char_freq_map[left_char] -= 1
                if char_freq_map[left_char] == 0:
                    del char_freq_map[left_char]
                start += 1

            # update result
            # window is valid at this point
            max_len = max(max_len, end - start + 1)
        return max_len

def main():
    sol = Solution()
    assert sol.lengthOfLongestSubstringKDistinct("eceba", 2) == 3, "test case 1 failed"
    assert sol.lengthOfLongestSubstringKDistinct("aa", 1) == 2, "test case 2 failed"

main()
