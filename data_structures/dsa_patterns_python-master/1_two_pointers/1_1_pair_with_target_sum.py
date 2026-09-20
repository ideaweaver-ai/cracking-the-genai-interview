# O(N) time (array already sorted) | O(1) space
def pair_with_targetsum(arr, target_sum):
    # o/p var
    result = []
    # initialize two pointers
    left, right = 0, len(arr) - 1
    while left < right:
        pair_sum = arr[left] + arr[right]
        if pair_sum == target_sum:
            return [left, right]

        # Use the fact - array is sorted to increment or decrement one of the pointers
        elif pair_sum > target_sum:
            # we need to reduce pair_sum
            right -= 1
        else:
            # we need to increase pair_sum
            left += 1
    return result


# # O(n) hashmap solution
# def pair_with_targetsum(arr, target_sum):
#     num_index_map = {}
#     for index, num in enumerate(arr):
#         compliment = target_sum - num
#         if compliment in num_index_map:
#             return [num_index_map[compliment], index]
#         num_index_map[num] = index
#     return [-1, -1]


if __name__ == '__main__':
    print(pair_with_targetsum([1, 2, 3, 4, 5, 6], 6))