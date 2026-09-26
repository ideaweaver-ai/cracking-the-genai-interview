# LeetCode: 15 - 3Sum

from typing import List

# Algo
# When we are asked to find any sum, triplets, quadruplets, five_number_sum etc
# 1. sort array if not sorted
# 2. write generic pair_sum function that can find multiple pairs adding to target sum and handle duplicates
# 3. Number of for loops required in main function = m - 2 i.e. triplets = 3-2, quadruplets = 4-2, five_num_sum = 5-2
# These for loops will cover all unique combinations for remaining  numbers (for target sum) in the array
# 4. Call pair_sum in each for loop
# 5. Compared to brute force this algo will reduce time complexity by one order

# Time: O(n^2) | Space: O(n) sorting + O(k) output; k = number of triplets
def threeSum(nums: List[int]) -> List[List[int]]:
    triplets = []
    n = len(nums)
    nums.sort()
    for i in range(len(nums)-2):
        if i > 0 and nums[i] == nums[i - 1]:  # unique pairs - imp check
            continue
        left, right = i + 1, n - 1
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            if current_sum == 0:
                triplets.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                # Handle duplicates
                # Need to check left < right in these cases
                # because while handling duplicates our left may cross right making it an invalid case
                # e.g. [2, 2, 2, 2, 1] target_sum =3
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
            elif current_sum > 0:
                right -= 1
            else:
                left += 1
    return triplets


# Extract pair_sum function from threeSum
# def two_sum(nums: List[int], left: int, right: int, target: int) -> List[int]:
#         left, right = left, right
#         pairs = []
#         while left < right:
#             current_sum = nums[left] + nums[right]
#             if current_sum == target:
#                 pairs.append([nums[left], nums[right]])
#                 # skip duplicates
#                 left += 1
#                 while left < right and nums[left] == nums[left-1]:
#                     left += 1
#                 right -= 1
#                 while left < right and nums[right] == nums[right+1]:
#                     right -= 1
#             elif current_sum < target:
#                 left += 1
#             else:
#                 right -= 1
#         return pairs

# def three_sum(nums: List[int]) -> List[List[int]]:
#     nums.sort()
#     triplets = []
#     for i in range(len(nums)):
#         # skip dups
#         if i > 0 and nums[i] == nums[i-1]:
#             continue
#         pairs = self.twoSum(nums, i+1, len(nums)-1, -nums[i])
#         for pair in pairs:
#             if len(pair) != 2:
#                 raise Exception("invalid two sum pair")
#             triplets.append([nums[i], pair[0], pair[1]])
#     return triplets

if __name__ == '__main__':
    print(three_sum([-3, 0, 1, 2, -1, 1, -2]))
    print(three_sum([-5, 2, -1, -2, 3]))
