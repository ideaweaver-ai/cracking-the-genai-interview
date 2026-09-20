# Leetcode 424 - Longest Substring Without Repeating Characters

class Solution:
    # O(N) time | O(26) = O(1) space
    def characterReplacement(self, s: str, k: int) -> int:
        # initialize output variable
        max_len = 0
        # define  window start  and metric
        start = 0
        char_freq_map = {}
        # We need additional var to identify which char to keep and which chars should we replace
        max_freq = 0
        for end in range(len(s)):
            # expand
            right_char = s[end]
            char_freq_map[right_char] = char_freq_map.get(right_char, 0) + 1
            # max_freq can be updated only if current character freq becomes greater than current max_freq as we expand 1 char at a time
            max_freq = max(max_freq, char_freq_map[right_char])

            num_replacements = (end - start + 1) - max_freq
            # Imp: Logic of shrinking window is different
            # When window becomes invalid i.e num_replacements > k,
            # previous iterations we reached max_len with num_replacements = k
            # We can get a new max len only when max_freq becomes greater than current max_freq
            # for e.g max_freq = 4 when max_len=6 was acheived with k=2.
            # We can get new max_len only when max_freq = 5
            # Hence keeping window of current max_len(6) we slide window by 1 character
            # to see if max_freq of 5 can be achieved and hence new max_len

            # Validate
            if num_replacements > k:
                left_char = s[start]
                # shrink
                char_freq_map[left_char] -= 1
                start += 1
            # update result
            max_len = max(max_len, end - start + 1)
        return max_len

def main():
    sol = Solution()
    assert sol.characterReplacement("ABAB", 2) == 4, "test case 1 failed"
    assert sol.characterReplacement("AABABBA", 1) == 4, "test case 2 failed"

main()        
