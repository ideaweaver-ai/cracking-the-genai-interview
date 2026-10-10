# Leetcode #904. Fruit Into Baskets
# This is the same problem as longest substrings with k distinct characters (problem 4)
# trees = array, 2 baskets = 2 distinct characters
# Rephrase as find maximum continuous subarray with at most 2 distinct characters

from typing import List

# O(n) time | O(1) space
class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        if fruits is None or len(fruits) == 0:
            return 0
        # actual algo
        start = 0
        fruit_freq_map = {}
        max_fruits = 0
        for end in range(len(fruits)):
            right_fruit = fruits[end]
            fruit_freq_map[right_fruit] = fruit_freq_map.get(right_fruit, 0) + 1
            while len(fruit_freq_map) > 2:
                left_fruit = fruits[start]
                fruit_freq_map[left_fruit] -=  1
                if fruit_freq_map[left_fruit] == 0:
                    del fruit_freq_map[left_fruit]
                start += 1
            max_fruits = max(max_fruits, end - start + 1)
        return max_fruits


def main():
    sol = Solution()
    assert sol.totalFruit([1,2,1]) == 3, "test case 1 failed"
    assert sol.totalFruit([0,1,2,2]) == 3, "test case 2 failed"
    assert sol.totalFruit([1,2,3,2,2]) == 4, "test case 3 failed"

main()
