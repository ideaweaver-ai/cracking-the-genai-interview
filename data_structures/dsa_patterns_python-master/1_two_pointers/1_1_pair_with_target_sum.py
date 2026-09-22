"""
Q: You are given an array of integers nums and an integer target, return the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Input: nums = [2,7,11,15], target = 9
Output: [2,7]

"""


#  Brute Force Solution - O(N^2) time | O(1) space
from typing import Any


def pair_with_targetsum_brute_force(arr, target_sum):
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] + arr[j] == target_sum:
                return [arr[i], arr[j]]
    return []

# O(N*log(N)) time | O(1) space
def pair_with_targetsum(arr, target_sum):
    # o/p var
    result = []
    # sort the array
    arr.sort()
    # initialize two pointers
    left, right = 0, len(arr) - 1
    while left < right:
        pair_sum = arr[left] + arr[right]
        if pair_sum == target_sum:
            return [arr[left], arr[right]]

        # Use the fact - array is sorted to increment or decrement one of the pointers
        elif pair_sum > target_sum:
            # we need to reduce pair_sum
            right -= 1
        else:
            # we need to increase pair_sum
            left += 1
    return result


# O(n) hashmap solution
def pair_with_targetsum_hashmap(arr, target_sum):
    num_index_map = {}
    for index, num in enumerate[Any](arr):
        compliment = target_sum - num
        if compliment in num_index_map:
            return [num_index_map[compliment], index]
        num_index_map[num] = index
    return [-1, -1]


if __name__ == '__main__':
    arr = [2, 7, 11, 15]
    target_sum = 9
    print(f"Brute Force: {pair_with_targetsum_brute_force(arr, target_sum)}")
    print(f"Two Pointers: {pair_with_targetsum(arr, target_sum)}")
    print(f"Hashmap: {pair_with_targetsum_hashmap(arr, target_sum)}")