# Leetcode 567 - Permutation in String

# Brute force & alternate solution
# Brute force
# O(N*k) time | O(1) space
# def checkInclusion(s1, s2):
#     k = len(s1)
#     p_map = dict()
#     for c in s1:
#         p_map[c] = p_map.get(c, 0) + 1
#     for start in range(len(s2) - k + 1):
#         w_map = dict()
#         for end in range(start, start + k):
#             w_map[s2[end]] = w_map.get(s2[end], 0) + 1
#         if p_map == w_map:
#             return True
#     return False


# # O(N*K) time | O(K) space - N*k because has hashmap checking
# def checkInclusion(s1, s2):
#     start = 0
#     k = len(s1)
#     p_map = dict()
#     for c in s1:
#         p_map[c] = p_map.get(c, 0) + 1
#     w_map = dict()
#     for end in range(len(s2)):
#         w_map[s2[end]] = w_map.get(s2[end], 0) + 1
#         if end >= k-1:
#             if w_map == p_map:
#                 return True
#             # slide window
#             w_map[s2[start]] -= 1
#             if w_map[s2[start]] == 0:
#                 del(w_map[s2[start]])
#             start += 1
#     return False

class Solution:
    # O(N+K) time | O(K)
    # This solution is the most eficient solution
    def checkInclusion(self, s1: str, s2: str) -> bool:
        # Permutation match ~ frequency map should match for the two strings
        pattern_freq_map = {}
        for char in s1:
            pattern_freq_map[char] = pattern_freq_map.get(char, 0) + 1
        # Window start and metric
        start = 0
        matched = 0
        # slide window
        for end in range(len(s2)):
            # expand
            right_char = s2[end]
            if right_char in pattern_freq_map:
                pattern_freq_map[right_char] -= 1
                if pattern_freq_map[right_char] == 0:
                    matched += 1
            # validate
            if end >= len(s1) - 1:
                if matched == len(pattern_freq_map):
                    return True
                # shrink
                left_char = s2[start]
                if left_char in pattern_freq_map:
                    if pattern_freq_map[left_char] == 0:
                        matched -= 1
                    pattern_freq_map[left_char] += 1
                start += 1
        return False

def main():
    sol = Solution()
    assert sol.checkInclusion("ab", "eidbaooo") == True
    assert sol.checkInclusion("ab", "eidboaoo") == False

main()
