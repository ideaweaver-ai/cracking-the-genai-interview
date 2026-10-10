# Leetcode 3 - Longest Substring Without Repeating Characters
# This problem is unique. In the problems before we mostly expand the window ( add end element to window in first line fo for loop)
# In this problem we need to validate first & shrink the window to make it valid before we expand it

class Solution:
    # O (n) time | O(K) space where K is the number of distinct characters
    def lengthOfLongestSubstring(self, s: str) -> int:
        # initialize Output/result
        max_len = 0
        # define window start and window metric
        start = 0
        char_index_map = {}  # can you figure out why index and not requency
        # slide window
        for end in range(len(s)):
            right_char = s[end]
            # validate ** imp -in this case we need to validate before adding ?
            # if we add right_char to the char_index_map before we will overwrite its previous index,
            # hence we will not know if the char is repeating
            # if right_char is already in the map, adding right_char to window will make it invalid
            if right_char in char_index_map:
                # shrink window

                # In current window right_char's position can be given by value of right_char key
                # right_char cannot be present in current window at any other index
                # Hence move start 1 character ahead of right_char's previous index
                # tricky - what if case start is already ahead of that # e.g. 'abccbad' - second 'b'
                start = max(start, char_index_map[right_char] + 1)
            # expand window
            char_index_map[right_char] = end
            # update result
            max_len = max(max_len, end - start + 1)
        return max_len

def main():
    sol = Solution()
    assert sol.lengthOfLongestSubstring("abcabcbb") == 3, "test case 1 failed"
    assert sol.lengthOfLongestSubstring("bbbbb") == 1, "test case 2 failed"
    assert sol.lengthOfLongestSubstring("pwwkew") == 3, "test case 3 failed"

main()
